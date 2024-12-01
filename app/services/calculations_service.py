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

def function_constructor(iterative, equationP, equationT, phaseConcat):

    if iterative:

        # Construct the name of the function using the phases provided by the userData object
        functionName = f'calculate{phaseConcat}_press_temp'

        return functionName

    elif equationP is not None : # Case to calculate P

        # Construct the name of the fonction using the phases provided by the userData object
        functionName = f'calculate{phaseConcat}_press, '

        return functionName

    elif equationT is not None : # Case to calculate T

        # Construct the name of the fonction using the phases provided by the userData object
        functionName = f'calculate{phaseConcat}_temp, '

        return functionName

    else :

        # if no equation is passed (SHOULD NOT HAPPEN) the system shutdown
        print(f"No equation passed shutting down")

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

    if iterative:

        # Construction of the arguments of the function and function call (arg)
        eqArg = f'equationP="{equationP}", equationT="{equationT}", '
        arguments = phaseArg + eqArg + 'eq_tests=True'

        return arguments

    elif equationP is not None : # Case to calculate P

        eqArg = f'equationP="{equationP}", '

        if tDependant: # If the equation is temperature dependant the temperature argument is added
            tempArg = f'T = {temperature}, '

        if h2oDependant: # If the equation is water content dependant the water content argument is added
            h2oArg = f'H2O_Liq = {h2o}, '

        # Construction of the arguments of the function and function call (arg)
        arguments = phaseArg + eqArg + tempArg + h2oArg + 'eq_tests=True'

        return arguments

    elif equationT is not None : # Case to calculate T

        eqArg = f'equationT="{equationT}", '

        if pDependant: # If the equation is temperature dependant the temperature argument is added
            pressArg = f'P = {pressure} ,'

        if h2oDependant: # If the equation is water content dependant the water content argument is added
            h2oArg = f'H2O_Liq = {h2o} ,'

        # Construction of the arguments of the function and function call (arg)
        arguments = phaseArg + eqArg + pressArg + h2oArg + 'eq_tests=True'

        return arguments

    else :
        # if no equation is passed (SHOULD NOT HAPPEN) the system shutdown
        print(f"No equation passed shutting down")