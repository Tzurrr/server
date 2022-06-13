import uvicorn
from fastapi import File, UploadFile, FastAPI
from typing import List
import find_dot
import encryptor
import elogger
import os
import file_merger

app = FastAPI()

@app.post("/")
async def upload(files: List[UploadFile] = File(...)):
    filename = file_merger.merge_halfs(files)
    elogger.write_logs_to_elastic("wrote")
    encryptor.encrypt(filename)
    return {"message": f"Successfuly uploaded {[file.filename for file in files]}"}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

