#
# test_validate.py
#
import unittest
import validate


# noinspection PyPep8Naming
class test_validate(unittest.TestCase):
    def test_run(self):
        log = validate.run()
        self.assertTrue("found feature 4.0 in picture data/MulSet/set20/90_5.png" in log)


if __name__ == '__main__':
    unittest.main()
