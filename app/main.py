from fastapi import FastAPI
from typing import List, Dict
import numpy as np
import pandas as pd
import thermobar

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app"}

@app.get("/calculate")
def calculate():
    # Exemple utilisant numpy et pandas
    data = np.array([1, 2, 3, 4])
    df = pd.DataFrame(data, columns=["Numbers"])
    return {"dataframe": df.to_dict()}