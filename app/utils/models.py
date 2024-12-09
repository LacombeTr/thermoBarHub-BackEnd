# Create an object of what the application receive
from typing import Optional, List
from pydantic import BaseModel

"""
The models used serialize and validate the data exchanged with the Front-End.
"""

class calculationRequest(BaseModel):

    """
    Calculation request model correspond to what the Front-End send to the Back-End
    """

    phases: List[str]
    system: str
    data: str
    iterative: bool
    equationP: Optional[str]
    equationT: Optional[str]
    pDependant: bool
    tDependant: bool
    h2oDependant: bool
    pressure: Optional[float]
    temperature: Optional[float]
    h2o: Optional[float]


class calculationResponse(BaseModel):
    """
    Calculation response model correspond to what the Back-End send back to the Front-End
    """

    phases: List[str]
    data: str
    equationP: Optional[str]
    equationT: Optional[str]
    pressure: Optional[float]
    temperature: Optional[float]
    h2o: Optional[float]