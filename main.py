import json
import time
import numpy
import requests
import os
# import matplotlib.pyplot as plt
from PIL import Image


def print_response(response):
    print(response)
    _data = response.json()
    for _key in _data:
        print(_key, _data[_key])


def get_server_address():
    with open(os.getenv('ProgramData') + '/SteelSeries/SteelSeries Engine 3/coreProps.json') as json_file:
        data = json.load(json_file)
        address = data['address']
    return address


def get_wallpaper_dir():
    try:
        _wallpaper_folder = os.getenv('AppData') + '/Microsoft/Windows/Themes/CachedFiles/'
        _wallpaper_name = os.listdir(_wallpaper_folder)[0]
        return _wallpaper_folder + '/' + _wallpaper_name
    except:
        wallpaper = os.getenv('AppData') + '/Microsoft/Windows/Themes/TranscodedWallpaper'
        return wallpaper


def compute_keyboard_ilum():
    global cached_image
    try:
        server_address = get_server_address()
        wallpaper_dir = get_wallpaper_dir()
        print('Successful fetch')

    except Exception as e:
        print('Error')
        print(e)
        return

    if cached_image is None:
        payload_1 = {
            "game": "WALLPAPER",
            "event": "TEST",
            "min_value": 0,
            "max_value": 100,
            "icon_id": 1,
            "handlers": [
                {
                    # "device-type": "keyboard",
                    "device-type": "rgb-per-key-zones",
                    # "zone": "function-keys",
                    # "color": {"gradient": {"zero": {"red": 255, "green": 0, "blue": 0},
                    #                        "hundred": {"red": 0, "green": 255, "blue": 0}}},
                    # "mode": "percent",
                    "mode": "bitmap",
                }
            ]
        }
        try:
            requests.post('http://' + server_address + '/bind_game_event', json=payload_1)
        except:
            return
        # print_response(r)

    try:
        img_full = Image.open(wallpaper_dir)
    except:
        return
    img = img_full.resize((22, 6), Image.NEAREST)

    # plt.figure(1)
    # plt.imshow(img_full)
    #
    # plt.figure(2)
    # plt.imshow(img)
    #
    # plt.show()

    cached_image = img

    pix = numpy.array(img.convert('RGB')).reshape([132, 3])
    color_array = pix.tolist()

    payload_2 = {
        "game": "WALLPAPER",
        "event": "TEST",
        # "data": {
        #     "value": 100
        # }
        "data": {
            "frame": {
                "bitmap": color_array
            }
        }
    }

    requests.post('http://' + server_address + '/game_event', json=payload_2)
    # print_response(r)


cached_image = None
while True:
    compute_keyboard_ilum()
    time.sleep(1)
