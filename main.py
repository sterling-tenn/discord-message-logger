import websocket
import json
import threading
import time
import os

def send_json_request(ws,request):
    ws.send(json.dumps(request))

def receive_json_response(ws):
    response = ws.recv()
    if response:
        return json.loads(response)

def heartbeat(interval, ws):
    while True:
        time.sleep(interval)
        heartbeatJSON = {
            "op": 1,
            "d": "null"
        }
        send_json_request(ws, heartbeatJSON)

ws = websocket.WebSocket()
ws.connect("wss://gateway.discord.gg/?v=6&encording=json")
heartbeat_interval = receive_json_response(ws)["d"]["heartbeat_interval"]
heartbeat_interval = heartbeat_interval / 1000 #time.sleep uses seconds not milli seconds
threading._start_new_thread(heartbeat, (heartbeat_interval, ws, ))

channel_id = input("Enter Channel ID:")
token = input("Enter Authorization Token:")
os.system("cls")
payload = {
    "op":2,
    "d":{
        "token":token,
        "intents":513,
        "properties":{
            "$os":"windows",
            "$browser":"chrome",
            "$device":"pc"
        }
    }
}


send_json_request(ws,payload)

while True:
    event = receive_json_response(ws)
    try:
        if event["d"]["channel_id"]==channel_id:
            content = event["d"]["content"]
            author = event["d"]["author"]["username"]
            print(f"{author}: {content}\n")
    except:
        pass