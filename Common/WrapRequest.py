"""封装各种请求类"""

import requests
import requests_mock
import os
import json as _json
import random
from contextlib import ExitStack
from nb_log import simple_logger



class HttpRequest:
    def __init__(self, logger=simple_logger) -> None:
        
        self.logger = logger
        self.resp = None
        self.content_type = None

    def _prepare(self, **kwargs):
        """准备 HTTP 请求的参数。该方法检查传入的参数是否符合 HTTP 请求方法的要求，并记录日志。

        Args:
            **kwargs: 包含 HTTP 请求参数的字典。

        Raises:
            ValueError: 如果 GET 请求中传入了 data 或 json 参数，或者 POST 请求中传入了 params 参数，或者同时传入了 json 和 params 或 data 参数，将抛出此异常。

        Returns:
            None
        """
        arg_dict = locals()
        # print(arg_dict)
        arg_dict.pop('self')
        arg_dict = arg_dict['kwargs']

        # 待完善对传入参数的处理，params、data、json不能混用
        if kwargs['method'] == 'get' and (kwargs['data'] is not None or kwargs['json'] is not None):
            raise ValueError("get方法不能传data或json参数")
        elif kwargs['method'] == 'post' and kwargs['params'] is not None:
            raise ValueError("post方法不能传params参数")

        if kwargs['json'] is not None and (kwargs['params'] is not None or kwargs['data'] is not None):
            raise ValueError("json不能与params或data同时传")
        

        self.logger.warning("↓↓↓↓开始上传参数↓↓↓↓")

        # for i, (arg_key, arg_value) in enumerate(arg_dict.items()):
        #     output = "无"
        #     if arg_value is not None:
        #         if isinstance(arg_value, dict) or isinstance(arg_value, list):
        #             output = "\n" + _json.dumps(arg_value, indent=4)
        #         else:
        #             output = arg_value
        #     self.logger.info(f"{arg_key}为：" + output)

        self.logger.info("\n" + _json.dumps(arg_dict, indent=4))

        self.logger.warning("↑↑↑↑参数上传结束↑↑↑↑")

    def send_http(
        self,
        method: str,
        url: str,
        params: dict = None,
        data: dict = None,
        headers: dict = None,
        cookies: dict = None,
        json: dict = None,
        file_paths: list = None,
        auth: tuple = None,
        timeout: int = None,
        allow_redirects: bool = True,
        proxies=None,
        hooks=None,
        stream=False,
        verify=None,
        cert=None
    ) -> requests.Response:
        """ 重新定义了请求参数的顺序

        Args:
            method (str, optional): 请求方法
            url (str, optional): 请求地址
            params (dict, optional): 请求参数(get方法). 
            data (dict, optional): 请求数据，用于传输body内容(post方法)
            headers (dict, optional): 自定义请求头信息，其中字典的值必须为字符串类型. Defaults to None.
            cookies (dict, optional): 携带的cookie信息，其中字典的值必须为字符串类型. Defaults to None.
            json (dict, optional): JSON序列化后的内容，会自动设置 Content-Type: application/json 头部。只有当 data 为 None 时才能使用该参数. Defaults to None.
            file_paths (list, optional): 上传文件的本地路径. Defaults to None.
            auth (tuple, optional): 访问目标资源需要的认证信息，格式为元组 (username, password). Defaults to None.
            timeout (int, optional): 超时时间，单位为秒. Defaults to None.
            allow_redirects (bool, optional): 是否允许重定向. Defaults to True.
            proxies (_type_, optional): 指定使用代理服务器来连接远程服务器，字典的键为协议名称（http、https），值为代理服务器地址，格式为 {"http|https": "proxyurl"}. Defaults to None.
            hooks (_type_, optional): 注册的钩子函数，用于在请求前后执行自定义操作，常见的钩子函数有 response、download 和 upload. Defaults to None.
            stream (bool, optional): 是否以流式方式接收响应内容，默认为 False。如果为 True，将不会缓存响应体，而是直接从网络读取. Defaults to False.
            verify (_type_, optional): 是否验证 SSL 证书，默认为 True。如果为 False，将不会验证 SSL 证书，即使目标服务器使用了 HTTPS 协议。使用代理时，最好设置为false，避免 SSLError 错误。 Defaults to None.
            cert (_type_, optional): 指定客户端 SSL 证书，通常情况下不需要配置，因为 requests 会尝试使用系统默认的 CA 证书。如果配置，可以是单个证书文件或包含两个元素的元组（证书文件，私钥文件），用于验证目标服务器。
            
        Raises:
            e: _description_

        Returns:
            requests.Response: _description_
        """

        kwargs = locals()
        kwargs.pop('self')
        self.logger.debug("↓↓↓↓↓↓↓↓请求开始↓↓↓↓↓↓↓↓")
        self._prepare(**kwargs)


        # 用ExitStack来处理不确定数量的资源或对象
        with ExitStack() as stack:
            # 使用了or操作符来检查file_paths是否为None，如果是，则使用空列表[]代替，以避免触发异常
            # 假如file_paths为None, file_paths or []这个条件表达式判定为[], 因为None会被视为假(False), 所以files的值是一个空的字典
            # 对于requests的files参数, None或者{}都是不会报异常的
            files = {os.path.basename(fname): stack.enter_context(open(fname, 'rb')) for fname in file_paths or []}
            self.resp = requests.Session().request(
                method=method,
                url=url,
                params=params,
                data=data,
                headers=headers,
                cookies=cookies,
                files=files,
                auth=auth,
                timeout=timeout,
                allow_redirects=allow_redirects,
                proxies=proxies,
                hooks=hooks,
                stream=stream,
                verify=verify,
                cert=cert,
                json=json
            )

        self.handle_resp(self.resp)
        return self.resp
    
    def handle_resp(self) -> None:

        self.logger.warning("↓↓↓↓开始返回响应↓↓↓↓")
        try:
            self.logger.info(f"响应状态码为：{self.resp.status_code} {self.resp.reason}")
            self.content_type = self.resp.headers['Content-Type']
            self.logger.info(f"响应的类型为：{self.content_type}")

            if "application/json" in self.content_type:
                self.logger.info(f"返回的 json 为：\n{_json.dumps(self.resp.json(), indent=4)}")
            elif any(t in self.content_type for t in ["text/html", "text/plain", "application/xml", "application/xhtml+xml", "application/x-www-form-urlencoded"]):
                self.logger.info(f"返回的文本为：\n{self.resp.text}")
            elif any(t in self.content_type for t in ["text/csv", "application/pdf", "image/", "video/", "audio/"]):
                ...


        except Exception as e:
            if e.__class__ == requests.JSONDecodeError:
                self.logger.error(f"返回的 json 响应解析失败！{e.__doc__}")
            
            self.logger.info(f"返回的二进制数据为：{self.resp.content}")
            # nb_log.exception(e)
            raise e
        finally:
            self.logger.warning("↑↑↑↑响应返回结束↑↑↑↑")
            self.logger.debug("↑↑↑↑↑↑↑↑请求结束↑↑↑↑↑↑↑↑")
    
    
    
    

