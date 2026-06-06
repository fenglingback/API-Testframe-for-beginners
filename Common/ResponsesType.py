import json as _json
from nb_log import simple_logger
from requests import Response




class ResponsesType:
    def __init__(self, response: Response, logger=simple_logger):
        self.response = response
        self.logger = logger
        self.logger.info(f"状态码为：{self.response.status_code} {self.response.reason}")
        self.content_type = self.response.headers.get('Content-Type')
        self.logger.info(f"响应的类型为：{self.content_type}")

    def handle_resp(self, resp: Response):

        if self.content_type is not None:
            if ';' in self.content_type:
                self.content_type = self.content_type.split(';')[0]
            resp_type = self.content_type.split('/')
            sub = resp_type[0]
            subtype = resp_type[-1]

        if sub == 'text':
            content = Text(resp, subtype)
        elif sub == 'application':
            if subtype == 'json':
                content = Json(resp)
            elif subtype == 'xml':
                content = Xml(resp)
            elif subtype == 'octet-stream':
                content = OctetStream()
        elif sub == 'image':
            content = Image()
        else:
            raise Exception("响应类型还未进行判断处理......")



        return content




class Download(ResponsesType):
    def save_as_file(self, file_path):
        ...




class Text(ResponsesType):
    # def __init__(self, resp: Response, subtype) -> None:
    #     if subtype == 'plain':
    #         console_logger.info("返回的是纯文本！")
    #         console_logger.info(f"返回的 text 为：{resp.text}")
    def __init__(self, response: Response, subtype, logger=simple_logger):
        super().__init__(response, logger)



class Json(ResponsesType):
    def __init__(self, resp: Response) -> None:
        self.logger.info("返回的是 json！")
        self.logger.info(f"返回的 json 为：\n{_json.dumps(resp.json(), indent=4)}")



class Xml:
    def __init__(self, resp: Response) -> None:
        pass



class Image(Download):
    def __init__(self) -> None:
        print("this is image type!")

    def save_as_file(self, file_path):
        pass




class OctetStream(Download):
    def __init__(self) -> None:
        print("this is octet-stream type!")

    def save_as_file(self, file_path):
        ...


