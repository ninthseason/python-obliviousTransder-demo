import des
import rsa
import httpx

des_key = 'justakey'
des_factory = des.DesSecret(des_key)

people = input('请输入要查询的人名: 张三|李四|王五:\n')
table = httpx.get("http://127.0.0.1:8000").json()
pub_key = table[people]
pub_key = rsa.PublicKey.load_pkcs1(pub_key.encode())
des_key_encrypt = rsa.encrypt(des_key.encode(), pub_key)
url = f'http://127.0.0.1:8000/get'
res = httpx.post(url, files={'encrypt_key': des_key_encrypt}).json()

result_table = {}
for i in res:
    result_table.update({i: des_factory.des_de(res[i])})

print(result_table)