@requests_mock.Mocker(kw="mock", real_http=True)
def test_method_by_mock(data, headers, cookies, file_paths, **kwargs):

    http_req = HttpRequest()
    kwargs['mock'].register_uri("post", "https://whj.test", text="test mock!!", reason="ok", headers={"Content-Type": "text/plain"})
    res = http_req.send_http('post', "https://whj.test", None, data, headers, cookies, None, file_paths)




if __name__ == '__main__':
    # 生成32位随机字符串
    def randomString():
        str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        Random_device_ID = ""
        for i in range(32):
            id = int(round(random.random() * len(str)))
            Random_device_ID += str[id]
        return Random_device_ID

    device_id = randomString()
    response = requests.get(f"https://api2.immersivetranslate.com/big-model/get-token?deviceId={device_id}")
    token_data = response.json()
    print(token_data)
    # print(token_data['apiToken'])

    # pa = {'no': 1, 'name': 'Runoob'}
    # da = {"no": 1, "name": "Runoob"}
    # he = {"no": "haha", "name": "Runoob"}
    # co = {"no": "whj", "name": "Runoob"}
    # js = {"no": 1, "name": "Runoob"}
    # fi = ['d://temp/whj.txt', 'd://temp/tsl.txt']
    # example_1 = {'data': da, 'headers': he, 'cookies': co, 'file_paths': fi}
    # test_method_by_mock(**example_1)
    pass
