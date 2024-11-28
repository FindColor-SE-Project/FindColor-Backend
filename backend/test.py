import unittest

from controllers.UserController import allowed_file

ALLOWED_EXTENSIONS = {'png', 'jpeg', 'jpg'}

class TestAllowedFileFunction(unittest.TestCase):

    def test_allowed_file_valid_extensions(self):
        # Test case 1: JPEG format (expected: True)
        self.assertTrue(allowed_file("girl.jpeg"))

        # Test case 2: PNG format (expected: True)
        self.assertTrue(allowed_file("image.png"))

        # Test case 3: GIF format (expected: False)
        self.assertFalse(allowed_file("200.gif"))


if __name__ == '__main__':
    unittest.main()
