class Text:
    def __init__(self, subtype) -> None:
        print("this is text type!")



class Json:
    ...


class Image:
    ...


class OctetStream:
    ...


def pipei_type(sub, subtype):
    if sub == 'text':
        return Text(subtype)
    elif sub == 'application':
        if subtype == 'json':
            return Json()
        elif subtype == 'octet-stream':
            return OctetStream()
    elif sub == 'image':
        return Image()
    else:
        raise Exception("not support type")


if __name__ == '__main__':
    ...
