from battleapi.api.controller import GameControllerApi
from battleapi.api.persistence import GamePersistenceApi
from battleapi.utils.id_generator import Uuid4IdGenerator
from db.in_memory_db_client import InMemoryDbClient

IN_MEMORY_DB_CLIENT = InMemoryDbClient()
ID_GENERATOR = Uuid4IdGenerator()
PERSISTENCE_API = GamePersistenceApi(IN_MEMORY_DB_CLIENT)
GAME_CONTROLLER: GameControllerApi = GameControllerApi(
    persistence=PERSISTENCE_API, id_generator=ID_GENERATOR
)
