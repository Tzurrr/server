import uvicorn
from fastapi import File, UploadFile, FastAPI
from typing import List
import encryptor
import elogger
import os
import json_parser

async def merge_files(uploaded_files):
    contents = []
    for file in uploaded_files:
        contents.append(await file.read())
        await file.close()
    with open (f"../all-the-photos/{os.path.splitext(file.filename)[0][:-2]}.jpg", "wb") as file:
        file.writelines(contents)
        filename = file.name
    return filename


app = FastAPI()

@app.post("/")
async def listen_for_uploaded_files(files: List[UploadFile] = File(...)):
    merged_file_name = await merge_files(files)
    elogger.write_logs_to_elastic("wrote")
    encryptor.encrypt(merged_file_name)
    return {"message": f"Successfuly uploaded {[file.filename for file in files]}"}

if __name__ == '__main__':
    conf = json_parser.parse_json_to_var("/home/tzur/server/config.json")
    app_conf = conf["apps_configuration"]
    uvicorn.run(app, host=app_conf["host"], port=app_conf["port"])

