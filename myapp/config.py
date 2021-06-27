from dotenv import load_dotenv
from secrets import token_urlsafe
from os import getenv


load_dotenv()

# Site meta
SITE_NAME = getenv('SITE_NAME', 'MyApp')
SECRET_KEY = getenv('SECRET_KEY')
STATS_TOKEN = getenv('STATS_TOKEN', token_urlsafe(8))
SERVER_NAME = getenv('SERVER_NAME', 'localhost:5000')

# Crypto RPC
XMR_WALLET_PASS = getenv('XMR_WALLET_PASS')
XMR_WALLET_RPC_USER = getenv('XMR_WALLET_RPC_USER')
XMR_WALLET_RPC_PASS = getenv('XMR_WALLET_RPC_PASS')
XMR_WALLET_RPC_ENDPOINT = getenv('XMR_WALLET_RPC_ENDPOINT')
XMR_DAEMON_URI = getenv('XMR_DAEMON_URI')

# Database
DB_HOST = getenv('DB_HOST', 'localhost')
DB_PORT = getenv('DB_PORT', 5432)
DB_NAME = getenv('DB_NAME', 'myapp')
DB_USER = getenv('DB_USER', 'myapp')
DB_PASS = getenv('DB_PASS')

# Redis
REDIS_HOST = getenv('REDIS_HOST', 'localhost')
REDIS_PORT = getenv('REDIS_PORT', 6379)

# Development
TEMPLATES_AUTO_RELOAD = True
