from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import thermobarometry

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
#
# @appCalculationThermobar.post("/api/calculate", response_model=calculationResponse)
appCalculationThermobar.include_router(thermobarometry.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(appCalculationThermobar, host='localhost:8000', port=8000)