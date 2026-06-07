# QFT – QUIC File Transfer Protocol

## Author

**Yashaswini Batchu**
Student ID: **14730825**

## Project Description

QFT (QUIC File Transfer Protocol) is a stateful application-layer protocol designed for secure and reliable file transfer. This project implements the protocol designed in Part 2 of the CS544 course project.

The implementation demonstrates:

* HELLO / WELCOME handshake
* Username and password authentication
* File request processing
* Chunk-based file transfer
* ACK-based reliability
* Error handling
* DFA state validation
* Graceful session termination

## Programming Language

Python 3

## Files Included

```text
QFT_Project/
│
├── server.py
├── client.py
├── protocol.py
├── README.md
│
├── files/
│   └── sample.txt
│
└── received/
    └── sample.txt
```

## Default Configuration

**Port Number:** 4444

**Username:** admin

**Password:** password123

## How to Run the Server

Open a terminal and navigate to the project directory:

```bash
cd QFT_Project
python3 server.py
```

Expected output:

```text
QFT Server Started
Listening on port 4444
Waiting for client...
```

## How to Run the Client

Open a second terminal and navigate to the project directory:

```bash
cd QFT_Project
python3 client.py
```

Enter the following information when prompted:

```text
Server IP Address: 127.0.0.1
Username: admin
Password: password123
Filename: sample.txt
```

## Protocol States Implemented

* STATE_START
* STATE_CONNECTED
* STATE_AUTHENTICATED
* STATE_TRANSFERRING
* STATE_COMPLETED
* STATE_CLOSED
* STATE_ERROR

## Message Types Implemented

* HELLO
* WELCOME
* AUTH_REQUEST
* AUTH_SUCCESS
* FILE_REQUEST
* FILE_CHUNK
* ACK
* ERROR
* CLOSE

## Successful Test Cases

* Client successfully connects to server
* HELLO/WELCOME handshake
* Successful authentication
* File request processing
* File transfer using FILE_CHUNK messages
* ACK processing
* Session termination using CLOSE
* File successfully saved in the received directory

## Error Test Cases

* Invalid password
* AUTH_FAILED error response
* DFA state validation
* Error message processing

## Notes

The original QFT protocol design specifies operation over QUIC. For this prototype implementation, TCP sockets were used to demonstrate protocol functionality, message processing, file transfer, and DFA validation.

This implementation serves as a working foundation for future development of a complete QUIC-based QFT implementation.

Extra Credit
GitHub Repository

Project source code is available at:

https://github.com/Yashaswinibatchu/CS544-QFT-Protocol

Implementation Reflection

Additional documentation discussing lessons learned during implementation, protocol design updates, and future enhancements is included in:

implementation_notes.txt
