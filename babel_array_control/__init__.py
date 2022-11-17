import time
import zmq
import json
from threading import Thread
from server import ArrayServer, ArrayServerException


def reply(socket, body):
    response = bytes(json.dumps(body), 'utf-8')
    socket.send(response)


def reply_error(zmq_sock, error_msg):
    error = {
        'error': error_msg,
    }

    reply(zmq_sock, error)


def zmq_thread_fn(array_server):
    context = zmq.Context()

    zmq_sock = context.socket(zmq.REP)
    zmq_sock.bind("tcp://*:5555")

    while True:
        message = zmq_sock.recv()
        print(f'Received external request: {message}')

        try:
            reply(zmq_sock, array_server.handle_request(message))
        except ArrayServerException as e:
            reply_error(zmq_sock, str(e))


def main():
    array_server = ArrayServer()

    Thread(target=zmq_thread_fn, daemon=True, args=(array_server,)).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('Exiting...')


if __name__ == '__main__':
    main()
