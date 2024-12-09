from fastapi import APIRouter

from app.services.thermobarometryService import calculate_thermobaro
from app.utils.models import calculationRequest, calculationResponse

router = APIRouter()

@router.post("/api/thermobarometry")

async def create_thermobaro_calculation(request: calculationRequest, response_model=calculationResponse):

    calculations = calculate_thermobaro(request)

    return calculations
