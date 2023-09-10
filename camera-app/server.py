from datetime import datetime
from flask import Flask, jsonify, render_template

import base64
import glob

app = Flask(__name__)

img_path = '/srv/pi-camera'
camera_log_file = img_path + '/camera_mode.log'
mode_waiting = 'WAIT'
mode_error = 'ERROR'
mode_picture = 'PICTURE'
mode_video = 'VIDEO'

#
# Client App to operate pi-camera
#

def write_camera_log(mode, comment):
    now = datetime.now()
    with open(camera_log_file, mode='a') as f:
        f.write(mode + ':' + now.strftime("%Y%m%d%H%M%S") + ':' + '\n')

def current_status():
    with open(camera_log_file) as f:
        latest = f.readlines()[-1]
        status = latest.split(':')[0]
        comment = latest.split(':')[-1]
        if len(comment) > 0: 
            status += (': ' + comment)
        return status

def latest_picture_mode():
    latest = 20230901010101
    with open(camera_log_file) as f:
        for line in f.readlines():
            if line.split(':')[0] == mode_picture:
                latest = line.split(':')[1]
    return latest

@app.route('/')
def index():
    print(latest_picture_mode())
    return render_template('index.html')

@app.route('/status', methods=['GET'])
def status():
    status = current_status()
    latest_picture_mode()
    return jsonify({'status': status})

@app.route('/start', methods=['GET'])
def start():
    write_camera_log(mode_picture, '')
    status = current_status()
    return jsonify({'status': status})

@app.route('/stop', methods=['GET'])
def stop():
    write_camera_log(mode_waiting, '')
    status = current_status()
    return jsonify({'status': status})

@app.route('/pictures', methods=['GET'])
def pictures():
    pictures = []
    for jpg_path in glob.glob(img_path + '/*.jpg'):
        with open(jpg_path, 'rb') as img_file:
            data = base64.b64encode(img_file.read())
            pictures.append(data.decode('utf-8'))
    return jsonify({'pictures': pictures})


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")
