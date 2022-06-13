import uvicorn
from fastapi import File, UploadFile, FastAPI
from typing import List
import find_dot
import encryptor
import elogger

app = FastAPI()

@app.post("/")
async def upload(files: List[UploadFile] = File(...)):
    contents = []
    for file in files:
        await file.seek(0)
        contents.append(await file.read())
        await file.close()
        dot = find_dot.find(file.filename)
    with open (f"/home/tzur/all-the-photos/{file.filename[:dot-2]}.jpg", "wb") as file:
        file.writelines(contents)
        filename = file.name
    elogger.write_logs_to_elastic("wrote")
    encryptor.encrypt(filename)
    return {"message": f"Successfuly uploaded {[file.filename for file in files]}"}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
    intro = "/home/tzur/getters/"

