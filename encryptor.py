import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


def encrypt(filename):
    # hash
 #   print(filename)
    with open(filename, "rb") as file:
        file.seek(0)
        content = file.read()

    a = hashlib.sha512(str(content).encode())
    a = a.hexdigest()
 #   print(a)

    # iv for obj props
    iv = Random.new().read(AES.block_size)
#    print(iv)

    # getting the key which is also for generating the obj props
    with open("/home/tzur/server-tools1/keys/tornado.key", "rb") as file:#"/home/tzur/keys/tornado.key", "rb") as file:
        key = file.read() + b"    "  # [:24]

    # creating the obj
    obj = AES.new(key, AES.MODE_CFB, iv)

    # the hash encrypted with the object
    final_obj = base64.b64encode(obj.encrypt(a.encode()))

    with open(filename, "ab") as file:
        print((iv, final_obj))
        file.write(iv)
        file.write(final_obj)



def to_bytes(s):
    if type(s) is bytes:
        return s
    elif type(s) is str or (sys.version_info[0] < 3 and type(s) is unicode):
        return codecs.encode(s, 'utf-8')
    else:
        raise TypeError("Expected bytes or string, but got %s." % type(s))         
