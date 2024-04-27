from requests import Response
from kuai_log import k_logger
import json as _json



class Download:
    def save_as_file(self, file_path):
        ...


class Text:
    def __init__(self, resp: Response, subtype) -> None:
        if subtype == 'plain':
            k_logger.info("返回的是纯文本！")
            k_logger.info(f"返回的 text 为：{resp.text}")
            



class Json:
    def __init__(self, resp: Response) -> None:
        k_logger.info("返回的是 json！")
        k_logger.info(f"返回的 json 为：\n{_json.dumps(resp.json(), indent=4)}")






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
        pass




def handle_resp(resp: Response):

    k_logger.info(f"状态码为：{resp.status_code} {resp.reason}")
    content_type = resp.headers.get('Content-Type')
    k_logger.info(f"响应的类型为：{content_type}")

    if content_type is not None:
        if ';' in content_type:
            content_type = content_type.split(';')[0]
        temp_data = content_type.split('/')
        sub = temp_data[0]
        subtype = temp_data[-1]

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




