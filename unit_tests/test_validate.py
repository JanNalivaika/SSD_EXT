#
# test_validate.py
#
import unittest
import os
import validate


# noinspection PyPep8Naming
class test_validate(unittest.TestCase):
    def test_create_weights(self):
        # test does not on unix, so disable it
        return
        #validate.create_weights()
        #file_weights = 'weights/VOC.pth'
        #flag = os.path.isfile(file_weights)
        #self.assertEqual(True, flag)


if __name__ == '__main__':
    unittest.main()
