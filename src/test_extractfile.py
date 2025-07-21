import unittest

class TestExtractTitle(unittest.TestCase):
    def test_no_h1_raises_exception(self):
        md = """
        ## This is an H2 header
        Some random text
        ###
        """
        with self.assertRaises(Exception):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()