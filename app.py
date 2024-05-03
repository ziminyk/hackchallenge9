import json
from db import db
from db import User
from db import Order
from db import Account
from flask import Flask, request

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

def success_request(data, code = 200):
    return json.dumps(data), code

def failure_request(message, code = 404):
    return json.dumps({"error": message}), code

@app.route("/api/users/")
def get_users():
    """
    Endpoint for getting all users
    """
    user = [users.serialize() for users in User.query.all()]
    return success_request({"users": user})

@app.route("/api/users/<int:user_id>/")
def get_account(user_id):
    """
    Endpoint for getting an account by id
    """
    account = Account.query.filter_by(id=user_id).first()
    if account == None:
        return failure_request("Account was not found.")
    return success_request(account.serialize())

@app.route("/api/users/", methods=["POST"])
def create_user():
    """
    Endpoint for creating a new user
    """
    body = json.loads(request.data)
    if body == None:
        return failure_request("Empty body", 400)
    name = body.get("name")
    age = body.get("age")
    
    if (name == None or age == None or account == None):
        return failure_request("name or age is incomplete", 400)
    if (type(name) != str or type(age) != int):
        return failure_request("The datatypes are incorrect", 400)
    newUser = User(name = name, age = age) 
    db.session.add(newUser)
    db.session.commit()
    return success_request(newUser.serialize(), 201)

@app.route("/api/users/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    """
    Endpoint for deleting a user by id
    """
    user = User.query.filter_by(id = user_id).first()
    if user == None:
        return failure_request("user was not found.")
    db.session.delete(user)
    db.session.commit()
    return success_request(user.serialize(), 200)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)



