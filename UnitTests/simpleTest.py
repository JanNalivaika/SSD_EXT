import unittest
from simple import simple


class SimpleTest(unittest.TestCase):
    def test_SimpleA(self):
        self.assertEqual(simple('hello'), 'hello')


if __name__ == '__main__':
    unittest.main()
