from os.path import exists
import sys

if not exists("./.env"):
    print("[ERROR] .env not found. Did you install?")
    print("https://github.com/redigermany/cas-robocup-master/#install")
    sys.exit()

import asyncio
import random
import websockets
import jsonpickle
import threading
import datetime

from enum import Enum

from dotenv import dotenv_values
config = dotenv_values(".env")

from src.web.server import runWebserver

class EGameState(Enum):
    PLAYING = 1
    PAUSED = 2
    FOUL = 3
    ENDED = 4
    GOAL = 5

class GameState:
    state:EGameState = EGameState.PAUSED

class Singleton(object):
    _instance = None

    data = {
        "state": "debug",
        "time_remaining": "time_remaining",
        "robots": [
            {
                "x": random.random(),
                "y": random.random(),
                "id": "blue",
                "angle": random.random()*360,
            },
            {
                "x": random.random(),
                "y": random.random(),
                "id": "green",
                "angle": random.random()*360,
            },
            {
                "x": random.random(),
                "y": random.random(),
                "id": "yellow",
                "angle": random.random()*360,
            },
            {
                "x": random.random(),
                "y": random.random(),
                "id": "pink",
                "angle": random.random()*360,
            }
        ],
        "balls": [
            {
                "x": random.random(),
                "y": random.random(),
            }   
        ]
    }

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

s1 = Singleton()

async def show_time(websocket):
    while True:
        message = datetime.datetime.utcnow().isoformat() + "Z"
        await websocket.send(jsonpickle.encode({
            "state": "debug",
            "time_remaining": message,
            "robots": [
                {
                    "x": random.random(),
                    "y": random.random(),
                    "id": "blue",
                    "angle": random.random()*360,
                },
                {
                    "x": random.random(),
                    "y": random.random(),
                    "id": "green",
                    "angle": random.random()*360,
                },
                {
                    "x": random.random(),
                    "y": random.random(),
                    "id": "yellow",
                    "angle": random.random()*360,
                },
                {
                    "x": random.random(),
                    "y": random.random(),
                    "id": "pink",
                    "angle": random.random()*360,
                }
            ],
            "balls": [
                {
                    "x": random.random(),
                    "y": random.random(),
                }   
            ]
        }))
        await asyncio.sleep(1)

async def do_start_websocket():
    WS_PORT = int(config.get("WS_PORT"))
    async with websockets.serve(show_time, "localhost", WS_PORT):
        print(f"Websocket listening on ws://localhost:{WS_PORT}")
        await asyncio.Future()  # run forever

def start_websocket():
    asyncio.run(do_start_websocket())
    
# Start Server
def main():
    http = threading.Thread(target=runWebserver, daemon=True)
    http.start()
    start_websocket()

if __name__ == "__main__":
    main()
