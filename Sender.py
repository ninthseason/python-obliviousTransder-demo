import json
import random

import rsa
import fastapi
import des

database = {
    '张三': '80',
    '李四': '50',
    '王五': '90'
}

pub_table = {}
pri_table = {}

for people in database:
    pub, pri = rsa.newkeys(256)
    pub_table.update({people: pub.save_pkcs1().decode()})
    pri_table.update({people: pri.save_pkcs1().decode()})

app = fastapi.FastAPI()


@app.get("/")
async def index():
    return pub_table


def generate_random_str(random_length=16):
    """
    生成一个指定长度的随机字符串
    """
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(random_length):
        random_str += base_str[random.randint(0, length)]
    return random_str


@app.post("/get")
async def get(encrypt_key: bytes = fastapi.File()):
    print(encrypt_key)
    table = {}
    for key in pri_table:
        pri_key = rsa.PrivateKey.load_pkcs1(pri_table[key].encode())
        try:
            des_key = rsa.decrypt(encrypt_key, pri_key).decode()
        except rsa.pkcs1.DecryptionError:
            des_key = generate_random_str(8)
        table.update({key: des_key})
    response = {}
    for i in database:
        print(table[i])
        des_factory = des.DesSecret(table[i])
        encrypt_res = des_factory.des_en(database[i])
        response.update({i: encrypt_res})
    return response
