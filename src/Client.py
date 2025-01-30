from time import sleep
import RPi.GPIO as GPIO
from mfrc522 import MFRC522
import tkinter as tk
from tkinter import ttk
from utils import *
from Sender import SenderMqtt
from Receiver import ReceiverMqtt
from namespace import SERVER_CHANNEL
from namespace import CLINET_CHANNEL
from commands import *
import threading

class ScrollableFrame(ttk.Frame):
    def __init__(self, parent, bg_color="#361B41"):
        super().__init__(parent)

        self.canvas = tk.Canvas(self, bg=bg_color)
        
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg_color)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

class Client():
    def __init__(self):
        self.logged_rfid = None
        self.cardReader = MFRC522()
        self.main_view = None

        self.current_score = None
        self.ranking = [["test", -1]]*1
        self.current_message = None

        self.to_server_connection = None
        self.from_server_connection = None

        self.loop_thread = threading.Thread(target=self.service_loop, daemon=True)
        self.loop_thread.start()

    def refresh(self):
        clear_frame(self.main_view)
        self.main_view.geometry("800x400")

        # Custom font
        fixedsys_font = ("Fixedsys", 14)
        title_font = ("Fixedsys", 32, "bold")

        # Top frame (Title Bar)
        top_frame = tk.Frame(self.main_view, bg="#361B41", height=80)
        top_frame.pack(fill=tk.X)

        title_label = tk.Label(top_frame, text="BREAKOUT", font=title_font, fg="#FFBB00", bg="#361B41")
        title_label.pack(expand=True)

        # Bottom container
        bottom_frame = tk.Frame(self.main_view, bg="#361B41")
        bottom_frame.pack(fill=tk.BOTH, expand=True)

        # Left panel
        left_panel = tk.Frame(bottom_frame, bg="#361B41", bd=5, relief=tk.RIDGE, highlightbackground="#A30003",
                              highlightthickness=5)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Right panel
        right_panel = tk.Frame(bottom_frame, bg="#361B41", bd=5, relief=tk.RIDGE, highlightbackground="#A30003",
                               highlightthickness=5)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Player ID
        player_frame = tk.Frame(left_panel, bg="#361B41", highlightbackground="#A30003", highlightthickness=5)
        player_frame.pack(fill=tk.X, padx=10, pady=5)

        player_label = tk.Label(player_frame, text="PLAYER", font=fixedsys_font, fg="#A2EEBE", bg="#361B41")
        player_label.pack()

        player_value = tk.Label(player_frame, text=self.get_rfid(), font=fixedsys_font, fg="#A2EEBE", bg="#361B41")
        player_value.pack()

        # Score
        score_frame = tk.Frame(left_panel, bg="#361B41", highlightbackground="#A30003", highlightthickness=5)
        score_frame.pack(fill=tk.X, padx=10, pady=5)

        score_label = tk.Label(score_frame, text="SCORE", font=fixedsys_font, fg="#A2EEBE", bg="#361B41")
        score_label.pack()

        score_value = tk.Label(score_frame, text=self.get_current_score(), font=fixedsys_font, fg="#A2EEBE",
                               bg="#361B41")
        score_value.pack()

        # Message
        message_frame = tk.Frame(left_panel, bg="#361B41", highlightbackground="#A30003", highlightthickness=5)
        message_frame.pack(fill=tk.X, padx=10, pady=5)

        message_label = tk.Label(message_frame, text="CURRENT MESSAGE", font=fixedsys_font, fg="#A2EEBE", bg="#361B41")
        message_label.pack()

        message_value = tk.Label(message_frame, text=self.current_message, font=fixedsys_font, fg="#A2EEBE",
                                 bg="#361B41")
        message_value.pack()

        # Play Button
        play_button = tk.Button(left_panel, text="PLAY", font=fixedsys_font, fg="#A2EEBE", bg="#5348C9",
                                relief=tk.RIDGE, command=self.start_game)
        play_button.pack(fill=tk.X, padx=10, pady=10)

        # Right Panel (Top Scores)
        top_scores_frame = tk.Frame(right_panel, bg="#361B41", highlightbackground="#A30003")
        top_scores_frame.pack(fill=tk.BOTH, expand=True)

        top_scores_label = tk.Label(top_scores_frame, text="TOP SCORES", font=fixedsys_font, fg="#A2EEBE", bg="#361B41")
        top_scores_label.pack()

        scrollable_frame = ScrollableFrame(top_scores_frame)
        scrollable_frame.pack(fill="both", expand=True)

        # Populate ranking
        if self.ranking:
            self.ranking.sort(key=lambda x: x[1], reverse=True)

            for player_id, score in self.ranking:
                score_label = tk.Label(scrollable_frame.scrollable_frame, 
                                       text=f"{player_id}: {score}", 
                                       font=fixedsys_font, fg="#A2EEBE", bg="#361B41")
                score_label.pack(anchor="w", padx=10, pady=2)
        else:
            empty_label = tk.Label(scrollable_frame.scrollable_frame, text="No scores yet", 
                                   font=fixedsys_font, fg="#A2EEBE", bg="#361B41")
            empty_label.pack()


        self.main_view.update_idletasks()

    def on_close(self):
        self.main_view.destroy()
        if self.to_server_connection is not None:
            self.to_server_connection.disconnect_from_broker()
            self.from_server_connection.disconnect_from_broker()

    def on_server_message(self,message):
        frame: MessageFrame = MessageFrame.from_json(message)
        if frame.command_name == SC_REFRESH:
            self.produce_request(CS_REFRESH)
            return
        if frame.dest != self.get_rfid():
            return
        if frame.command_name == SC_RANKING_DELIVER:
            self.ranking =  json.loads(frame.data)
        elif frame.command_name == SC_SUCCESS or frame.command_name == SC_FAILURE:
            self.current_message = frame.data
        elif frame.command_name == SC_END_OF_GAME:
            passed_data = json.loads(frame.data)
            self.current_message = passed_data['message']
            self.current_score = passed_data['score']
            self.ranking = json.loads(passed_data['ranking'])

        sleep(0.5)
        self.refresh()

    def establish_connection(self):
        self.current_message = "Play to set your score"

        self.to_server_connection = SenderMqtt(self.logged_rfid, topic=CLINET_CHANNEL)
        self.to_server_connection.connect_to_broker()

        self.from_server_connection = ReceiverMqtt(self.logged_rfid, topic=SERVER_CHANNEL)
        self.from_server_connection.connect_to_broker()
        self.from_server_connection.subscribe_and_start_observing(on_proper_closure=self.on_server_message)

    def produce_request(self, command: str):
        self.to_server_connection.publishMessage(MessageFrame(command,self.get_rfid(),"server","None").to_str())

    def get_ranking(self):
        self.produce_request(CS_GET_RANKING)

    def start_game(self):
        self.produce_request(CS_GAME_INIT)

    def get_rfid(self):
        return str(self.logged_rfid)

    def get_current_score(self):
        return str(self.current_score) if self.current_score is not None else "No score yet"

    def initalize(self):
        self.main_view = tk.Tk()
        self.main_view.title("Breakout")
        self.main_view.geometry("300x200")
        self.main_view.resizable(False, False) 

        frame = tk.Frame(self.main_view, padx=20, pady=20)
        frame.pack(expand=True, fill=tk.BOTH)

        banner_label = tk.Label(frame, text="Log in with your card", font=("Arial", 18, "bold"), fg="black")
        banner_label.pack(pady=30)

        self.main_view.protocol("WM_DELETE_WINDOW", self.on_close)
        self.main_view.mainloop()


    def try_to_read_rfid(self):
        (status, TagType) = self.cardReader.MFRC522_Request(self.cardReader.PICC_REQIDL)
        if status == self.cardReader.MI_OK:
            (status, uid) = self.cardReader.MFRC522_Anticoll()
            if status == self.cardReader.MI_OK:
                self.logged_rfid = uid

    def service_loop(self):
        while True:
            self.execute_in_loop()

    def execute_in_loop(self):
        if self.logged_rfid is None:
            self.try_to_read_rfid()
            if self.logged_rfid is not None:
                self.establish_connection()
                self.get_ranking()
                self.refresh()

if __name__ == '__main__':
    client = Client()
    client.initalize()