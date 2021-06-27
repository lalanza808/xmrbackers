from quart import Blueprint, jsonify


bp = Blueprint('api', 'api')

@bp.route('/api/test')
async def get_prices():
    return jsonify({
        'test': True,
        'message': 'This is only a test.'
    })
