from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

app = Flask(__name__)
# Configure the database URI. Replace 'username', 'password', 'hostname', 'port', and 'database_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@hostname:port/database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<Item {self.name}>'

# Create the tables
db.create_all()

# Routes
@app.route('/items', methods=['GET', 'POST'])
def items():
    if request.method == 'GET':
        items = Item.query.all()
        result = [{'name': item.name, 'description': item.description} for item in items]
        return jsonify(result)
    elif request.method == 'POST':
        data = request.json
        new_item = Item(name=data['name'], description=data['description'])
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'message': 'Item created successfully'}), 201

@app.route('/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def single_item(item_id):
    item = Item.query.get_or_404(item_id)
    if request.method == 'GET':
        return jsonify({'name': item.name, 'description': item.description})
    elif request.method == 'PUT':
        data = request.json
        item.name = data.get('name', item.name)
        item.description = data.get('description', item.description)
        db.session.commit()
        return jsonify({'message': 'Item updated successfully'})
    elif request.method == 'DELETE':
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)