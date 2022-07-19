from datetime import datetime
import json
import math
import os
from typing import Dict, List
from . import Encrypt, Functions

AUTH_STORAGE_PATH = '.salaauth'

def serialize_dict(d: dict) -> str:
    return Encrypt.aes_encode(json.dumps(d))

def deserialize_dict(c: str) -> dict:
    return json.loads(Encrypt.aes_decode(c))

class Auth:
    admin = 'admin'
    maintainer = 'maintainer'
    owner = 'owner'
    user = 'user'
    auomaintainer = 'auomaintainer'

    @staticmethod
    def rationalize(authName: str) -> str:
        '''
        Make auth reasonable, admin should not been set.
        '''
        if authName in [Auth.admin, Auth.auomaintainer]:
            return Auth.user
        return authName

    @staticmethod
    def higher_than(a: str, b: str) -> bool:
        '''
        (auomaintainer) > admin > maintainer > owner > user
        '''
        if a == Auth.auomaintainer: return True
        if b == Auth.auomaintainer: return False
        if a == Auth.admin: return True
        if b == Auth.admin: return False
        if a == Auth.maintainer: return True
        if b == Auth.maintainer: return False
        if a == Auth.owner: return True
        if b == Auth.owner: return False
        if a == Auth.user: return True
        if b == Auth.user: return False
        return False

class User:
    def __init__(self, id: int, username: str, password: str):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'User(id={self.id}, username={self.username}, password={self.password}'

    def serialize(self) -> str:
        '''
        Serialize user to string.
        '''
        userCode = serialize_dict({
            'id': self.id,
            'username': self.username,
            'password': self.password,
        })
        return userCode

    @classmethod
    def deserialize(cls, code: str):
        return User(**deserialize_dict(code))

    def generate_token(self, iat: datetime) -> str:
        token = Encrypt.jwt_encode({
            'username': self.username,
            'iat': math.floor(iat.timestamp())
        })
        return token

class AuthGroup:
    def __init__(self, name: str):
        self.name = name
        self.auths = {}

    def __repr__(self):
        return f'Group(name={self.name}, auths={self.auths}'

    def add_user(self, username: str, auth: str):
        self.auths[username] = Auth.rationalize(auth)

    def remove_user(self, username: str):
        if self.auths.get(username):
            del self.auths[username]

    def auth_of(self, username: str) -> str:
        '''
        find auth of user in group, maintainer has auth only if it is an owner or user.
        '''
        if Auth.higher_than(username, Auth.admin):
            return username
        return self.auths.get(username)

    def serialize(self) -> str:
        '''
        Serialize group auths to string.
        '''
        groupCode = serialize_dict(self.auths)
        return groupCode

    @classmethod
    def deserialize(cls, name: str, code: str):
        group = cls(name)
        group.auths = Encrypt.aes_decode(code)
        return group

class EasyAuthService:
    catalog = {
        Auth.auomaintainer: 0,
        Auth.admin: 1
    }
    users: List[User] = [
        User(0, Auth.auomaintainer, Encrypt.sha1_encode('auo@84149738')),
        User(1, Auth.admin, Encrypt.sha1_encode('admin'))
    ]
    auths: Dict[str, AuthGroup] = {}

    @classmethod
    def init(cls):
        'Sync data and storage on start'
        if not os.path.isfile(AUTH_STORAGE_PATH):
            cls.save()
            return

        with open(AUTH_STORAGE_PATH, 'r') as fin:
            storage = fin.read()
            if storage == '':
                cls.save()
                return

            data = json.loads(storage)
            cls.catalog = deserialize_dict(data['catalog'])
            for id, userCode in data['users'].items():
                cls.append_user_list(int(id), User.deserialize(userCode))
            cls.auths = {name: AuthGroup.deserialize(name, authCode) for name, authCode in data['auths'].items()}

    @classmethod
    def show(cls):
        print(cls.catalog)
        print(cls.users)
        print(cls.auths)

    @classmethod
    def add_user(cls, username, password) -> int:
        '''
        Add new user and return userId.
            Parameters:
                username (str): unique username
                password (str): raw password string, will be encrypted
                auth (str): role of user, value other than Auth members will be invalid
            Returns:
                id (int): id of the new user, 0 if failed
        '''
        if username in cls.catalog.keys(): return 0

        id = len(cls.users)
        user = User(id, username, Encrypt.sha1_encode(password))
        cls.append_user_list(id, user)

        cls.save()
        return id

    @classmethod
    def append_user_list(cls, id: int, user: User):
        if len(cls.users) <= id:
            cls.users += [None] * (id - len(cls.users) + 1)
        cls.users[id] = user
        cls.catalog[user.username] = id

    @classmethod
    def remove_user(cls, username: str):
        id = cls.catalog[username]
        del cls.catalog[username]
        cls.users[id] = None

        for group in cls.auths.values():
            group.remove_user(username)

        cls.save()

    @classmethod
    def add_group(cls, name: str, owner: str):
        group = AuthGroup(name)
        group.add_user(owner, Auth.owner)
        cls.auths[name] = group

        cls.save()

    @classmethod
    def remove_group(cls, name: str):
        del cls.auths[name]

        cls.save()

    @classmethod
    def group(cls, name: str) -> AuthGroup:
        group = cls.auths.get(name)
        if group == None:
            return AuthGroup('unknown')
        return group

    @classmethod
    def login(cls, username: str, password: str):
        id = cls.catalog[username]
        user = cls.users[id]
        if Encrypt.sha1_encode(password) == user.password:
            return user
        return None

    @classmethod
    def authorize(cls, token: str) -> User:
        userInfo = Encrypt.jwt_decode(token)
        timeValid = Functions.check_valid_time(userInfo['iat'])
        if not timeValid: return

        return cls.users[cls.catalog[userInfo['username']]]

    @classmethod
    def check_auth(cls, username: str, auth: str, groupName: str=None) -> bool:
        if Auth.higher_than(username, Auth.maintainer):
            return True
        if groupName != None:
            return Auth.higher_than(cls.auths[groupName].auths[username], auth)
        else:
            return Auth.higher_than(username, auth)

    @classmethod
    def save(cls):
        with open(AUTH_STORAGE_PATH, 'w') as fout:
            data = {
                'catalog': serialize_dict(cls.catalog),
                'users': {i: user.serialize() for i, user in enumerate(cls.users)},
                'auths': {name: group.serialize() for name, group in cls.auths.items()},
            }
            json.dump(data, fout, indent=2)

EasyAuthService.init()
