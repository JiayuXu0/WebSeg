'''
Author: Jiayu Xu
Date: 2022-05-16 18:15:44
LastEditors: Jiayu Xu
Description: file content
FilePath: \EISeg\web.py
'''
from flask import Flask
import cv2
import urllib
import json
import numpy as np
from flask import Flask, redirect, url_for, request
from eiseg.controller import InteractiveController
app = Flask(__name__)


predictor_params = {
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

controller = InteractiveController(
    predictor_params=predictor_params,
    prob_thresh=0.5)

controller.setModel(
    "pretrain\static_hrnet18s_ocr48_cocolvis.pdiparams")
controller.filterLargestCC(True)
controller.addLabel(0, "default", [200, 200, 0])
# path = "C:\\Users\\vitio\\Desktop\\wKhkEWJ7p-WAKE0pACGZ84crPr4856.png"
# image = cv2.imdecode(np.fromfile(path, dtype=np.uint8), 1)
# image = image[:, :, ::-1]  # BGR转RGB
# controller.setImage(image)
# controller.addClick(640, 309, True)
# A = controller.finishObject()
# print(A)


@app.route('/load_image', methods=['POST'])
def load_image():
    if request.method == 'POST':
        url = request.form['image_url']
        req = urllib.request.urlopen(url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, 1)
        img = img[:, :, ::-1]
        controller.setImage(img)
        return json.dumps({"ret": 0, "msg": "ok"})


@app.route('/add_click', methods=['POST'])
def add_click():
    if request.method == 'POST':
        x = int(request.form['click_x'])
        y = int(request.form['click_y'])
        controller.addClick(x, y, True)
        A = controller.finishObjectwithoutclear()
        return json.dumps({"ret": 0, "msg": "ok", "result": A[1]})


@app.route('/clear')
def clear():
    controller.resetLastObject()
    return json.dumps({"ret": 0, "msg": "ok"})


if __name__ == '__main__':
    app.run()
