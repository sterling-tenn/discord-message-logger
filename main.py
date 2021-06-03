import websocket
import json
import threading
import time
import os
import random

def send_json_request(ws,request):
    global websocket_url
    while True:
        try:
            ws.send(json.dumps(request))
        except websocket.WebSocketConnectionClosedException:
            ws.connect(websocket_url)
            continue
        break

def receive_json_response(ws):
    global websocket_url
    while True:
        try:
            response = ws.recv()
            if response:
                return json.loads(response)
        except websocket.WebSocketConnectionClosedException:
            ws.connect(websocket_url)
            continue
        break

def heartbeat(interval,ws,heartbeat_JSON):
    while True:
        time.sleep(interval)
        send_json_request(ws, heartbeat_JSON)


websocket_url = "wss://gateway.discord.gg/?v=8&encoding=json"
channel_id = input("Enter Channel ID:")
token = input("Enter Authorization Token:")
os.system("cls")
payload = {
    "op":2,
    "d":{
        "token":token,
        "properties":{
            "$os":"windows",
            "$browser":"chrome",
            "$device":"pc"
        }
    }
}
heartbeat_JSON = {
    "op": 1,
    "d": "null"
}

ws = websocket.WebSocket()
ws.connect(websocket_url)

event = receive_json_response(ws)
heartbeat_interval = event["d"]["heartbeat_interval"] / 1000 * random.random()
threading.Thread(target=heartbeat,args=(heartbeat_interval,ws,heartbeat_JSON)).start()

send_json_request(ws,payload)

while True:
    event = receive_json_response(ws)
    if event["op"]==1:
        send_json_request(ws,heartbeat_JSON)
    try:
        if event["d"]["channel_id"]==channel_id:
            content = event["d"]["content"]
            author = event["d"]["author"]["username"]
            print(f"{author}: {content}\n")
    except:
        pass