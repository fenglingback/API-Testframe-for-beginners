import unittest
import ddt
from Common.WrapRequest import http_req
from Common.GetDataFromYaml import getdata




shuju = getdata.return_data_from('user_data.yml', isMock=False)
# print(shuju)




@ddt.ddt
class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # makeLogFile("Test_HomePage")
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    @ddt.data(*shuju)
    def test_user(self, data):
        try:
            res = http_req.send_http(**data)
        except Exception as e:
            raise e








if __name__ == '__main__':
    unittest.main()
