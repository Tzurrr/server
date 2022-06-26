import uvicorn
from fastapi import File, UploadFile, FastAPI
from typing import List
import encryptor
import elogger
import os
import json_parser


class MoreFilesThanExcpectedException(Exception):
    pass

class LessFilesThanExcpectedException(Exception):
    pass

async def merge_files(uploaded_files):
    contents = []
    for file in uploaded_files:
        contents.append(await file.read())
        await file.close()

    filename = uploaded_files[0].filename
    filename_clean = os.path.splitext(filename)[0][:-2]
    with open(f"../all-the-photos/{filename_clean}.jpg", "wb") as file:
        file.writelines(contents)
        filename = file.name
    return filename


app = FastAPI()


@app.post("/")
async def listen_for_uploaded_files(files: List[UploadFile] = File(...)):
    if len(files) < 2:
        raise LessFilesThanExcpectedException

    elif len(files) > 2:
        raise MoreFilesThanExcpectedException

    merged_file_name = await merge_files(files)
    elogger.write_logs_to_elastic("wrote")
    encryptor.encrypt(merged_file_name)
    return {"message": f"Successfuly uploaded {[file.filename for file in files]}"}


if __name__ == '__main__':
    conf = json_parser.parse_json_to_var("./config.json")
    app_conf = conf["apps_configuration"]
    uvicorn.run(app, host=app_conf["host"], port=app_conf["port"])
