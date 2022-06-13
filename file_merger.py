def merge_halfs(files):
    contents = []
    for file in files:
        contents.append(await file.read())
        await file.close()
    with open (f"/home/tzur/all-the-photos/{os.path.splitext(file.filename)[0]}.jpg", "wb") as file:
        file.writelines(contents)
        filename = file.name
    return filename
