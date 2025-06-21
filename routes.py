
from flask import Blueprint, request, jsonify
lead_routes = Blueprint('lead_routes', __name__)
@lead_routes.route('/leads', methods=['POST'])
def create_lead():
    data = request.json
    return jsonify({'message': 'Lead recebido', 'data': data})
