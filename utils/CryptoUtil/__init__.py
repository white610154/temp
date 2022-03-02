import jwt

key = '2c3d60951d544a8bf815c1b8485047da793d395fbee26c63c4f0f6c3d1d3ebe6'
algorithm = 'HS256'

def decode(token):
    deDict = jwt.decode(token, key, algorithms=[algorithm])
    return deDict