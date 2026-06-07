"""
QFT Protocol Definitions

Defines message types, protocol states,
message creation/parsing functions,
and DFA validation logic.
"""
import json

# Message Types
MSG_HELLO = "HELLO"
MSG_WELCOME = "WELCOME"
MSG_AUTH_REQUEST = "AUTH_REQUEST"
MSG_AUTH_SUCCESS = "AUTH_SUCCESS"
MSG_FILE_REQUEST = "FILE_REQUEST"
MSG_FILE_CHUNK = "FILE_CHUNK"
MSG_ACK = "ACK"
MSG_ERROR = "ERROR"
MSG_CLOSE = "CLOSE"

# States
STATE_START = "START"
STATE_CONNECTED = "CONNECTED"
STATE_AUTHENTICATED = "AUTHENTICATED"
STATE_TRANSFERRING = "TRANSFERRING"
STATE_COMPLETED = "COMPLETED"
STATE_CLOSED = "CLOSED"
STATE_ERROR = "ERROR"

HEADER_LENGTH = 8


def create_message(message_type, payload):
    message = {
        "header": {
            "header_length": HEADER_LENGTH,
            "message_type": message_type,
            "flags": 0,
            "payload_length": len(json.dumps(payload))
        },
        "payload": payload
    }
    return (json.dumps(message) + "\n").encode()


def receive_message(sock):
    data = b""
    while not data.endswith(b"\n"):
        chunk = sock.recv(4096)
        if not chunk:
            return None
        data += chunk
    return json.loads(data.decode())


def validate_state(current_state, message_type):
    valid = {
        STATE_START: [MSG_HELLO],
        STATE_CONNECTED: [MSG_AUTH_REQUEST],
        STATE_AUTHENTICATED: [MSG_FILE_REQUEST, MSG_CLOSE],
        STATE_TRANSFERRING: [MSG_ACK, MSG_CLOSE],
        STATE_COMPLETED: [MSG_CLOSE],
        STATE_CLOSED: [],
        STATE_ERROR: []
    }

    return message_type in valid.get(current_state, [])
