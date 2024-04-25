import unittest
import ddt
from Common.WrapRequest import http_req
from Common.GetDataFromYaml import getdata


shuju = getdata.return_data_from('pet_data.yml', isMock=False)



@ddt.ddt
class TestPet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # makeLogFile("Test_HomePage")
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    @ddt.data(*shuju)
    def test_pet(self, data):
        res = http_req.send_http(**data)


if __name__ == '__main__':
    unittest.main()
