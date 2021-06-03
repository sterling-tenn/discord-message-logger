import websocket
import json
import threading
import time
import os
import random

def send_json_request(ws,request):
    global websocket_url
    try:
        ws.send(json.dumps(request))
    except websocket.WebSocketConnectionClosedException:
        ws.connect(websocket_url)
        ws.send(json.dumps(request))

def receive_json_response(ws):
    global websocket_url
    try:
        response = ws.recv()
        if response:
            return json.loads(response)
    except:
        pass

if __name__ == "__main__":
    websocket_url = "wss://gateway.discord.gg/?v=9&encoding=json"
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

    ws = websocket.WebSocket()# Create new websocket
    ws.connect(websocket_url)# Connect to the websocket

    send_json_request(ws,payload)# Send initial identify payload

    while True:
        event = receive_json_response(ws)
        try:
            if event["d"]["channel_id"] == channel_id:
                # print(json.dumps(event,indent = 5))# Test print message to see the structure of the payload better
                content = event["d"]["content"]
                author = event["d"]["author"]["username"]
                print(f"{author}: {content}\n")
        except:
            pass