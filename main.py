#!/usr/bin/env python3

import argparse
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import ipaddress
import json
import os
try:
    from secrets import token_hex
except ImportError:
    def token_hex(nbytes=None):
        return os.urandom(nbytes).hex()
import socket
from socketserver import ThreadingMixIn
import sys
import threading
from time import sleep

import command_queue as queue
import keyboard_controller

AUTH_KEY = 'DEADCODEDEADCODEDEADCODEDEADCODE'


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_resuse_address = True
    request_queue_size = 16


class MyHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def send_response(self, code, message=None):
        self.log_request(code)
        self.send_response_only(code, message)

    def my_sender(self, code, mime, content):
        try:
            self.send_response(code)
            self.send_header('Connection', 'close')
            self.send_header('Content-Type', mime)
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        except socket.error:
            print('ERROR: Broken Pipe')

    def do_GET(self):
        if self.headers['x-auth-key'] == AUTH_KEY:
            if self.path == '/api/queue':
                response = queue.view()
                response = bytes(json.dumps(response), 'utf-8')
                self.my_sender(200, 'application/json', response)
            else:
                response = bytes(json.dumps({
                    'status': 'failure',
                    'message': 'API ndpoint not found'
                }), 'utf-8')
                self.my_sender(404, 'application/json', response)
        else:
            response = bytes(json.dumps({
                'status': 'failure',
                'message': 'Not Authorized'
            }), 'utf-8')
            self.my_sender(403, 'application/json', response)

    def do_POST(self):
        if self.headers['x-auth-key'] == AUTH_KEY:
            try:
                length = int(self.headers['content-length'])
                postvars = self.rfile.read(length)
                data = json.loads(postvars.decode('utf-8'))
            except json.JSONDecodeError:
                response = bytes(json.dumps({
                    'status': 'failure',
                    'message': 'Error parsing JSON'
                }), 'utf-8')
                self.my_sender(400, 'application/json', response)
                return

            if self.path == '/api/append':
                code, response = queue.append(data)
                response = bytes(json.dumps(response), 'utf-8')
                self.my_sender(code, 'application/json', response)
            elif self.path == '/api/remove':
                code, response = queue.remove(data)
                response = bytes(json.dumps(response), 'utf-8')
                self.my_sender(code, 'application/json', response)
            elif self.path == '/api/insert':
                code, response = queue.insert(data)
                response = bytes(json.dumps(response), 'utf-8')
                self.my_sender(code, 'application/json', response)
            else:
                response = bytes(json.dumps({
                    'status': 'failure',
                    'message': 'API ndpoint not found'
                }), 'utf-8')
                self.my_sender(404, 'application/json', response)
        else:
            response = bytes(json.dumps({
                'status': 'failure',
                'message': 'Not Authorized'
            }), 'utf-8')
            self.my_sender(403, 'application/json', response)

    def log_message(self, format, *args):
        pass


def getch():
    """MIT Licensed: https://github.com/joeyespo/py-getch"""
    import termios
    import tty

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def closer(message):
    print(message)
    if message != '\r>> Exiting...                                           ':
        print('Press any key to exit...', end='')
        sys.stdout.flush()
        if os.name == 'nt':
            from msvcrt import getch as w_getch
            w_getch()
        else:
            getch()
        print()
    sys.exit()


def run_command(command):
    if 'sleep' in command.keys():
        total_sleep_seconds = command['sleep'] / 1000
        i = 0.0

        # HACK: This needs to be synced in command_queue.remove() it currently
        # sleeps there to prevent this loop from missing the change in
        # command_queue.run()
        while i < total_sleep_seconds:
            if not queue.run():
                return False
            sleep(0.001)
            i = i + 0.001
    if command['command'] == 'press':
        keyboard_controller.input_key(command['input'])
    if command['command'] == 'hold':
        keyboard_controller.input_key(command['input'], command['delay'])
    if command['command'] == 'string':
        keyboard_controller.input_string(command['input'])

    return True


def command_processor():
    while 1:
        if queue.length() > 0 and queue.run():
            if run_command(queue.view()[0]):
                queue.remove({'uuid': queue.view()[0]['uuid']})


def start_server(host, port):
    try:
        server = ThreadedHTTPServer((host, port), MyHandler)
        thread = threading.Thread(name='HTTP_Server',
                                  target=server.serve_forever,
                                  args=(),
                                  daemon=True)
        thread.start()
        print('>> HTTP server thread is running...')
    except OSError:
        print('ERROR: Could not start server, ' +
              'is another program on {}:{}?'.format(host, port))
        closer('    ^^This could also be a permission error^^')
    except UnicodeDecodeError:
        print('ERROR: Python failed to get a FQDN (This is a Python Bug)')
        closer('    ^^Change your computers name to be [a-zA-Z0-9]^^')


def start_command_processor():
    thread = threading.Thread(name='Command_Processor',
                              target=command_processor(),
                              args=(),
                              daemon=True)
    thread.start()


def main():
    global AUTH_KEY

    parser = argparse.ArgumentParser(description='Remote Keyboard via USB OTG')
    parser.add_argument('--host', dest='host', action='store', type=str,
                        default='127.0.0.1', required=False,
                        help='Specify the IP of the interface to listen to')
    parser.add_argument('--port', dest='port', action='store', type=int,
                        default=8080, required=False,
                        help='Specify the port to listen to')
    parser.add_argument('--auth-key', dest='auth_key', action='store',
                        type=str, default=token_hex(32), required=False,
                        help='Specify the authorization key')
    args = parser.parse_args()

    if not ipaddress.IPv4Address(args.host):
        closer('ERROR: Invalid IPv4 input for host')

    if args.port <= 0 or args.port > 65535:
        closer('ERROR: Invalid port input (Must be between 1 and 65535)')

    AUTH_KEY = args.auth_key
    print('AUTH_KEY: {}'.format(AUTH_KEY))

    try:
        start_server(args.host, args.port)
        start_command_processor()

        while True:
            sleep(24 * 60 * 60)
    except KeyboardInterrupt:
        closer('\r>> Exiting...                                           ')


if __name__ == '__main__':
    main()
