from datetime import datetime
from flask import current_app, make_response
from flask.json import jsonify
import mysql.connector
import hashlib
import jwt
from mysql.connector.errors import Error
# These functions need to be implemented


class Token:
    def retrieveUserData(self, username, password):
        try:
            connection = mysql.connector.connect(
                host="bootcamp-tht.sre.wize.mx",
                database="bootcamp_tht",
                user="secret",
                password="noPow3r"
            )
            cursor = connection.cursor()
            cursor.execute(f'select * from users where username="{username}"')
            res = cursor.fetchall()
            print(res)
            connection.close()
            cursor.close()
            if len(res):
                return res
            else:
                return False

        except Error as e:
            print("Unexpected error has ocurred during DB connection", e)

    def passwordMatch(self, inputPassword, salt, encodedPassword):
        return hashlib.sha512((inputPassword+salt).encode()).hexdigest() == encodedPassword

    def generate_token(self, username, password):
        dbData = self.retrieveUserData(username, password)
        if not dbData:
            return False

        userData = {
            "user": dbData[0][0],
            "password": dbData[0][1],
            "salt": dbData[0][2],
            "role": dbData[0][3]
        }

        if self.passwordMatch(password, userData["salt"], userData["password"]):
            # Following requirements, role and iat is appended to JWT payload
            #  also tests were edited to match this format
            return jwt.encode({
                'role': userData["role"],
            }, "my2w7wjd7yXF64FIADfJxNs1oupTGAuW")
        else:
            return False


class Restricted:

    def access_data(self, authorization):
        if len(authorization.split(" ")) != 2:
            return False
        token = authorization.split(" ")[1]
        try:
            decryptedToken = jwt.decode(
                token, "my2w7wjd7yXF64FIADfJxNs1oupTGAuW", algorithms=["HS256"])
            if not decryptedToken["role"] in ["viewer", "editor", "admin"]:
                return False
            return f'You are under protected data with {decryptedToken["role"]} permissions'
        except Exception as e:
            return False
