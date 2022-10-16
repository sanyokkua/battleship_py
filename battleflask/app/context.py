"""Context module. Has public constants."""
import battleapi.abstract as abstract
import battleapi.api.controller as controller
import battleapi.api.persistence as persistence
import battleapi.db.in_memory_db_client as db_client
import battleapi.utils.id_generator as id_generator

IN_MEMORY_DB_CLIENT: abstract.DbClient = db_client.InMemoryDbClient()
ID_GENERATOR: abstract.IdGenerator = id_generator.Uuid4IdGenerator()
PERSISTENCE_API: abstract.GamePersistence = persistence.GamePersistenceApi(
    IN_MEMORY_DB_CLIENT
)
GAME_API: abstract.GameController = controller.GameControllerApi(
    persistence=PERSISTENCE_API, id_generator=ID_GENERATOR
)
