#!/usr/bin/env python3

# TODO: Write valid_macro and macro

from copy import copy
from re import match
from time import sleep
from uuid import uuid4

from keyboard_controller import get_keys

QUEUE = []
VALID_KEYS = get_keys()
RUN = True


def set_run(toggle):
    global RUN

    if isinstance(toggle, bool):
        RUN = toggle


def run():
    if RUN:
        return True

    return False


def length():
    return len(QUEUE)


def view():
    return QUEUE


def valid_command(data):
    regex = r'^[\w\d !@#$%=;`,_:"~\^\&\*\(\)\-\[\]\\\'\.\/\+\{\}\|\<\>\?]+$'

    if 'sleep' in data.keys() and not isinstance(data['sleep'], int):
        return False

    if 'multiplier' in data.keys() and not isinstance(data['multiplier'], int):
        return False

    if 'command' in data.keys() and 'input' in data.keys():
        if data['command'] == 'press' and data['input'] in VALID_KEYS:
            return True
        if data['command'] == 'hold' and data['input'] in VALID_KEYS \
                and 'delay' in data.keys() and isinstance(data['delay'], int):
            return True
        if data['command'] == 'string' and match(regex, data['input']):
            return True

    return False


def clean_command(command):
    new_command = copy(command)
    valid_keys = ['command', 'input', 'delay', 'sleep', 'comment', 'uuid']

    for key in command.keys():
        if key not in valid_keys:
            del new_command[key]

    if new_command['command'] != 'hold' and 'delay' in new_command.keys():
        del new_command['delay']

    return new_command


def valid_multiplier(data):
    if 'multiplier' in data.keys() and isinstance(data['multiplier'], int) \
            and data['multiplier'] > 0:
        return True

    return False


def valid_append(data):
    if isinstance(data, dict) and valid_command(data):
        return True

    return False


def valid_macro(data):
    pass


def valid_insert(data):
    if isinstance(data, dict) and 'command' in data.keys() \
            and 'location' in data.keys() and valid_command(data['command']) \
            and (0 <= data['location'] < length()):
        return True

    return False


def valid_remove(data):
    if isinstance(data, dict) and 'uuid' in data.keys() \
            and isinstance(data['uuid'], str):
        return True

    return False


def append(data):
    if not valid_append(data):
        return 400, {
            'status': 'failure',
            'message': 'Malformed input'
        }

    response = []
    i = 1
    if valid_multiplier(data):
        i = data['multiplier']
        del data['multiplier']
    while i > 0:
        command = data
        command['uuid'] = str(uuid4())
        command = clean_command(command)
        QUEUE.append(command)
        response.append(command)
        i = i - 1

    return 200, {
        'status': 'success',
        'message': 'Command appended sucessfully',
        'commands': response
    }


def macro(data):
    pass


def insert(data):
    if not valid_insert(data):
        return 400, {
            'status': 'failure',
            'message': 'Malformed input'
        }

    command = data['command']
    command['uuid'] = str(uuid4())
    command = clean_command(command)
    QUEUE.insert(data['location'], command)

    return 200, {
        'status': 'success',
        'message': 'Command inserted successfully',
        'location': data['location'],
        'command': command
    }


def remove(data):
    if not valid_remove(data):
        return 400, {
            'status': 'failure',
            'message': 'Malformed input'
        }

    set_run(False)
    # HACK
    # We're racing here, if this falls in between the sleeping checks it'll
    # just keep running on the last command, so we'll sleep for a 1/10 of a
    # second, which should be 100x longer than needed
    sleep(0.1)

    i = 0
    removed = False

    for entry in QUEUE:
        if entry['uuid'] == data['uuid']:
            del QUEUE[i]
            removed = True
        i = i + 1

    set_run(True)

    if not removed:
        return 410, {
            'status': 'failure',
            'message': 'Could not find command to remove'
        }

    return 200, {
        'status': 'success',
        'message': 'Removed command sucessfully'
    }
