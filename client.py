"""
QFT Client

Handles:
- Server connection
- Authentication
- File requests
- File download
- DFA state tracking
"""
import socket
from protocol import *

PORT = 4444
RECEIVED_DIR = "received"


def run_client():
    state = STATE_START

    host = input("Enter server hostname or IP address: ")
    username = input("Enter username: ")
    password = input("Enter password: ")
    filename = input("Enter filename to download: ")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, PORT))

    print("\nConnected to QFT server")
    print(f"Current State: {state}")

    hello_payload = {
        "version": 1,
        "client_id": 1,
        "max_chunk_size": 32,
        "auth_method": 1
    }

    client.sendall(create_message(MSG_HELLO, hello_payload))
    print("HELLO sent")

    response = receive_message(client)

    if response["header"]["message_type"] == MSG_WELCOME:
        state = STATE_CONNECTED
        print("WELCOME received")
        print("STATE_START -> STATE_CONNECTED")
    else:
        print("Expected WELCOME but received error")
        return

    auth_payload = {
        "username": username,
        "password": password
    }

    client.sendall(create_message(MSG_AUTH_REQUEST, auth_payload))
    print("AUTH_REQUEST sent")

    response = receive_message(client)

    if response["header"]["message_type"] == MSG_AUTH_SUCCESS:
        state = STATE_AUTHENTICATED
        print("AUTH_SUCCESS received")
        print("STATE_CONNECTED -> STATE_AUTHENTICATED")
    else:
        print("Authentication failed")
        print(response)
        return

    file_payload = {
        "request_id": 1,
        "filename": filename,
        "chunk_size": 32,
        "start_chunk": 0
    }

    client.sendall(create_message(MSG_FILE_REQUEST, file_payload))
    print("FILE_REQUEST sent")

    state = STATE_TRANSFERRING
    print("STATE_AUTHENTICATED -> STATE_TRANSFERRING")

    output_path = f"{RECEIVED_DIR}/{filename}"

    with open(output_path, "w") as f:
        while True:
            msg = receive_message(client)

            if msg is None:
                break

            msg_type = msg["header"]["message_type"]
            payload = msg["payload"]

            if msg_type == MSG_FILE_CHUNK:
                chunk_number = payload["chunk_number"]
                total_chunks = payload["total_chunks"]

                print(f"FILE_CHUNK received: {chunk_number + 1}/{total_chunks}")
                f.write(payload["data"])

                ack_payload = {
                    "request_id": payload["request_id"],
                    "chunk_number": chunk_number
                }

                client.sendall(create_message(MSG_ACK, ack_payload))
                print(f"ACK sent for chunk {chunk_number + 1}")

            elif msg_type == MSG_CLOSE:
                state = STATE_COMPLETED
                print("All chunks received")
                print("STATE_TRANSFERRING -> STATE_COMPLETED")

                state = STATE_CLOSED
                print("CLOSE received")
                print("STATE_COMPLETED -> STATE_CLOSED")
                break

            elif msg_type == MSG_ERROR:
                state = STATE_ERROR
                print("ERROR received")
                print(payload)
                break

    client.close()
    print(f"File saved to {output_path}")


if __name__ == "__main__":
    run_client()
