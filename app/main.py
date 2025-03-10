from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import pandas as pd
import Thermobar as TB

from app.services.calculations_service import argument_constructor
from app.utils.utils import rename_duplicate_columns
from app.services.calculations_service import function_constructor, phase_concatenate, phase_arg_constructor
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

    userData = request

    # print(userData.data)
    # Transform the stringified json into usable dataframe ___________________________________________________

    userData.data = pd.DataFrame(userData.data)

    print(userData.data)

    # Creating the function name and the arguments for the different cases ___________________________________

    function_name = function_constructor(userData.iterative,
                                         userData.equationP,
                                         userData.equationT,
                                         phase_concatenate(userData.phases))

    arguments = argument_constructor(userData.iterative,
                                         userData.tDependant,
                                         userData.pDependant,
                                         userData.h2oDependant,
                                         userData.equationP,
                                         userData.equationT,
                                         userData.phases,
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

    calculations = function_to_call(**arguments)

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