from monero.wallet import Wallet
from monero.exceptions import WrongAddress

from xmrbackers import config

def check_tx_key(tx_id, tx_key, wallet_address):
    try:
        check_data = {
            'txid': tx_id,
            'tx_key': tx_key,
            'address': wallet_address
        }
        w = Wallet(port=8000, user=config.XMR_WALLET_RPC_USER, password=config.XMR_WALLET_RPC_PASS)
        res = w._backend.raw_request('check_tx_key', check_data)
        return res
    except:
        raise Exception('there was a problem i dont feel like writing good code for right now')
