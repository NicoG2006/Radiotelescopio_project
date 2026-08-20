from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from radio_logic import astronomy_logic as astro
from radio_logic import star_data as sd

app = FastAPI(title="RadioHunter || Nicolás García Parra")

class stuctCoord(BaseModel):
    ra:float
    dec:float

current_angle = {
    "az": 0.0,
    "alt": 0.0,
}

@app.get("/greet")
def greet():
    try:
        return{
            "status" : "Server online",
            "message" : "This server is ok"
        }
    except Exception as e:
        print(f"error:{e}")

@app.post("/api/track/sun")
def trackSun():
    try:
        az, alt = astro.buscar_sol()
        current_angle["az"]=az
        current_angle["alt"]=alt
        return{
            "status": "Upload target",
            "Coords" : f"az:{az},alt:{alt}" 
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/track/object")
def trackObject(coord:stuctCoord):
    try:
        az, alt = astro.rastrear(coord.ra, coord.dec)
        current_angle["az"]=az
        current_angle["alt"]=alt
        return{
            "status": "Upload target",
            "Coords": f"az:{az},alt:{alt}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/track/savedObj")
def track_savedOBJ(name:str):
    try:
        coords= sd.buscar_obj(name)
        if (coords)==None:
            raise HTTPException(status_code=500, detail=str(f"{name} not exist on catalog"))
        ra,dec = coords
        az, alt = astro.rastrear(ra,dec)
        current_angle["az"]=az
        current_angle["alt"]=alt
        return{
            "Status": "Upload Target",
            "Coords": f"az.{az},alt{alt}"
        }
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/data/save")
def save(name:str, ra:float, dec:float):
    sd.guardar_obj(name, ra, dec)


@app.get("/api/target")
def getTarget():
    return current_angle
