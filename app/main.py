from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import pandas as pd # Used to manipulate dataframes
import Thermobar as TB # Core of calculation

# Create an instance of the app
appCalculationThermobar = FastAPI()

appCalculationThermobar.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Create an object of what the appliction receive
class CalculationRequest(BaseModel):
    data: str
    equationP: Optional[str]
    equationT: Optional[str]
    h2o: Optional[float]
    h2oDependant: bool
    iterative: bool
    pDependant: bool
    phases: List[str]
    pressure: Optional[float]
    system: str
    tDependant: bool
    temperature: Optional[float]

# Create an object of what the application send back
class CalculationResponse(BaseModel):
    phases: List[str]
    equationP: Optional[str]
    equationT: Optional[str]
    pressure: Optional[float]
    temperature: Optional[float]
    h2o: Optional[float]
    data: str

# _________________________________________________________________________________

@appCalculationThermobar.post("/api/calculate", response_model=CalculationResponse)

async def calculate(request: CalculationRequest):

    phaseConcat = ''
    phasesVarableList = {}
    phaseArg = ''

    userData = request

    # Transform the stringified json into usable dataframe ___________________________________________________

    userData.data = json.loads(userData.data)
    userData.data = userData.data["Feuil1"]

    userData.data = pd.DataFrame(userData.data)

    print(userData)

    for phase in userData.phases:
        globals()[f'compo_{phase.lower()}'] = userData.data.filter(regex = '_' + phase)
        phasesVarableList[f'compo_{phase.lower()}'] = f'compo_{phase.lower()}'

        phaseConcat = phaseConcat + '_' + phase.lower() # used later for function name

        phaseArg = phaseArg + f'{phase.lower()}_comps = compo_{phase.lower()}, ' # used later for argument construction

    if len(userData.phases) == 1: # Case where there is only one phase the name of the function will be "phase_only_"
        phaseConcat = f'_{phase(0).lower()}_only'

    # Creating the function name and the arguments for the different cases ___________________________________

    function_name = functionConstructor(userData.iterative,
                                        userData.tDependant,
                                        userData.pDependant,
                                        userData.h2oDependant,
                                        userData.equationP,
                                        userData.equationT,
                                        phaseArg,
                                        phaseConcat,
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

    return CalculationResponse(

        phases=request.phases,
        equationP=request.equationP,
        equationT=request.equationT,
        pressure=request.pressure,
        temperature=request.temperature,
        h2o = request.h2o,
        data=calculations
    )



def functionConstructor(iterative, tDependant, pDependant, h2oDependant, equationP, equationT, phaseArg, phaseConcat, temperature, pressure, h2o):

    if iterative == True:

        # Construct the name of the fonction using the phases provided by the userData object
        functionName = f'calculate{phaseConcat}_press_temp'

        # Construction of the arguments of the function and function call (arg)
        eqArg = f'equationP="{equationP}", equationT="{equationT}", '
        arguments = phaseArg + eqArg + 'eq_tests=True'

    elif equationP != None : # Case to calculate P

        # Construct the name of the fonction using the phases provided by the userData object
        functionName = f'calculate{phaseConcat}_press, '

        eqArg = f'equationP="{equationP}", '
        tempArg = ''

        if tDependant == True: # If the equation is temperature dependant the temperature argument is added
            tempArg = f'T = {temperature}, '

        if h2oDependant == True: # If the equation is water content dependant the water content argument is added
            h2oArg = f'H2O_Liq = {h2o}, '

        # Construction of the arguments of the function and function call (arg)
        arguments = phaseArg + eqArg + tempArg + h2oArg + 'eq_tests=True'

    elif equationT != None : # Case to calculate T
        # Construct the name of the fonction using the phases provided by the userData object
        functionName = f'calculate{phaseConcat}_temp, '

        eqArg = f'equationT="{equationT}", '
        pressArg = ''

        if pDependant == True: # If the equation is temperature dependant the temperature argument is added
            pressArg = f'P = {pressure} ,'

        if h2oDependant == True: # If the equation is water content dependant the water content argument is added
            h2oArg = f'H2O_Liq = {h2o} ,'

        # Construction of the arguments of the function and function call (arg)
        arguments = phaseArg + eqArg + pressArg + h2oArg + 'eq_tests=True'

    else :
        # if no equation is passed (SHOULD NOT HAPPEN) the system shutdown
        print(f"No equation passed shutting down")
        raise SystemExit

# Function to correct if there is duplicated column names (which case the change to a json will fail at the end of calculations)
def rename_duplicate_columns(df):

    new_columns = []
    column_count = {}

    for col in df.columns:
        if col in column_count:
            column_count[col] += 1
            new_columns.append(f"{col}_{column_count[col]}")
        else:
            column_count[col] = 0
            new_columns.append(col)

    df.columns = new_columns
    return df

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(appCalculationThermobar, host='localhost:8000', port=8000)