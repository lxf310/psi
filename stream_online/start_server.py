import gevent
from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template
from flask_socketio import SocketIO, Namespace
from bsread import source
import argparse
import os
from matplotlib import pyplot
from threading import Lock
picName = ''
picUrlName = ''

async_mode = None
app = Flask(__name__, static_url_path="/static", static_folder="static")
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)  
stream_output_port = None
stream_output_host = None
thread = None
thread_lock = Lock()

def processStream():
    with source(host=stream_output_host, port=stream_output_port, receive_timeout=1000) as input_stream:
        while True:
            message = input_stream.receive()
            if message is None:
                continue

            socketio.sleep(1)
            beam_energy = message.data.data["beam_energy"].value
            repetition_rate = message.data.data["repetition_rate"].value
            image = message.data.data["image"].value
            pyplot.imshow(image)
            pyplot.savefig(picName)
            metadata = {
                'beam_energy': str(beam_energy),
                'repetition_rate': str(repetition_rate),
                'picture': picUrlName
            }
            print(metadata)
            socketio.emit('server_response', 
                           metadata, 
                           namespace='/test_conn')

@app.route('/')
def index():
    return render_template('index.html')

class MyNamespace(Namespace):
    def on_my_event(self, message):
        print(message)

    def on_connect(self):
        global thread
        with thread_lock:
            if thread is None:
                thread = socketio.start_background_task(
                    target=processStream)
        socketio.emit('server_response', {'beam_energy': '', 'repetition_rate': '', 'picture': ''})

    def on_disconnect(self):
        print('Client disconned!')

socketio.on_namespace(MyNamespace('/test_conn'))

def main():
    parser = argparse.ArgumentParser(description='Socekt IO server')
    parser.add_argument('-o', '--output_port', default=8888, type=int, help="Stream output port")
    parser.add_argument('-s', '--output_host', default='localhost', type=str, help="Stream output host")
    parser.add_argument('-p', '--server_port', default=5000, type=int, help="Server port")
    arguments = parser.parse_args()
    # set the arguments
    global stream_output_port
    global stream_output_host
    stream_output_port = arguments.output_port
    stream_output_host = arguments.output_host
    global picUrlName
    global picName
    picUrlName = "/static/%s.jpg" % str(stream_output_port)
    picName = "." + picUrlName
    socketio.run(app, port=arguments.server_port, debug=True)

if __name__ == "__main__":
    main()
