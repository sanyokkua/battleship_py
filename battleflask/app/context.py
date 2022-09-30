from battleapi.api.controller_api import ControllerApi
from battleapi.api.persistance_api import PersistenceApi
from battleapi.implementations.id_generator import Uuid4IdGenerator
from battleapi.implementations.in_memory_db_client import InMemoryDbClient

IN_MEMORY_DB_CLIENT = InMemoryDbClient()
ID_GENERATOR = Uuid4IdGenerator()
PERSISTENCE_API = PersistenceApi(IN_MEMORY_DB_CLIENT)
GAME_CONTROLLER: ControllerApi = ControllerApi(
    persistence=PERSISTENCE_API, id_generator=ID_GENERATOR
)
