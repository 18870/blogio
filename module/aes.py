import base64

from Crypto import Random
from Crypto.Cipher import AES

from module.config.config import config


# AESCoder
class AESCoder:
    def __init__(self, key):
        self.key = key
        # 数据块的大小  16位
        self.BS = 16
        # CBC模式 相对安全 因为有偏移向量 iv 也是16位字节的
        self.mode = AES.MODE_CBC
        # 填充函数 因为AES加密是一段一段加密的  每段都是BS位字节，不够的话是需要自己填充的
        self.pad = lambda s: s + (self.BS - len(s.encode()) % self.BS)*chr(self.BS - len(s.encode()) % self.BS)
        # 将填充的数据剔除
        self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    def encrypt(self, raw):
        raw = self.pad(raw).encode()
        # 随机获取iv
        iv = Random.new().read(AES.block_size)
        # 定义初始化
        cipher = AES.new(self.key, self.mode, iv)
        # 此处是将密文和iv一起 base64 解密的时候就可以根据这个iv来解密
        return base64.b64encode(iv + cipher.encrypt(raw)).decode()

    def decrypt(self, enc):
        # 先将密文进行base64解码
        enc = base64.b64decode(enc)
        # 取出iv值
        iv = enc[:self.BS]
        # 初始化自定义
        cipher = AES.new(self.key, self.mode, iv)
        # 返回utf8格式的数据
        return self.unpad(cipher.decrypt(enc[self.BS:])).decode()


aes = AESCoder(bytes(config.AES_KEY, encoding='utf-8'))