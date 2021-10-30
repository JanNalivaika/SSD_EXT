import unittest
import os
import validate


class ValidateTest(unittest.TestCase):

    def create_weights(self):
        validate.create_weigths()

        file_weights = 'weights/VOCx.pth'
        flag = os.path.isfile(file_weights)

        self.assertEqual(True, flag)


if __name__ == '__main__':
    unittest.main()
