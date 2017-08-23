# __*__ coding: utf-8 __*__
import hashlib


def get_md5(url):
    #in python3  str==unicode
    if isinstance(url, str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)

    return m.hexdigest()

if __name__ == '__main__':
    print(get_md5('www.baidu.com'))