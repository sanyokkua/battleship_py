import battleapi.api.dto as dto


class GameLogicController:
    def init_game_session(self) -> str:
        # TODO: implement
        return ''

    def create_player_in_session(self, session_id: str,
                                 player_name: str) -> dto.PlayerInfo:
        # TODO:
        player_id: str = ''  # TODO:
        self._join_game_session(session_id, player_id)
        return dto.PlayerInfo(player_name, player_id, session_id)

    def _join_game_session(self, session_id: str, player_id: str) -> None:
        # TODO: implement
        pass

    def get_opponent_prepare_status(self, session_id: str, current_player_id: str):
        return "READY"

    def get_prepare_ships_list(self, session_id: str, current_player_id: str):
        return []

    def get_prepare_player_field(self, session_id: str, current_player_id: str):
        return [[]]

    def get_opponent(self, session_id: str,
                     current_player_id: str) -> dto.PlayerInfo:
        pl = self.get_player_by_id(session_id, 'player_id')
        return pl

    def get_active_player(self, session_id: str) -> dto.PlayerInfo:
        pass

    def get_player_by_id(self, session_id: str, player_id: str) -> dto.PlayerInfo:
        # TODO:
        return dto.PlayerInfo("NAME", player_id, session_id)

    def get_number_of_cells_left(self, session_id: str, player_id: str) -> int:
        pass

    def get_field(self, session_id: str, player_id: str, is_for_opponent: bool = False) -> list[list]:
        pass

    def get_winner(self, session_id: str) -> dto.PlayerInfo:
        pass

    def add_ship_to_field(self, session_id, cookies_player_id, ship_type, param,
                          ship_direction):
        pass

    def remove_ship_from_field(self, session_id, cookies_player_id, param):
        pass

    def start_game(self, session_id):
        pass

    def make_shot(self, session_id, cookies_player_id, param):
        pass


