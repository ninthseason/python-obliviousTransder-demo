import pyDes
import binascii


class DesSecret:
    def __init__(self, key: str):
        self.KEY = key

    # 加密
    def des_en(self, text):
        iv = secret_key = self.KEY
        k = pyDes.des(secret_key, pyDes.CBC, iv, pad=None, padmode=pyDes.PAD_PKCS5)
        data = k.encrypt(text, padmode=pyDes.PAD_PKCS5)
        # data.进制返回文本字符串.解码字符串
        return binascii.b2a_hex(data).decode()

    # 解密
    def des_de(self, text):
        iv = secret_key = self.KEY
        k = pyDes.des(secret_key, pyDes.CBC, iv, pad=None, padmode=pyDes.PAD_PKCS5)
        data = k.decrypt(binascii.a2b_hex(text), padmode=pyDes.PAD_PKCS5)
        return data.decode()
