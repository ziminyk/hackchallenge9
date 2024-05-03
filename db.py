from flask_sqlalchemy import SQLAlchemy
import time

db = SQLAlchemy()

class User(db.Model):
  """
  User model 
  """
  __tablename__ = "user"
  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  name = db.Column(db.String, nullable = False)
  age = db.Column(db.Integer, nullable = False)

  def __init__(self, **kwargs):
    """
    Initializes a User object
    """
    self.name = kwargs.get("name", "")
    self.age = kwargs.get("age", 0)
    
  def serialize(self):
    """
    Serializes a User object
    """
    orderlist = Order.query.filter_by(user_id=self.id)
    orders = [
      {
        "id": order.id,
        "start_location": order.start_location,
        "end_location": order.end_location,
        "timestamp": order.timestamp,
        "price": order.price
      }
      for order in orderlist
    ]
    
    account = Account.query.filter_by(user_id=self.id).first()
    if (not account):
      accounts = ""
    else:  
      accounts = {
        {
          "id": account.id,
          "balance": account.balance,
          "transactions": account.transactions
        }
    }

    return {
      "id": self.id,
      "name": self.name,
      "age": self.age,
      "orders": orders,
      "account": accounts
    }


class Order(db.Model):
  """
  Order Model 
  """
  __tablename__ = "order"
  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  start_location = db.Column(db.String, nullable = False)
  end_location = db.Column(db.String, nullable = False)
  timestamp = db.Column(db.Integer, nullable=False)
  price = db.Column(db.Float, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  
  def __init__(self, **kwargs):
    """
    Initializes User object"""
    self.start_location = kwargs.get("start_location", "")
    self.end_location = kwargs.get("end_location", "")
    self.timestamp = time.time()
    self.price = kwargs.get("price", "")

  def serialize(self):
    """
    Serialize a Order object
    """
    return {
      "id": self.id,
      "start_location": self.start_location,
      "end_location": self.end_location,
      "timestamp": self.timestamp,
      "price": self.price,
      "user_id": self.user_id,
    }


class Account(db.Model):
  """
  Account model
  """
  __tablename__ = "account"
  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  balance = db.Column(db.Float, nullable = False)
  transactions = db.Column(db.String, nullable = False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  def __init__(self, **kwargs):
    """
    Initializes an Account object
    """
    self.balance = kwargs.get("balance", 0)
    self.transactions = kwargs.get("transactions", "")

  def serialize(self):
    """
    Serializes an Account object
    """
    
    return {
      "id": self.id,
      "balance": self.balance,
      "transactions": self.transactions,
      "user_id": self.user_id
    }

  