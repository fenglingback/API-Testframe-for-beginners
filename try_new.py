"""代码的一些新尝试"""

from kuai_log import k_logger


def check_args(params, data, json):
    w = 8
    arguments = locals()
    h = 10
    j = 6

    arguments.pop('w')
    print(arguments)


def check_dict():
    # 创建一个字典
    example_dict = {1: 'a', 2: 'b', 3: 'c', 4: {'w': 21, 'h': 44}}

    # 使用items()方法遍历字典的键和值
    for i, (key, value) in enumerate(example_dict.items(), start=1):
        print(i, key, value)



def derector_log(func):
    def wrapper(**kwargs):
        args = locals()
        args.pop('func')
        print(args)
        end_args = args['kwargs']
        print(end_args)
        for i, (arg_key, arg_value) in enumerate(end_args.items(), start=1):
            if arg_value is not None:
                output = str(arg_value)
            k_logger.info(f"{arg_key}为：" + output)
        return func(**kwargs)
    return wrapper


@derector_log
def hhh(a=None, b=None, c=None, d=None):
    e = 3
    print(e)
    return f"val = {e}"


if __name__ == '__main__':
    # try_locals = check_args(params=None, data='hhh', json=3)
    hhh(a=1, b=2, c=4)
