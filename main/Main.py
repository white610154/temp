import jwt
import base64

key = 'auo'
algorithm = 'HS256'

if __name__ == "__main__":

    token = 'eyJ0eXAiOiJhdW8iLCJhbGciOiJIUzI1NiJ9.eyJwcm9qZWN0IjoxLCJleHBlcmltZW50IjoxfQ.w_3oT1ZydG3gFzGURyKnf3uethembV_RV4VuuNbMyUs'
    deDict = jwt.decode(token, key, algorithms=algorithm, options={"verify_signature": False})
    print(deDict)