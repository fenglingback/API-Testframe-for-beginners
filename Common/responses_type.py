from requests import Response
from kuai_log import k_logger



class Download:
    def save_as_file(self, file_path):
        ...


class Text:
    def __init__(self, resp: Response, subtype) -> None:
        if subtype == 'plain':
            k_logger.info("返回的是纯文本！")
            k_logger.info(f"返回的 text 为：{resp.text}")
            




class Json:
    def __init__(self) -> None:
        print("this is json type!")


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




def handle_type(resp: Response):
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
            content = Json()
        elif subtype == 'octet-stream':
            content = OctetStream()
    elif sub == 'image':
        content = Image()
    else:
        raise Exception("not support type")
    return content




