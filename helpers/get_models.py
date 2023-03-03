import os.path
import queue
import socketio
import json

import os.path
# import queue
import socketio
import json
import time

def model_lister():
    # global models
    # models = queue.Queue()
    f = open(os.path.dirname(__file__) + '/../config.json')
    server_url = json.load(f)["server_url"]


    sio = socketio.Client()
    sio.connect(server_url)

    sio.emit("requestSystemConfig")
    models = None
    def get_models(socket_event):
        nonlocal models
        models = socket_event
    sio.on("systemConfig", get_models)
    time.sleep(0.5)

    # models = models.get()["model_list"]
    model_list = list(models["model_list"].keys())
    sio.disconnect()
    return model_list
