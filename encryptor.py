import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


def encrypt(filename):
    with open(filename, "rb") as file:
        file_contents = file.read()

    a = hashlib.sha512(str(file_contents).encode())
    a = a.hexdigest()
    iv = Random.new().read(AES.block_size)

    with open("./keys/tornado.key", "rb") as file:
        key = file.read() + b"    "  # [:24]

    obj = AES.new(key, AES.MODE_CFB, iv)
    final_obj = base64.b64encode(obj.encrypt(a.encode()))

    with open(filename, "ab") as file:
        file.writelines([iv, final_obj])

