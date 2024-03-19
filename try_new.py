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


if __name__ == '__main__':
    # try_locals = check_args(params=None, data='hhh', json=3)
    check_dict()
