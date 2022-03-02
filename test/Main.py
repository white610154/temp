import jwt

algorithm = ['HS256']
secret = 'auo'

if __name__ == "__main__":

    encodedJwt = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwcm9qZWN0IjoxLCJleHBlcmltZW50IjoxfQ.bmXAqoMMAvCx0tXFWa37iaUCy2-XDgU9sf4bGawIP1o'
    decodedJwt = jwt.decode(encodedJwt, secret, algorithms=algorithm)
    print(decodedJwt)