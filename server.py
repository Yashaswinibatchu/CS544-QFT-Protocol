"""
QFT Server

Handles:
- Client connections
- Authentication
- File transfer
- ACK processing
- DFA validation
"""
import socket
import os
import math
from protocol import *

HOST = "0.0.0.0"
PORT = 4444
FILES_DIR = "files"
USERNAME = "admin"
PASSWORD = "password123"
CHUNK_SIZE = 32


def send_error(conn, code, message):
    error_payload = {
        "error_code": code,
        "error_message": message
    }
    conn.sendall(create_message(MSG_ERROR, error_payload))
    print(f"ERROR sent: {code} - {message}")


def run_server():
    state = STATE_START

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)

    print("QFT Server Started")
    print(f"Listening on port {PORT}")
    print("Waiting for client...")

    conn, addr = server.accept()
    print(f"Client Connected: {addr}")
    print(f"Current State: {state}")

    while True:
        msg = receive_message(conn)

        if msg is None:
            break

        msg_type = msg["header"]["message_type"]
        payload = msg["payload"]

        print(f"\nReceived Message: {msg_type}")

        if not validate_state(state, msg_type):
            print(f"Invalid message {msg_type} received in state {state}")
            send_error(conn, 103, "INVALID_STATE")
            state = STATE_ERROR
            print(f"State changed to: {state}")
            break

        if msg_type == MSG_HELLO:
            print("HELLO received")
            state = STATE_CONNECTED
            print("STATE_START -> STATE_CONNECTED")

            welcome_payload = {
                "version": 1,
                "server_id": 100,
                "session_id": 555,
                "selected_chunk_size": CHUNK_SIZE
            }
            conn.sendall(create_message(MSG_WELCOME, welcome_payload))
            print("WELCOME sent")

        elif msg_type == MSG_AUTH_REQUEST:
            username = payload["username"]
            password = payload["password"]

            if username == USERNAME and password == PASSWORD:
                state = STATE_AUTHENTICATED
                print("Authentication successful")
                print("STATE_CONNECTED -> STATE_AUTHENTICATED")

                auth_payload = {
                    "session_id": 555,
                    "role": "user"
                }
                conn.sendall(create_message(MSG_AUTH_SUCCESS, auth_payload))
                print("AUTH_SUCCESS sent")
            else:
                print("Authentication failed")
                send_error(conn, 101, "AUTH_FAILED")
                state = STATE_ERROR
                break

        elif msg_type == MSG_FILE_REQUEST:
            filename = payload["filename"]
            request_id = payload["request_id"]
            start_chunk = payload["start_chunk"]

            filepath = os.path.join(FILES_DIR, filename)

            if not os.path.exists(filepath):
                send_error(conn, 102, "FILE_NOT_FOUND")
                state = STATE_ERROR
                break

            state = STATE_TRANSFERRING
            print("FILE_REQUEST received")
            print("STATE_AUTHENTICATED -> STATE_TRANSFERRING")

            file_size = os.path.getsize(filepath)
            total_chunks = math.ceil(file_size / CHUNK_SIZE)

            with open(filepath, "rb") as f:
                f.seek(start_chunk * CHUNK_SIZE)

                for chunk_number in range(start_chunk, total_chunks):
                    data = f.read(CHUNK_SIZE)

                    chunk_payload = {
                        "request_id": request_id,
                        "chunk_number": chunk_number,
                        "total_chunks": total_chunks,
                        "data_length": len(data),
                        "data": data.decode(errors="ignore")
                    }

                    conn.sendall(create_message(MSG_FILE_CHUNK, chunk_payload))
                    print(f"FILE_CHUNK sent: {chunk_number + 1}/{total_chunks}")

                    ack = receive_message(conn)
                    if ack and ack["header"]["message_type"] == MSG_ACK:
                        print(f"ACK received for chunk {ack['payload']['chunk_number'] + 1}")

            state = STATE_COMPLETED
            print("All chunks acknowledged")
            print("STATE_TRANSFERRING -> STATE_COMPLETED")

            conn.sendall(create_message(MSG_CLOSE, {"reason": "Transfer complete"}))
            print("CLOSE sent")
            state = STATE_CLOSED
            print("STATE_COMPLETED -> STATE_CLOSED")
            break

        elif msg_type == MSG_CLOSE:
            print("CLOSE received")
            state = STATE_CLOSED
            print("State changed to CLOSED")
            break

    conn.close()
    server.close()
    print("Server shut down")


if __name__ == "__main__":
    run_server()
