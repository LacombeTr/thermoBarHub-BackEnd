# Create an object of what the application receive
from typing import Optional, List
from pydantic import BaseModel

"""
The models used serialize and validate the data exchanged with the Front-End.
"""

class calculationRequest(BaseModel):
    """Calculation request model correspond to what the Back-End receive from the Front-End """

    phases: List[str]
    """phases: a list of the phases used for calculation, can contain only one phase (ex: clinopyroxene)
    or two (ex: amphibole, liquid) (list[str])"""

    system: str
    """system: similar to phases (str)"""

    data: str
    """data: data used for calculations, correspond to the compositions of minerals, handled to the
       front-end as a table and converted to a single string (string)"""

    iterative: bool
    """iterative: if both temperature and pressure are calculated iteratively (boolean)"""

    equationP: Optional[str]
    """(optional) equationP: if the mode selected require the use of an equation to calculate P this
       equation is given here (string)"""

    equationT: Optional[str]
    """(optional) equationT: if the mode selected require the use of an equation to calculate T this
       equation is given here (string)"""

    pDependant: bool
    """pDependant: if one of the selected equation is dependant the pressure (boolean)"""

    tDependant: bool
    """tDependant: if one of the selected equation is dependant on the temperature (boolean)"""

    h2oDependant: bool
    """h2oDependant: if one of the selected equation is dependant on the water content of the melt (boolean)"""

    pressure: Optional[float]
    """(optional) pressure: if one of the selected equation require the pressure (float - kbar)"""

    temperature: Optional[float]
    """(optional) temperature: if one of the selected equation require the temperature  (float - K)"""

    h2o: Optional[float]
    """(optional) h2o: if one of the selected equation require the water content of the melt (float - %wt.)"""


class calculationResponse(BaseModel):
    """Calculation request model correspond to what the Back-End back send to the Front-End """

    phases: List[str]
    """phases: a list of the phases used for calculation, can contain only one phase (list[str])"""

    data: str
    """data: data used for calculations, correspond to the compositions of minerals, handled to the
       front-end as a table and converted to a single string (string)"""

    equationP: Optional[str]
    """(optional) equationP: if the mode selected require the use of an equation to calculate P this
       equation is given here (string)"""

    equationT: Optional[str]
    """(optional) equationT: if the mode selected require the use of an equation to calculate T this
       equation is given here (string)"""

    pressure: Optional[float]
    """(optional) pressure: if one of the selected equation require the pressure (float - kbar)"""

    temperature: Optional[float]
    """(optional) temperature: if one of the selected equation require the temperature  (float - K)"""

    h2o: Optional[float]
    """(optional) h2o: if one of the selected equation require the water content of the melt (float - %wt.)"""