from flask import Flask, json
from flask import jsonify
from flask import request
from flask.helpers import make_response
from methods import Token, Restricted

app = Flask(__name__)
login = Token()
protected = Restricted()


# DB and Secret key config
app.config["DB"] = "bootcamp_tht"
app.config["DB_USER"] = "secret"
app.config["DB_PASSWORD"] = "noPow3r"
app.config["DB_ENDPOINT"] = "bootcamp-tht.sre.wize.mx"
app.config["JWT_SECRET"] = "my2w7wjd7yXF64FIADfJxNs1oupTGAuW"

# Just a health check


@app.route("/")
def url_root():
    return "OK"


# Just a health check
@app.route("/_health")
def url_health():
    return jsonify({"status": "OK", 'data': 12})


# e.g. http://127.0.0.1:8000/login
@app.route("/login", methods=['POST'])
def url_login():
    username = request.form['username']
    password = request.form['password']
    res = {
        "data": login.generate_token(username, password)
    }
    if not res["data"]:
        return make_response("Invalid credentials", 403)

    return jsonify(res)


# # e.g. http://127.0.0.1:8000/protected
@app.route("/protected")
def url_protected():
    auth_token = request.headers.get('Authorization')
    res = {
        "data": protected.access_data(auth_token)
    }
    if not res["data"]:
        return make_response("Unauthenticated", 403)
    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
