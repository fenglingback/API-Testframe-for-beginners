"""封装各种请求类"""

import requests
import requests_mock
import json as _json
from contextlib import ExitStack
from kuai_log import k_logger


class HttpRequest:

    def __init__(self) -> None:
        pass

    def _prepare(
        self,
        method,
        url,
        params: dict = None,
        data: dict = None,
        headers: dict = None,
        cookies: dict = None,
        json: dict = None,
        file_paths: list = None
    ):
        arg_dict = locals()
        arg_dict.pop('self')
        # arg_dict.pop('method')
        # arg_dict.pop('url')

        k_logger.warning("↓↓↓↓↓↓↓↓请求开始↓↓↓↓↓↓↓↓")
        k_logger.warning("↓↓↓↓开始上传参数↓↓↓↓")
        # k_logger.info(f"method为: {method}")
        # k_logger.info(f"url为: {url}")

        print(arg_dict.items())
        for i, (arg_key, arg_value) in enumerate(arg_dict.items()):
            output = "无"
            if arg_value is not None:
                output = "\n" + _json.dumps(arg_value, indent=4)
            k_logger.info(f"{arg_key}为：" + output)

        k_logger.warning("↑↑↑↑参数上传结束↑↑↑↑")

    def send_http(
        self,
        method,
        url,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        json=None,
        file_paths: list = None,
        auth=None,
        timeout=None,
        allow_redirects: bool = True,
        proxies=None,
        hooks=None,
        stream=False,
        verify=None,
        cert=None
    ):
        """重新定义了请求参数的顺序
        Args:
            method (_type_): _请求方法_
            url (_type_): _请求url_
            params (_type_): _get请求传入参数_
            data (_type_): _post请求传入参数_
            headers (_type_): _请求头_
            cookies (_type_): _携带的cookies_
            json (_type_): _携带的json_
            file_paths (_type_): _上传文件的绝对路径_
            auth (_type_): _description_
            timeout (_type_): _description_
            allow_redirects (bool): _description_
            proxies (_type_): _description_
            hooks (_type_): _description_
            stream (_type_): _description_
            verify (_type_): _description_
            cert (_type_): _description_
        """
        self._prepare(method, url, params, data,
                      headers, cookies, json, file_paths)

        # 用ExitStack来处理不确定数量的资源或对象
        with ExitStack() as stack:
            # 使用了or操作符来检查file_paths是否为None，如果是，则使用空列表[]代替，以避免触发异常
            # 假如file_paths为None, file_paths or []这个条件表达式判定为[], 因为None会被视为假(False), 所以files的值是一个空的字典
            # 对于requests的files参数, None或者{}都是不会报异常的
            files = {fname: stack.enter_context(
                open(fname, 'rb')) for fname in file_paths or []}
            res = requests.request(
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

        self._handle_resp(resp=res)
        k_logger.warning("↑↑↑↑↑↑↑↑请求结束↑↑↑↑↑↑↑↑")
        return res

    def _handle_resp(self, resp: requests.Response):
        k_logger.warning("↓↓↓↓开始返回响应↓↓↓↓")
        k_logger.info(f"状态码为：{resp.status_code} {resp.reason}")
        k_logger.warning("↑↑↑↑响应结束↑↑↑↑")


http_req = HttpRequest()


@requests_mock.Mocker(kw="mock", real_http=True)
def test_mock(**kwargs):
    kwargs['mock'].get("https://whj.test", text="test mock!!", reason="ok")
    res = http_req.send_http('get', "https://whj.test")
    print(res.text)


if __name__ == '__main__':

    # h = HttpRequest()
    # pa = {'no': 1, 'name': 'Runoob'}
    # da = {"no": 1, "name": "Runoob"}
    # he = {"no": 1, "name": "Runoob"}
    # co = {"no": 1, "name": "Runoob"}
    # js = {"no": 1, "name": "Runoob"}
    # fi = ['c://whj/hhh.txt', 'd://cxfl/www.json', 'e://fl/jjb.sass']
    test_mock()
