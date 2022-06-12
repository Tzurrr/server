def find(filename):
#    print(filename)
    for i in range(len(filename)):
        if filename[i] == ".":
            return i#filename[:i]
    return len(filename)

