from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS
from dotenv import load_dotenv

from funtion_jwt import validate_token
from routes.auth import routes_auth
from bson import ObjectId

# Instantiation
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/pythonreactdb'
mongo = PyMongo(app)

# Settings
CORS(app)

# Database
db = mongo.db.users

app.register_blueprint(routes_auth, url_prefix="/api")

#@app.before_request
def verify_token_middleware():
    print('entro al validator')
    token = request.headers['Autorization'].split(" ")[1]
    validate_token(token, output=False)
      
# Routes
@app.route('/users', methods=['POST'])
def createUser():
  print(request.json)
  id = db.insert_one({
    'name': request.json['name'],
    'email': request.json['email'],
    'password': request.json['password']
  })
  return jsonify(str(ObjectId(id)))


@app.route('/users', methods=['GET'])
def getUsers():
    users = []
    for doc in db.find():
        users.append({
            '_id': str(ObjectId(doc['_id'])),
            'name': doc['name'],
            'email': doc['email'],
            'password': doc['password']
        })
    return jsonify(users)

@app.route('/users/<id>', methods=['GET'])
def getUser(id):
  user = db.find_one({'_id': ObjectId(id)})
  print(user)
  return jsonify({
      '_id': str(ObjectId(user['_id'])),
      'name': user['name'],
      'email': user['email'],
      'password': user['password']
  })


@app.route('/users/<id>', methods=['DELETE'])
def deleteUser(id):
  db.delete_one({'_id': ObjectId(id)})
  return jsonify({'message': 'User Deleted'})

@app.route('/users/<id>', methods=['PUT'])
def updateUser(id):
  print(request.json)
  db.update_one({'_id': ObjectId(id)}, {"$set": {
    'name': request.json['name'],
    'email': request.json['email'],
    'password': request.json['password']
  }})
  return jsonify({'message': 'User Updated'})

if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True)