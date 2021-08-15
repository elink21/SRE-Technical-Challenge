import unittest
from methods import Token, Restricted


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.convert = Token()
        self.validate = Restricted()

    # Since the original JWT test didn't fulfill format requirements (role located on JWT payload),
    # it was modified to match the required data,
    # JWT token was validated using https://jwt.io/#libraries-io
    def test_generate_token(self):
        self.assertEqual('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiYWRtaW4ifQ.BmcZ8aB5j8wLSK8CqdDwkGxZfFwM1X1gfAIN7cXOx9w',
                         self.convert.generate_token('admin', 'secret'))

    def test_access_data(self):
        self.assertEqual('You are under protected data with admin permissions', self.validate.access_data(
            'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiYWRtaW4ifQ.BmcZ8aB5j8wLSK8CqdDwkGxZfFwM1X1gfAIN7cXOx9w'))

    def testRoleAssignment(self):
        self.assertEqual("You are under protected data with viewer permissions", self.validate.access_data(
            'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoidmlld2VyIn0._k6kmfmdOoKWWMT4qk9nFTz-7k-X_0UdS8tByaCaye8'
        ))

        self.assertEqual("You are under protected data with editor permissions", self.validate.access_data(
            'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiZWRpdG9yIn0.C01pddxYdEY0qum6u_jlQYx3QWpf5NwXJtMq1yoWhc0'
        ))

    def testLoginError(self):
        self.assertFalse(self.convert.generate_token("", ""))
        self.assertFalse(self.convert.generate_token("", "secret"))
        self.assertFalse(self.convert.generate_token("admin", ""))

    def testAccessError(self):
        self.assertFalse(self.validate.access_data(
            "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiZWRpdG9yIn0.C01pddxYdEY0XJtMq1yoWhc0"))
        self.assertFalse(self.validate.access_data("Bearer"))
        self.assertFalse(self.validate.access_data(""))


if __name__ == '__main__':
    unittest.main()
