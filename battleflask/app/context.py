from db.in_memory_db_client import InMemoryDbClient

from battleapi.api.controller import GameControllerApi
from battleapi.api.persistence import GamePersistenceApi
from battleapi.utils.id_generator import Uuid4IdGenerator

IN_MEMORY_DB_CLIENT = InMemoryDbClient()
ID_GENERATOR = Uuid4IdGenerator()
GAME_PERSISTENCE_API = GamePersistenceApi(IN_MEMORY_DB_CLIENT)
GAME_CONTROLLER_API: GameControllerApi = GameControllerApi(
    persistence=GAME_PERSISTENCE_API, id_generator=ID_GENERATOR
)
