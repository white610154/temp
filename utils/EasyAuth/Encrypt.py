import hashlib
import json
from Crypto.Cipher import AES
import jwt

secret = 'auomamc84149738k'

BLOCK_SIZE = 16

def pad(s: bytes) -> bytes:
    return s + bytes(BLOCK_SIZE - len(s) % BLOCK_SIZE)

def aes_encode(text: str) -> str:
    aes = AES.new(secret.encode('utf-8'), AES.MODE_ECB)
    return aes.encrypt(pad(text.encode('utf-8'))).hex()

def aes_decode(code: str) -> str:
    aes = AES.new(secret.encode('utf-8'), AES.MODE_ECB)
    return aes.decrypt(bytes.fromhex(code)).rstrip(b'\x00').decode('utf-8')

def sha1_encode(text: str) -> str:
    return hashlib.sha1(text.encode('utf-8')).hexdigest()

def jwt_encode(payload):
    code = jwt.encode(payload, secret, algorithm='HS256')
    return code

def jwt_decode(token: str):
    payload = jwt.decode(token, secret, algorithms=['HS256'])
    return payload
