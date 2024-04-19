"""封装各种请求类"""

import requests
import requests_mock
import os
import json as _json
from contextlib import ExitStack
from kuai_log import k_logger
from ResponsesType import handle_type


class HttpRequest:

    def __init__(self) -> None:
        pass

    def _prepare(self, **kwargs):
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
        

        k_logger.warning("↓↓↓↓开始上传参数↓↓↓↓")

        # for i, (arg_key, arg_value) in enumerate(arg_dict.items()):
        #     output = "无"
        #     if arg_value is not None:
        #         if isinstance(arg_value, dict) or isinstance(arg_value, list):
        #             output = "\n" + _json.dumps(arg_value, indent=4)
        #         else:
        #             output = arg_value
        #     k_logger.info(f"{arg_key}为：" + output)

        k_logger.info("\n" + _json.dumps(arg_dict, indent=4))

        k_logger.warning("↑↑↑↑参数上传结束↑↑↑↑")

    def send_http(
        self,
        method,
        url,
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
        """重新定义了请求参数的顺序
        :param method: 请求方法
        :param url: 请求地址
        :param params: 请求参数(get方法)
        :param data: 请求数据，用于传输body内容(post方法)，
        :param headers: 自定义请求头信息，其中字典的值必须为字符串类型
        :param cookies: 携带的cookie信息，其中字典的值必须为字符串类型
        :param json: JSON序列化后的内容，会自动设置 Content-Type: application/json 头部。只有当 data 为 None 时才能使用该参数
        :param file_paths: 上传文件的本地路径
        :param auth: 访问目标资源需要的认证信息，格式为元组 (username, password)
        :param timeout: 超时时间，单位为秒
        :param allow_redirects: 是否允许重定向
        :param proxies: 指定使用代理服务器来连接远程服务器，字典的键为协议名称（http、https），值为代理服务器地址，格式为 {"http|https": "proxyurl"}
        :param hooks: 注册的钩子函数，用于在请求前后执行自定义操作，常见的钩子函数有 response、download 和 upload
        :param stream: 是否以流式方式接收响应内容，默认为 False。如果为 True，将不会缓存响应体，而是直接从网络读取
        :param verify: 是否验证 SSL 证书，默认为 True。如果为 False，将不会验证 SSL 证书，即使目标服务器使用了 HTTPS 协议
        :param cert: 指定客户端 SSL 证书，通常情况下不需要配置，因为 requests 会尝试使用系统默认的 CA 证书。
                     如果配置，可以是单个证书文件或包含两个元素的元组（证书文件，私钥文件），用于验证目标服务器。
        """

        kwargs = locals()
        kwargs.pop('self')
        k_logger.warning("↓↓↓↓↓↓↓↓请求开始↓↓↓↓↓↓↓↓")
        self._prepare(**kwargs)

        # 用ExitStack来处理不确定数量的资源或对象
        with ExitStack() as stack:
            # 使用了or操作符来检查file_paths是否为None，如果是，则使用空列表[]代替，以避免触发异常
            # 假如file_paths为None, file_paths or []这个条件表达式判定为[], 因为None会被视为假(False), 所以files的值是一个空的字典
            # 对于requests的files参数, None或者{}都是不会报异常的
            files = {os.path.basename(fname): stack.enter_context(open(fname, 'rb')) for fname in file_paths or []}
            resp = requests.Session().request(
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

        self._handle_resp(resp=resp)
        k_logger.warning("↑↑↑↑↑↑↑↑请求结束↑↑↑↑↑↑↑↑")
        return resp

    def _handle_resp(self, resp: requests.Response):
        k_logger.warning("↓↓↓↓开始返回响应↓↓↓↓")
        k_logger.info(f"状态码为：{resp.status_code} {resp.reason}")

        handle_type(resp)

        k_logger.warning("↑↑↑↑响应结束↑↑↑↑")




http_req = HttpRequest()


@requests_mock.Mocker(kw="mock", real_http=True)
def test_method_by_mock(data, headers, cookies, file_paths, **kwargs):
    kwargs['mock'].register_uri("post", "https://whj.test", text="test mock!!", reason="ok", headers={"Content-Type": "text/plain"})
    res = http_req.send_http('post', "https://whj.test", None, data, headers, cookies, None, file_paths)




if __name__ == '__main__':

    pa = {'no': 1, 'name': 'Runoob'}
    da = {"no": 1, "name": "Runoob"}
    he = {"no": "haha", "name": "Runoob"}
    co = {"no": "whj", "name": "Runoob"}
    js = {"no": 1, "name": "Runoob"}
    fi = ['d://temp/whj.txt', 'd://temp/tsl.txt']
    test_method_by_mock(data=da, headers=he, cookies=co, file_paths=fi)
