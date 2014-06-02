import unittest

if __name__ == '__main__':
    testsuite = unittest.TestLoader().discover('./src/test/python/')
    unittest.TextTestRunner(verbosity=1).run(testsuite)