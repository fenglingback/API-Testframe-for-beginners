import unittest
import ddt
from Common.WrapRequest import HttpRequest
from nb_log import LogManager
from Common.GetDataFromYaml import getdata




shuju = getdata.return_data_from('user_data.yml', isMock=False)
# print(shuju)




@ddt.ddt
class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # makeLogFile("Test_HomePage")
        # cls.logger = MyLogger(is_stream=False, file_name='TestUser.log').logger
        cls.logger = LogManager('TestUser').get_logger_and_add_handlers(is_add_stream_handler=False, log_filename='TestUser.log')
        cls.http_req = HttpRequest(logger=cls.logger)
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    @ddt.data(*shuju)
    def test_user(self, data):
        try:
            res = self.http_req.send_http(**data)
        except Exception as e:
            self.logger.exception(e)
            raise e







if __name__ == '__main__':
    unittest.main()
