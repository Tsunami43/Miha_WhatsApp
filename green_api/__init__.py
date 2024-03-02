from utils import config
from .api import GreenApi

instance = GreenApi(
    idInstance=config.get('GreenAPI', 'id_instance'),
    apiTokenInstance=config.get('GreenAPI', 'api_token')
)