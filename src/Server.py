from Receiver import ReceiverMqtt
from Sender import SenderMqtt
from namespace import *
import time
from utils import *
from commands import *
from GameScripts.GameMain import game
import threading


def KaweciakTask() -> int:
    return game()


class Server:
    def __init__(self) -> None:
        self.receiver_role = ReceiverMqtt("server", CLINET_CHANNEL)
        self.receiver_role.connect_to_broker()
        self.receiver_role.subscribe_and_start_observing(on_proper_closure=self.mange_request)

        self.sender_role = SenderMqtt("server", SERVER_CHANNEL)
        self.sender_role.connect_to_broker()

        self.ranking = {}
        self.current_gamer = None

        threading.Thread(target=self.refresher, daemon=True).start()

    def transform_ranking_into_list(self):
        transformed_list = [[key, value] for key, value in self.ranking.items()]
        transformed_list.sort(key=lambda x: x[1], reverse=True)
        return transformed_list

    def print_client_channel_test(self, message):
        print(f'{message}')

    def ret_ranking(self, receiver_id):
        self.sender_role.publishMessage(
            MessageFrame(
                SC_RANKING_DELIVER,
                    "server",
                    receiver_id,
                    json.dumps(self.transform_ranking_into_list())
                ).to_str()
            )

    def update_ranking(self, score, receiver_id):
        self.ranking[receiver_id] = score
    
    def respond_to_game_request(self,receiver_id):
        if self.current_gamer == None:
            self.current_gamer = receiver_id
            self.sender_role.publishMessage(
                MessageFrame(
                    SC_SUCCESS,
                    "server",
                    receiver_id,
                    "You started a game"
                ).to_str()
            )
            def game_runner():
                score = KaweciakTask()
                self.ranking[self.current_gamer] = score
                self.sender_role.publishMessage(
                    MessageFrame(
                        SC_END_OF_GAME,
                        "server",
                        receiver_id,
                        json.dumps(
                            {
                                "message": "Game ended",
                                "score": score,
                                "ranking": json.dumps(self.transform_ranking_into_list())
                            }
                        )
                    ).to_str()
                )
                self.current_gamer = None

            threading.Thread(target=game_runner, daemon=True).start()
        else:
            self.sender_role.publishMessage(
                MessageFrame(
                    SC_FAILURE,
                    "server",
                    receiver_id,
                    "You are in game" if receiver_id == self.current_gamer else "other player on line"
                ).to_str()
            )

    def mange_request(self, message):
        message = MessageFrame.from_json(message)
        if message.command_name == CS_GET_RANKING:
            self.ret_ranking(message.src)
        if message.command_name == CS_GAME_INIT:
            self.respond_to_game_request(message.src)
        if message.command_name == SC_REFRESH:
            return

    def refresh_exe(self):
        time.sleep(5)
        self.sender_role.publishMessage(
            MessageFrame(
                SC_REFRESH,
                "server",
                "all",
                "None"
            ).to_str()
        )

    def refresher(self):
        while True:
            self.refresh_exe()

    def disconnect(self):
        self.sender_role.disconnect_from_broker()
        self.receiver_role.disconnect_from_broker()

if __name__ == "__main__":
    serv = Server()
    end_message = ''
    while end_message != 'end':
        end_message=input('Signal end:')
    serv.disconnect()
