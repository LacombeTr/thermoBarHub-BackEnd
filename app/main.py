from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import pandas as pd
import Thermobar as TB

from app.services.calculations_service import argument_constructor
from app.utils.utils import rename_duplicate_columns
from app.services.calculations_service import function_constructor
from app.utils.models import calculationRequest, calculationResponse

# Create an instance of the app
appCalculationThermobar = FastAPI()

appCalculationThermobar.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# _________________________________________________________________________________

@appCalculationThermobar.post("/api/calculate", response_model=calculationResponse)

async def calculate(request: calculationRequest):

    phaseConcat = ''
    phasesVariableList = {}
    phaseArg = ''

    userData = request

    # Transform the stringified json into usable dataframe ___________________________________________________

    userData.data = json.loads(userData.data)
    userData.data = userData.data["Feuil1"]

    userData.data = pd.DataFrame(userData.data)

    print(userData)

    for phase in userData.phases:
        globals()[f'compo_{phase.lower()}'] = userData.data.filter(regex = '_' + phase)
        phasesVariableList[f'compo_{phase.lower()}'] = f'compo_{phase.lower()}'

        phaseConcat = phaseConcat + '_' + phase.lower() # used later for function name

        phaseArg = phaseArg + f'{phase.lower()}_comps = compo_{phase.lower()}, ' # used later for argument construction

    if len(userData.phases) == 1: # Case where there is only one phase the name of the function will be "phase_only_"
        phaseConcat = f'_{phase(0).lower()}_only'

    # Creating the function name and the arguments for the different cases ___________________________________

    function_name = function_constructor(userData.iterative,
                                         userData.equationP,
                                         userData.equationT,
                                         userData.phaseConcat)

    arguments = argument_constructor(userData.iterative,
                                         userData.tDependant,
                                         userData.pDependant,
                                         userData.h2oDependant,
                                         userData.equationP,
                                         userData.equationT,
                                         phaseArg,
                                         userData.temperature,
                                         userData.pressure,
                                         userData.h2o)

    # Get this function using getattr (get attribute of the TB)
    # if the function doesn't exist an error is raised and the system is shut down

    try:
        function_to_call = getattr(TB, function_name)
    except:
        print(f"The function {function_name} doesn't exist in ThermoBar")
        raise SystemExit

    calculations = function_to_call(**eval(f"dict({arguments})"))

    calculations = rename_duplicate_columns(calculations) # In case of duplicate column name (in the case of CPX-OPX syem for example, two columns for the components exists for each pyroxene)

    calculations = calculations.to_json(orient='records', lines=False)

    return calculationResponse(

        phases=request.phases,
        equationP=request.equationP,
        equationT=request.equationT,
        pressure=request.pressure,
        temperature=request.temperature,
        h2o = request.h2o,
        data=calculations
    )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(appCalculationThermobar, host='localhost:8000', port=8000)