from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import threefive
import base64

app = FastAPI()

class SCTE35Request(BaseModel):
    scte35_string: str
    format: str  # "base64" or "hex"

@app.post("/parse_scte35/")
async def parse_scte35(request: SCTE35Request):
    try:
        if request.format == "base64":
            scte35_data = base64.b64decode(request.scte35_string)
        elif request.format == "hex":
            scte35_data = bytes.fromhex(request.scte35_string)
        else:
            raise HTTPException(status_code=400, detail="Invalid format. Use 'base64' or 'hex'.")
        
        cue = threefive.Cue(scte35_data)
        cue.decode()
        return cue.get()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

