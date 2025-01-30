# SC -> server sends to client
# CS -> client sends to server

import json

class MessageFrame:
    def __init__(self, command_name: str, src: str, dest: str, data: str):
        self.command_name = command_name
        self.src = src
        self.dest = dest
        self.data = data

    @staticmethod
    def from_json(other_str: str) -> "MessageFrame":
        obj = json.loads(other_str)
        return MessageFrame(
            command_name=obj.get("command_name"),
            src=obj.get("src"),
            dest=obj.get("dest"),
            data=obj.get("data"),
        )
    
    def to_dict(self) -> dict:
        return {
            "command_name": self.command_name,
            "src": self.src,
            "dest": self.dest,
            "data": self.data,
        }
    
    def to_str(self):
        return json.dumps(self.to_dict())

CS_GET_RANKING = "CSGETRANKING"
SC_RANKING_DELIVER = "SCRANKINGDELIVER"

CS_GAME_INIT = "CSGAMEINIT"
SC_SUCCESS = "SCSUCCESS"
SC_FAILURE = "SCFAILURE"

SC_END_OF_GAME = "ENDOFGAME"

SC_REFRESH = "SCREFRESH"
CS_REFRESH = "CSREFRESH"