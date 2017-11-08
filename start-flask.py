from flask import Flask, flash, render_template, request, redirect, url_for, send_file, make_response
from utils import json_format, success, gen_service
from crossdomain import CrossDomainResponse
import watson
import argparse
import watson
import io
import random
import time
import storage

from pythonosc import osc_message_builder
from pythonosc import udp_client

app = Flask(__name__)
app.secret_key = 'pgfall2017'
app.response_class = CrossDomainResponse

RUNNING = False


@app.route('/')
def index():
    return "jj"


@app.route('/start/', methods=['GET'])
@json_format
def start_listening():
    global RUNNING
    if not RUNNING:
        watson.start_listening()
        RUNNING = True
    return success()


@app.route('/gen_audio/')
def generate_audio_clip():
    start = request.args.get('start', -1.0, type=float)
    end = request.args.get('end', -1.0, type=float)
    filename = storage.get_wav_from_time(start, end)
    return send_file(
        filename,
        mimetype="audio/wav",
        as_attachment=True,
        attachment_filename=filename)


@app.route('/get_audio/')
def get_audio_clip():
    start = request.args.get('start', -1.0, type=float)
    end = request.args.get('end', -1.0, type=float)
    file = io.BytesIO()
    storage.get_wav_string_from_time(file, start, end)
    response = make_response(file.getvalue())
    file.close()
    response.headers['Content-Type'] = 'audio/wav'
    response.headers['Content-Disposition'] = 'attachment; filename=' + str(round(start * 100)) + '_' + str(round(end * 100)) + '.wav'
    return response



@app.route('/pause/', methods=['GET'])
@json_format
def pause_listening():
    watson.pause_listening()
    return success()


@app.route('/resume/', methods=['GET'])
@json_format
def resume_listening():
    watson.resume_listening()
    return success()


@app.route('/sentences/', methods=['GET'])
@json_format
def get_sentence_count():
    ret = {"count": len(watson.sentences)}
    return success(ret)


@app.route('/sentences/<int:sentence_id>', methods=['GET'])
@json_format
def get_sentence(sentence_id):
    try:
        ret = {"text": watson.sentences[sentence_id]}
        return success(ret)
    except:
        return success()


@app.route('/verbs/', methods=['GET'])
@json_format
def get_verb_count():
    ret = {"count": len(watson.verbs)}
    return success(ret)


@app.route('/verbs/<int:verbs_id>', methods=['GET'])
@json_format
def get_verb(verbs_id):
    try:
        ret = {"text": watson.verbs[verbs_id]}
        return success(ret)
    except:
        return success()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
                        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=8088,
                        help="The port the OSC server is listening on")
    args = parser.parse_args()

    osc_client = udp_client.SimpleUDPClient(args.ip, args.port)

    # for x in range(10):
    #     client.send_message("/filter", random.random())
    #     time.sleep(1)

    watson.set_osc_client(osc_client)
    # watson.start_listening()
    app.run(host="127.0.0.1", debug=True)
