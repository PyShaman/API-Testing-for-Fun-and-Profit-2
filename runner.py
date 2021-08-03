import unittest

# Import test modules
import tests.authentication as auth
import tests.client as client
import tests.clients as clients

# Initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# Add test to the test suite
suite.addTest(loader.loadTestsFromModule(auth))
suite.addTest(loader.loadTestsFromModule(client))
suite.addTest(loader.loadTestsFromModule(clients))

# Initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
