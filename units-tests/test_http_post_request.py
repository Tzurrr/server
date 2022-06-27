import unittest
import final_server
import requests
import encryptor
import os


class TestInotify(unittest.TestCase):
    def setUp(self):
        self.url_path = "http://0.0.0.0:8000/"

        with open("file1_a.txt", "wb+") as file:
            file.write(b"a")
            self.filepath = file.name
        with open("file1_b.txt", "wb+") as file:
            file.write(b"b")
            self.filename_from_redis = file.name

    def test_merge(self):
        arr = [("files", open(self.filepath, "rb")), ("files", open(self.filename_from_redis, "rb"))]
        requests.post(url=self.url_path, files=arr)
        
        with open("../all-the-photos/file1.jpg", "rb") as file:
            contents = file.read()

        with open("file1_a.txt", "rb") as file:
            a=file.read()
        with open("file1_b.txt", "rb") as file:
            a+=file.read()
        
        self.assertEqual(contents, a)

    def test_only_one_file(self):
        arr = [("files", open(self.filepath, "rb"))]
        requests.post(url=self.url_path, files=arr)
        self.assertRaises(Exception, final_server)

    def test_more_than_two_files(self):
        with open("file1_c.txt", "wb+") as file:
            file.write(b"c")
            filename = file.name

        arr = [("files", open(self.filepath, "rb")),
        ("files", open(self.filename_from_redis, "rb")),
        ("files", open(filename, "rb"))]
        requests.post(url=self.url_path, files=arr)
        os.remove("file1_c.txt")

        self.assertRaises(Exception, final_server)

    def tearDown(self):
        os.remove("file1_a.txt")
        os.remove("file1_b.txt")

if __name__ == '__main__':
    unittest.main()

