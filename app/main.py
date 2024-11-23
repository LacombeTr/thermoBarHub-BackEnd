from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app"}

@app.get("/calculate")
def calculate():
    # Exemple utilisant numpy et pandas
    data = np.array([1, 2, 3, 4])
    df = pd.DataFrame(data, columns=["Numbers"])
    return {"dataframe": df.to_dict()}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)