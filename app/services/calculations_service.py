def function_constructor(iterative, tDependant, pDependant, h2oDependant, equationP, equationT, phaseArg, phaseConcat, temperature, pressure, h2o):

    if iterative:

        # Construct the name of the function using the phases provided by the userData object
        functionName = f'calculate{phaseConcat}_press_temp'

        # Construction of the arguments of the function and function call (arg)
        eqArg = f'equationP="{equationP}", equationT="{equationT}", '
        arguments = phaseArg + eqArg + 'eq_tests=True'

    elif equationP is not None : # Case to calculate P

        # Construct the name of the fonction using the phases provided by the userData object
        functionName = f'calculate{phaseConcat}_press, '

        eqArg = f'equationP="{equationP}", '
        tempArg = ''
        h2oArg = ''

        if tDependant: # If the equation is temperature dependant the temperature argument is added
            tempArg = f'T = {temperature}, '

        if h2oDependant: # If the equation is water content dependant the water content argument is added
            h2oArg = f'H2O_Liq = {h2o}, '

        # Construction of the arguments of the function and function call (arg)
        arguments = phaseArg + eqArg + tempArg + h2oArg + 'eq_tests=True'

    elif equationT is not None : # Case to calculate T
        # Construct the name of the fonction using the phases provided by the userData object
        functionName = f'calculate{phaseConcat}_temp, '

        eqArg = f'equationT="{equationT}", '
        pressArg = ''
        h2oArg = ''

        if pDependant: # If the equation is temperature dependant the temperature argument is added
            pressArg = f'P = {pressure} ,'

        if h2oDependant: # If the equation is water content dependant the water content argument is added
            h2oArg = f'H2O_Liq = {h2o} ,'

        # Construction of the arguments of the function and function call (arg)
        arguments = phaseArg + eqArg + pressArg + h2oArg + 'eq_tests=True'

    else :
        # if no equation is passed (SHOULD NOT HAPPEN) the system shutdown
        print(f"No equation passed shutting down")
        raise SystemExit