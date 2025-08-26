from flask import Blueprint, jsonify, request
from application import gl, ap, ar, inventory

bp = Blueprint('integration', __name__)


@bp.get('/gl')
def get_gl():
    return jsonify(gl.summary())


@bp.post('/ap')
def post_ap():
    data = request.get_json() or {}
    ap.record_bill(data.get('vendor', ''), float(data.get('amount', 0)))
    return jsonify({'status': 'ok'})


@bp.post('/ar')
def post_ar():
    data = request.get_json() or {}
    ar.record_invoice(data.get('customer', ''), float(data.get('amount', 0)))
    return jsonify({'status': 'ok'})


@bp.post('/inventory')
def post_inventory():
    data = request.get_json() or {}
    inventory.add_item(data.get('name', ''), int(data.get('quantity', 0)))
    return jsonify({'status': 'ok'})
