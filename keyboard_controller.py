#!/usr/bin/env python3

from time import sleep

NULL_CHR = chr(0)
SHIFT = chr(32) + NULL_CHR
NO_SHIFT = NULL_CHR * 2
END_INPUT = NULL_CHR * 5

COMMANDS = {
    'dummy': NULL_CHR * 8,
    'a': NO_SHIFT + chr(4) + END_INPUT,
    'b': NO_SHIFT + chr(5) + END_INPUT,
    'c': NO_SHIFT + chr(6) + END_INPUT,
    'd': NO_SHIFT + chr(7) + END_INPUT,
    'e': NO_SHIFT + chr(8) + END_INPUT,
    'f': NO_SHIFT + chr(9) + END_INPUT,
    'g': NO_SHIFT + chr(10) + END_INPUT,
    'h': NO_SHIFT + chr(11) + END_INPUT,
    'i': NO_SHIFT + chr(12) + END_INPUT,
    'j': NO_SHIFT + chr(13) + END_INPUT,
    'k': NO_SHIFT + chr(14) + END_INPUT,
    'l': NO_SHIFT + chr(15) + END_INPUT,
    'm': NO_SHIFT + chr(16) + END_INPUT,
    'n': NO_SHIFT + chr(17) + END_INPUT,
    'o': NO_SHIFT + chr(18) + END_INPUT,
    'p': NO_SHIFT + chr(19) + END_INPUT,
    'q': NO_SHIFT + chr(20) + END_INPUT,
    'r': NO_SHIFT + chr(21) + END_INPUT,
    's': NO_SHIFT + chr(22) + END_INPUT,
    't': NO_SHIFT + chr(23) + END_INPUT,
    'u': NO_SHIFT + chr(24) + END_INPUT,
    'v': NO_SHIFT + chr(25) + END_INPUT,
    'w': NO_SHIFT + chr(26) + END_INPUT,
    'x': NO_SHIFT + chr(27) + END_INPUT,
    'y': NO_SHIFT + chr(28) + END_INPUT,
    'z': NO_SHIFT + chr(29) + END_INPUT,
    'A': SHIFT + chr(4) + END_INPUT,
    'B': SHIFT + chr(5) + END_INPUT,
    'C': SHIFT + chr(6) + END_INPUT,
    'D': SHIFT + chr(7) + END_INPUT,
    'E': SHIFT + chr(8) + END_INPUT,
    'F': SHIFT + chr(9) + END_INPUT,
    'G': SHIFT + chr(10) + END_INPUT,
    'H': SHIFT + chr(11) + END_INPUT,
    'I': SHIFT + chr(12) + END_INPUT,
    'J': SHIFT + chr(13) + END_INPUT,
    'K': SHIFT + chr(14) + END_INPUT,
    'L': SHIFT + chr(15) + END_INPUT,
    'M': SHIFT + chr(16) + END_INPUT,
    'N': SHIFT + chr(17) + END_INPUT,
    'O': SHIFT + chr(18) + END_INPUT,
    'P': SHIFT + chr(19) + END_INPUT,
    'Q': SHIFT + chr(20) + END_INPUT,
    'R': SHIFT + chr(21) + END_INPUT,
    'S': SHIFT + chr(22) + END_INPUT,
    'T': SHIFT + chr(23) + END_INPUT,
    'U': SHIFT + chr(24) + END_INPUT,
    'V': SHIFT + chr(25) + END_INPUT,
    'W': SHIFT + chr(26) + END_INPUT,
    'X': SHIFT + chr(27) + END_INPUT,
    'Y': SHIFT + chr(28) + END_INPUT,
    'Z': SHIFT + chr(29) + END_INPUT,
    '1': NO_SHIFT + chr(30) + END_INPUT,
    '2': NO_SHIFT + chr(31) + END_INPUT,
    '3': NO_SHIFT + chr(32) + END_INPUT,
    '4': NO_SHIFT + chr(33) + END_INPUT,
    '5': NO_SHIFT + chr(34) + END_INPUT,
    '6': NO_SHIFT + chr(35) + END_INPUT,
    '7': NO_SHIFT + chr(36) + END_INPUT,
    '8': NO_SHIFT + chr(37) + END_INPUT,
    '9': NO_SHIFT + chr(38) + END_INPUT,
    '0': NO_SHIFT + chr(39) + END_INPUT,
    '!': SHIFT + chr(30) + END_INPUT,
    '@': SHIFT + chr(31) + END_INPUT,
    '#': SHIFT + chr(32) + END_INPUT,
    '$': SHIFT + chr(33) + END_INPUT,
    '%': SHIFT + chr(34) + END_INPUT,
    '^': SHIFT + chr(35) + END_INPUT,
    '&': SHIFT + chr(36) + END_INPUT,
    '*': SHIFT + chr(37) + END_INPUT,
    '(': SHIFT + chr(38) + END_INPUT,
    ')': SHIFT + chr(39) + END_INPUT,
    'enter': NO_SHIFT + chr(40) + END_INPUT,
    'esc': NO_SHIFT + chr(41) + END_INPUT,
    'backspace': NO_SHIFT + chr(42) + END_INPUT,
    'tab': NO_SHIFT + chr(43) + END_INPUT,
    'delete': NO_SHIFT + chr(76) + END_INPUT,
    ' ': NO_SHIFT + chr(44) + END_INPUT,
    '-': NO_SHIFT + chr(45) + END_INPUT,
    '=': NO_SHIFT + chr(46) + END_INPUT,
    '[': NO_SHIFT + chr(47) + END_INPUT,
    ']': NO_SHIFT + chr(48) + END_INPUT,
    '\\': NO_SHIFT + chr(49) + END_INPUT,
    ';': NO_SHIFT + chr(51) + END_INPUT,
    '\'': NO_SHIFT + chr(52) + END_INPUT,
    '`': NO_SHIFT + chr(53) + END_INPUT,
    ',': NO_SHIFT + chr(54) + END_INPUT,
    '.': NO_SHIFT + chr(55) + END_INPUT,
    '/': NO_SHIFT + chr(56) + END_INPUT,
    '_': SHIFT + chr(45) + END_INPUT,
    '+': SHIFT + chr(46) + END_INPUT,
    '{': SHIFT + chr(47) + END_INPUT,
    '}': SHIFT + chr(48) + END_INPUT,
    '|': SHIFT + chr(49) + END_INPUT,
    ':': SHIFT + chr(51) + END_INPUT,
    '"': SHIFT + chr(52) + END_INPUT,
    '~': SHIFT + chr(53) + END_INPUT,
    '<': SHIFT + chr(54) + END_INPUT,
    '>': SHIFT + chr(55) + END_INPUT,
    '?': SHIFT + chr(56) + END_INPUT,

    # PS4 Controller Buttons
    'cross': NO_SHIFT + chr(40) + END_INPUT,
    'circle': NO_SHIFT + chr(41) + END_INPUT,
    'triangle': NO_SHIFT + chr(58) + END_INPUT,
    'square': NO_SHIFT + chr(59) + END_INPUT,
    'options': NO_SHIFT + chr(60) + END_INPUT,
    'share': NO_SHIFT + chr(70) + END_INPUT,
    'ps-button': NO_SHIFT + chr(72) + END_INPUT,
    'right': NO_SHIFT + chr(79) + END_INPUT,
    'left': NO_SHIFT + chr(80) + END_INPUT,
    'down': NO_SHIFT + chr(81) + END_INPUT,
    'up': NO_SHIFT + chr(82) + END_INPUT,
    'l1': NO_SHIFT + chr(0) + END_INPUT,  # Not Mapped?
    'l2': NO_SHIFT + chr(0) + END_INPUT,  # Not Mapped?
    'l3': NO_SHIFT + chr(0) + END_INPUT,  # Not Mapped?
    'r1': NO_SHIFT + chr(0) + END_INPUT,  # Not Mapped?
    'r2': NO_SHIFT + chr(0) + END_INPUT,  # Not Mapped?
    'r3': NO_SHIFT + chr(0) + END_INPUT   # Not Mapped?
}


def valid_key(key, shift, usage_id):
    if isinstance(key, str) and isinstance(shift, bool) \
            and isinstance(usage_id, int) and (0 <= usage_id <= 65535):
        return True

    return False


def get_keys():
    return COMMANDS.keys()


def add_key(key, shift, usage_id):
    if not valid_key(key, shift, usage_id):
        print('ERROR: Tried to add a malformed keyboard command')
        return

    if shift:
        COMMANDS[key] = SHIFT + chr(usage_id) + END_INPUT
    else:
        COMMANDS[key] = NO_SHIFT + chr(usage_id) + END_INPUT


def write_report(report):
    with open('/dev/hidg0', 'rb+') as buf:
        buf.write(report.encode())


def input_key(key, delay=100):
    if key in COMMANDS:
        write_report(COMMANDS[key])
        sleep(delay / 1000)
        write_report(NULL_CHR * 8)


def input_string(input_str):
    for character in input_str:
        input_key(character)
