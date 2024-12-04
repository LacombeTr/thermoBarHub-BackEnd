import pytest
from app.services.calculations_service import *

# Parameters for the test of function_constructor
@pytest.mark.parametrize("iterative, equationP, equationT, phase_concat, expected_function",
[
    (False, "placeHolderPEquation", None, "_cpx_liq",                        # Set of parameter for this scenario
        "calculate_cpx_liq_press"),                                          # Excepted result
    (False, None, "placeHolderTEquation", "_cpx_liq",
        "calculate_cpx_liq_temp"),
    (True, "placeHolderPEquation", "placeHolderTEquation", "_cpx_liq",
        "calculate_cpx_liq_press_temp"),

    (True, None, None, "_cpx_liq",
        "calculate_cpx_liq_press_temp"),
    (False, None, None, "_cpx_liq",
        "No equation passed, shutting down"),
], ids=
[
    "Should pass - Calculate P non iteratively",
    "Should pass - Calculate T non iteratively",
    "Should pass - Calculate P and T iteratively",

    "Should pass - Calculate iteratively with no P and T equation given",
    "Should fail - Calculate non iteratively with no P and T equation given",
])

def test_function_constructor(iterative, equationP, equationT, phase_concat, expected_function):
    assert function_constructor(iterative, equationP, equationT, phase_concat) == expected_function

# Parameters for the test of argument_constructor
@pytest.mark.parametrize("iterative, tDependant, pDependant, h2oDependant, equationP, equationT, phaseArg, temperature, pressure, h2o,"
                                "expected_arguments",
[
    (False, False, False, False, "placeHolderPEquation", None, "phase_comps = compo_phases, ", None, None, None,
            'phase_comps = compo_phases, equationP="placeHolderPEquation", eq_tests=True'),
    (False, True, False, False, "placeHolderPEquation", None, "phase_comps = compo_phases, ", 1000, None, None,
            'phase_comps = compo_phases, equationP="placeHolderPEquation", T = 1000, eq_tests=True'),
    (False, False, False, True, "placeHolderPEquation", None, "phase_comps = compo_phases, ", None, None, 3,
            'phase_comps = compo_phases, equationP="placeHolderPEquation", H2O_Liq = 3, eq_tests=True'),
    (False, True, False, True, "placeHolderPEquation", None, "phase_comps = compo_phases, ", 1000, None, 3,
            'phase_comps = compo_phases, equationP="placeHolderPEquation", T = 1000, H2O_Liq = 3, eq_tests=True'),

    (False, False, False, False, None, "placeHolderTEquation", "phase_comps = compo_phases, ", None, None, None,
            'phase_comps = compo_phases, equationT="placeHolderTEquation", eq_tests=True'),
    (False, False, True, False, None, "placeHolderTEquation", "phase_comps = compo_phases, ", None, 3.5, None,
            'phase_comps = compo_phases, equationT="placeHolderTEquation", P = 3.5, eq_tests=True'),
    (False, False, False, True, None, "placeHolderTEquation", "phase_comps = compo_phases, ", None, None, 3,
            'phase_comps = compo_phases, equationT="placeHolderTEquation", H2O_Liq = 3, eq_tests=True'),
    (False, False, True, True, None, "placeHolderTEquation", "phase_comps = compo_phases, ", None, 3.5, 3,
            'phase_comps = compo_phases, equationT="placeHolderTEquation", P = 3.5, H2O_Liq = 3, eq_tests=True'),

    (True, True, True, False, "placeHolderPEquation", "placeHolderTEquation", "phase_comps = compo_phases, ", None, None, None,
            'phase_comps = compo_phases, equationP="placeHolderPEquation", equationT="placeHolderTEquation", eq_tests=True'),
    (True, True, True, True, "placeHolderPEquation", "placeHolderTEquation", "phase_comps = compo_phases, ", None, None, 3,
            'phase_comps = compo_phases, equationP="placeHolderPEquation", equationT="placeHolderTEquation", H2O_Liq = 3, eq_tests=True'),
    (True, False, False, False, None, None, "phase_comps = compo_phases, ", None, None, None,
            'No equation passed shutting down'),
], ids=
[
    "Should pass - Calculate P non iteratively",
    "Should pass - Calculate P non iteratively with T-dependant equation",
    "Should pass - Calculate P non iteratively with H2O-dependant equation",
    "Should pass - Calculate P non iteratively with H2O-dependant and T-dependant equation",

    "Should pass - Calculate T non iteratively",
    "Should pass - Calculate T non iteratively with P-dependant equation",
    "Should pass - Calculate T non iteratively with H2O-dependant equation",
    "Should pass - Calculate T non iteratively with H2O-dependant and P-dependant equation",

    "Should pass - Calculate P and T iteratively, both co-dependant",
    "Should pass - Calculate P and T iteratively, both co-dependant and with H2O dependant equation",
    "Should fail - Calculate P and T iteratively but not providing the equations",
])

def test_arguments_constructor(iterative, tDependant, pDependant, h2oDependant, equationP, equationT, phaseArg, temperature, pressure, h2o, expected_arguments):
    assert argument_constructor(iterative, tDependant, pDependant, h2oDependant, equationP, equationT, phaseArg, temperature, pressure, h2o) == expected_arguments