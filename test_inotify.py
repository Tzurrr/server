import unittest
import final_server
import requests
import encryptor
import os


class TestInotify(unittest.TestCase):
    def setUp(self):
        url_path = "http://0.0.0.0:8000/"

        with open("file1_a.txt", "wb+") as file:
            file.write(b"a")
            filepath = file.name
        with open("file1_b.txt", "wb+") as file:
            file.write(b"b")
            filename_from_redis = file.name

        arr = [("files", open(filepath, "rb")), ("files", open(filename_from_redis, "rb"))]
        requests.post(url=url_path, files=arr)

    def test_merge(self):
        with open("../all-the-photos/file1.jpg", "rb") as file:
            contents = file.read()

        a = b""
        with open("file1_a.txt", "rb") as file:
            a+=file.read()
        with open("file1_b.txt", "rb") as file:
            a+=file.read()

        #
#        with open("file.txt", "wb") as file:
 #           file.write(a)
  #          filename = file.name
   #     encryptor.encrypt(filename)
    #    with open("file.txt", "rb") as file:
     #       a = file.read()
        #
        
        self.assertEqual(contents, a)
    
    def test_only_one_file(self):
        self.assertRaises(Exception, final_server)

    def tearDown(self):
        os.remove("file1_a.txt")
        os.remove("file1_b.txt")
        #os.remove("file.txt")
        

if __name__ == '__main__':
    unittest.main()

