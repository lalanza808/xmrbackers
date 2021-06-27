from datetime import datetime

from quart import Blueprint, current_app


bp = Blueprint('filters', 'filters')


@bp.app_template_filter('ts')
def from_ts(v):
    return datetime.fromtimestamp(v)

@bp.app_template_filter('xmr_block_explorer')
def xmr_block_explorer(v):
    return f'https://www.exploremonero.com/transaction/{v}'
