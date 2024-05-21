from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb+srv://Trip:1234@cluster0.jx5papz.mongodb.net/')
db = client['sensors_db']
collection = db['sensors']

# Create a new document in MongoDB
@app.route('/api/create', methods=['POST'])
def create_document():
    data = request.json
    result = collection.insert_one(data)
    return jsonify({'message': 'Document created successfully', 'id': str(result.inserted_id)}), 201

# Get all documents from MongoDB
@app.route('/api/read', methods=['GET'])
def get_all_documents():
    documents = []
    for doc in collection.find():
        documents.append({
            'id': str(doc['_id']),
            'sensor_id': doc['sensor_id'],
            'description': doc['description'],
            'location': doc['location'],
            'type': doc['type'],
            'status': doc['status']
          
        })
    return jsonify(documents)

# Get a specific document by ID from MongoDB
@app.route('/api/read/<string:document_id>', methods=['GET'])
def get_document(document_id):
    doc = collection.find_one({'_id': ObjectId(document_id)})
    if doc:
        return jsonify({
            'id': str(doc['_id']),
            'name': doc['name'],
            'age': doc['age']
        })
    else:
        return jsonify({'message': 'Document not found'}), 404

# Update a document in MongoDB
@app.route('/api/update/<string:document_id>', methods=['PUT'])
def update_document(document_id):
    data = request.json
    result = collection.update_one({'_id': ObjectId(document_id)}, {'$set': data})
    if result.modified_count > 0:
        return jsonify({'message': 'Document updated successfully'})
    else:
        return jsonify({'message': 'Document not found'}), 404

# Delete a document from MongoDB
@app.route('/api/delete/<string:document_id>', methods=['DELETE'])
def delete_document(document_id):
    result = collection.delete_one({'_id': ObjectId(document_id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'Document deleted successfully'})
    else:
        return jsonify({'message': 'Document not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)