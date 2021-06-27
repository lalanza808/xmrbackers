from quart import Blueprint, render_template


bp = Blueprint('meta', 'meta')

@bp.route('/')
async def index():
    return await render_template('index.html')
