from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from app.api.keys import mongopswd as pswd, mongousr as usr, mongoserver as server, mongoappname as appname

uri = f"mongodb+srv://{usr()}:{pswd()}@{server()}/?retryWrites=true&w=majority&appName={appname()}"
client = MongoClient(uri, server_api=ServerApi('1'))
database = client["Crypto2"]

database["cryptocurrencies"].create_index([('id', 1)], unique=False)
database["cryptocurrencies"].create_index([('symbol', 1)])
database["currencies"].create_index([('symbol', 1)])
