from datetime import datetime
from flask import Flask, jsonify, render_template, Response
# from flask_socketio import SocketIO, emit
from imageio import v3 as iio

import base64
import imageio
import glob
import os
import time

app = Flask(__name__)

srv_path = '/srv/pi-camera'
camera_log_file = srv_path + '/camera_mode.log'
mode_waiting = 'WAIT'
mode_error = 'ERROR'
mode_picture = 'PICTURE'
mode_video = 'VIDEO'
init_timestamp = 20230901010101
frame_rate = 30

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

def latest_picture_mode_timestamp():
    latest = init_timestamp
    with open(camera_log_file) as f:
        for line in f.readlines():
            if line.split(':')[0] == mode_picture:
                latest = int(line.split(':')[1])
    return latest

def latest_video_mode_timestamp():
    latest = init_timestamp
    with open(camera_log_file) as f:
        for line in f.readlines():
            if line.split(':')[0] == mode_video:
                latest = int(line.split(':')[1])
    return latest

def latest_video_path():
    latest_video = init_timestamp
    for mp4_path in glob.glob(srv_path + '/*mp4'):
        file_name = os.path.basename(mp4_path)
        file_timestamp = os.path.splitext(file_name)[0]
        if int(file_timestamp) >= latest_video_mode_timestamp():
            if int(file_timestamp) > latest_video:
                latest_video = int(file_timestamp)
    return srv_path + '/' + str(latest_video) + '.mp4'

def gen_feed():
    video = imageio.get_reader(latest_video_path(), 'ffmpeg', ffmpeg_params=['-r', str(frame_rate)])
    for _, frame in enumerate(video):
        jpg_encoded = iio.imwrite("<bytes>", frame, plugin="pillow", format="JPEG")
        yield b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + jpg_encoded + b'\r\n\r\n'
        time.sleep(1/frame_rate)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status', methods=['GET'])
def status():
    status = current_status()
    return jsonify({'status': status})

@app.route('/start_video', methods=['GET'])
def start_video():
    write_camera_log(mode_video, '')
    status = current_status()
    return jsonify({'status': status})

@app.route('/start_picture', methods=['GET'])
def start_picture():
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
    for jpg_path in glob.glob(srv_path + '/*.jpg'):
        file_name = os.path.basename(jpg_path)
        file_timestamp = os.path.splitext(file_name)[0]
        if int(file_timestamp) >= latest_picture_mode_timestamp():
            with open(jpg_path, 'rb') as img_file:
                data = base64.b64encode(img_file.read())
                pictures.append(data.decode('utf-8'))
    return jsonify({'pictures': pictures, 'picture_mode_timestamp': latest_picture_mode_timestamp()})

@app.route('/video_feed', methods=['GET'])
def video_feed():
    return Response(gen_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")
