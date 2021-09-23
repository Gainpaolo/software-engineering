import unittest
import os
def pass_path(path1):
    with open(path1,"r", encoding="utf8") as f:
        return f.read().splitlines()[0]
class demoRaiseTest(unittest.TestCase):
    def test_IO(self):
        self.assertRaises(IOError,pass_path,"E:/hh/3")

if __name__ == '__main__':
    unittest.main()
