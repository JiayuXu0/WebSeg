'''
Author: Jiayu Xu
Date: 2022-05-16 18:15:44
LastEditors: Jiayu Xu
Description: file content
FilePath: \SegService\web.py
'''
from flask import Flask
import cv2
import urllib
import json
import numpy as np
import string
import random
import time
from flask import Flask, redirect, url_for, request
from cacheout import Cache
from eiseg.controller import InteractiveController
app = Flask(__name__)
cache = Cache(maxsize=256, ttl=600, timer=time.time, default=None)


@app.route('/load_image', methods=['POST'])
def load_image():
    letters = string.ascii_letters
    key = ''.join(random.choice(letters) for i in range(10))
    param = {
        "brs_mode": "NoBRS",
        "with_flip": False,
        "zoom_in_params": {
            "skip_clicks": -1,
            "target_size": (400, 400),
            "expansion_ratio": 1.4,
        },
        "predictor_params": {
            "net_clicks_limit": None,
            "max_size": 800,
            "with_mask": True,
        },
    }
    if request.method == 'POST':
        controller = InteractiveController(predictor_params=param,
                                           prob_thresh=0.5)
        controller.setModel(
            "pretrain/static_hrnet18s_ocr48_cocolvis.pdiparams")
        controller.filterLargestCC(True)
        controller.addLabel(0, "default", [200, 200, 0])
        url = request.form['image_url']
        req = urllib.request.urlopen(url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, 1)
        img = img[:, :, ::-1]
        controller.setImage(img)
        cache.set(key, controller)
        return json.dumps({"ret": 0, "msg": "ok", "key": key})


@app.route('/add_click', methods=['POST'])
def add_click():
    if request.method == 'POST':
        x = int(request.form['click_x'])
        y = int(request.form['click_y'])
        flag = int(request.form['flag'])
        key = request.form['key']
        f = True if flag == 1 else False
        controller = cache.get(key)
        controller.addClick(x, y, f)
        A = controller.finishObjectwithoutclear()
        return json.dumps({"ret": 0, "msg": "ok", "result": A[1]})


@app.route('/clear', methods=['GET'])
def clear():
    key = request.args.get('key')
    cache.delete(key)
    return json.dumps({"ret": 0, "msg": "ok"})


if __name__ == '__main__':
    app.run(host="0.0.0.0")
