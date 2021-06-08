import asyncio
import json
from firstbot import *
import aiohttp
from yarl import URL
import logging

def get_path_safe(d, *path):
    for node in path:
        d = d.get(node)
        if d == None:
            return None
    return d

with open("APIkeys.txt") as secrets:
    project_id = "c2d9d192-c769-47b1-8406-3c3b6489dc73"
    user_name = secrets.readline().rstrip("\r\n")
    user_secret = secrets.readline().rstrip("\r\n")

theBot = initializeBot(False, "chatbot-development12.tsv")

# wss://api.chatengine.io/person/?publicKey={{project_id}}&username={{user_name}}&secret={{user_secret}}
ws_uri = URL.build(
    scheme="wss",
    host="api.chatengine.io",
    path="/person/",
    query={
        "publicKey": project_id,
        "username": user_name,
        "secret": user_secret
    }
)

# https://urldefense.com/v3/__https://api.chatengine.io/__;!!DZ3fjg!oalyqJL5Hp13yYiTDsa-ZXaAzgcp1e7mDit7DxtvJ6takVxBCO5qd2zSTYqV3MjJX70$ 
chatengine_api_uri = URL.build(scheme="https", host="api.chatengine.io")

async def start():
    headers = {"Project-ID": project_id, "User-Name": user_name, "User-Secret": user_secret}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.ws_connect(ws_uri) as ws:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    logging.debug("Websocket Recieved: %s", msg.data)
                    try:
                        jsonmessage = json.loads(msg.data)
                    except:
                        continue
                    action = jsonmessage.get("action")
                    if action == None:
                        continue
                    if action == "new_message":
                        logging.debug("Got Message!")
                        data = jsonmessage.get("data")
                        if not isinstance(data, dict):
                            continue
                        chatId = data.get("id")
                        chatMessage = data.get("message")
                        if not isinstance(chatId, int) or not isinstance(chatMessage, dict):
                            continue
                        sender = get_path_safe(chatMessage, "sender", "username")
                        userIn = chatMessage.get("text")
                        if sender == user_name or not isinstance(userIn, str):
                            continue
                        output = getResponse(theBot, userIn)
                        logging.debug("Sending Message: %s", output)
                        async with session.post(
                            chatengine_api_uri.with_path(f"/chats/{chatId}/messages/"),
                            data={"text": output}
                        ) as response:
                            logging.debug("Chat Sending: %r", response)

                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break

asyncio.get_event_loop().run_until_complete(start())




