#
# test_helper.py
#
import unittest
import os
import helper


# noinspection PyPep8Naming
class test_helper(unittest.TestCase):
    def test_create_weights(self):
        helper.create_weights()
        file_weights = 'weights/VOC.pth'
        flag = os.path.isfile(file_weights)
        self.assertEqual(True, flag)


if __name__ == '__main__':
    unittest.main()
