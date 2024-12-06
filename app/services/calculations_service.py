from typing import List

def phase_concatenate(phases: List[str]):
    '''
    ### Phase Concatenation

    Transform the list of phases into a string that can be injected to construct function names

    :param phases: list of phases required by the chosen equations *(list[str])*
    :return: a string of the phases names
    '''

    if len(phases) == 1:
        return f"_{phases[0].lower()}_only"

    return "".join([f"_{phase.lower()}" for phase in phases])

def phase_arg_constructor(arguments_dict, phases):
    '''
    ### Phase argument constructor

    Transform the list of phases into an argument that will be passed to the function argument_constructor

    :param arguments_dict:
    :param phases: list of phases required by the chosen equations *(list[str])*
    :return: a string of the phases names in the form of an argument
    '''
    for phase in phases:
        arguments_dict[f'{phase.lower()}_comps'] = f'compos_{phase.lower()}'
        print(arguments_dict[f'{phase.lower()}_comps'])

def function_constructor(iterative, equationP, equationT, phaseConcat):
    """
    ### Dynamic function constructor

    Construct the function name used based on the input of the user.

    :param iterative: Is the calculation mode iterative? Equation for both P and T must be provided. *(bool)*
    :param equationP: Equation chosen to calculate P. *(str || null)*
    :param equationT: Equation chosen to calculate T. *(str || null)*
    :param phaseConcat: Used phases used for calculations. *(str)*

    :return: the name of the function to call *(str)*.
    ___________
    """

    if iterative:

        # Construct the name of the function using the phases provided by the userData object
        functionName = f'calculate{phaseConcat}_press_temp'

        return functionName

    elif equationP is not None : # Case to calculate P

        # Construct the name of the fonction using the phases provided by the userData object
        functionName = f'calculate{phaseConcat}_press'

        return functionName

    elif equationT is not None : # Case to calculate T

        # Construct the name of the fonction using the phases provided by the userData object
        functionName = f'calculate{phaseConcat}_temp'

        return functionName

    else :

        # if no equation is passed the system shutdown
        return "No equation passed, shutting down"

def argument_constructor(iterative, tDependant, pDependant, h2oDependant, equationP, equationT, phaseArg, temperature, pressure, h2o):
    """
    ### Dynamic argument constructor

    Construct the arguments used by the function defined in function_constructor.

    :param iterative: Is the calculation mode iterative? Equation for both P and T must be provided. *(bool)*
    :param tDependant: Is one of the equation chosen equation is temperature-dependant ? *(bool)*
    :param pDependant: Is one of the equation chosen equation is pressure-dependant ? *(bool)*
    :param h2oDependant: Is one of the equation chosen equation is water content-dependant ? *(bool)*
    :param equationP: Equation chosen to calculate P. *(str || null)*
    :param equationT: Equation chosen to calculate T. *(str || null)*
    :param phaseArg: Name of the dictionary(ies) containing the compositions of the phases used for calculations. *(str)*
    :param temperature: Temperature in K. *(float || null)*
    :param pressure: Pressure in kbar. *(float || null)*
    :param h2o: Water content in %wt. . *(float || null)*

    :return: the arguments used by the function *(str)*.
    ___________
    """

    arguments = {"eq_tests": True} # initializing the argument dictionary with this value by default
    phase_arg_constructor(arguments, phaseArg)

    if h2oDependant:  # If the equation is water content dependant the water content argument is added
        arguments["H2O_Liq"] = h2o

    if iterative:

        if equationP is not None and equationT is not None :
            # Construction of the arguments of the function and function call (arg)
            arguments["equationP"] = equationP
            arguments["equationT"] = equationT

            return arguments

        else:

            return "No equation passed shutting down"

    elif equationP is not None : # Case to calculate P

        arguments["equationP"] = f'"{equationP}"'

        if tDependant: # If the equation is temperature dependant the temperature argument is added
            arguments["T"] = temperature

        return arguments

    elif equationT is not None : # Case to calculate T

        arguments["equationT"] = f'"{equationT}"'

        if pDependant: # If the equation is temperature dependant the temperature argument is added
            arguments["P"] = pressure

        return arguments

    else :
        # if no equation is passed (SHOULD NOT HAPPEN) the system shutdown
        return "No equation passed shutting down"