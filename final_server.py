import uvicorn
from fastapi import File, UploadFile, FastAPI
from typing import List
import find_dot
import encryptor
import elogger
import os
import file_merger
import json_parser

app = FastAPI()

@app.post("/")
async def upload(files: List[UploadFile] = File(...)):
    filename = file_merger.merge_halfs(files)
    elogger.write_logs_to_elastic("wrote")
    encryptor.encrypt(filename)
    return {"message": f"Successfuly uploaded {[file.filename for file in files]}"}

if __name__ == '__main__':
    conf = json_parser.parse_json_to_var("/home/tzur/server/config.json")
    app_conf = conf["apps_configuration"]
    uvicorn.run(app, host=apps_conf["host"], port=apps_conf["port"])

