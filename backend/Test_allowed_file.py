import unittest

# ฟังก์ชันที่เราจะทดสอบ
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Test_allowed_file(unittest.TestCase):
    def test_allowed_file_valid_file_type(self):
        self.assertTrue(allowed_file("archive.jpg"))
        self.assertTrue(allowed_file("archive.png"))

    def test_allowed_file_invalid_file_type(self):
        self.assertFalse(allowed_file("archive.zip"))

if __name__ == '__main__':
    unittest.main()
