import socket
import threading
import sys

def client_request_handler(client, address):
    with client:
        print(f"Connected to: ({address[0]}), Port: ({address[1]})")

        client_request: str = client.recv(4096).decode()
        print(f"Client-Request: ({client_request})")

        split_client_request = list[str] = client_request.split("\r\n")
        print(f"Split-Client-Request: ({split_client_request})")

        method, path, version = split_client_request[0].split(" ")
        print(f"Method: ({method}), Path: ({path}), Version: ({version})")

        if path == "/":
            confirm_response: bytes = ("HTTP/1.1 200 OK\r\n\r\n").encode()
            client.send(confirm_response)

        elif "/user-agent" in path:
            user_agent = next((data.split(" ")[1] for data in split_client_request if data.startswith("user-agent")), None)
            print(f"User-Agent: ({user_agent})")
            response = (f"HTTP/1.1 200 OK\r\nContent-Type: text-plain\r\nContent-Length: ({len(user_agent)}\r\n\r\n({user_agent})").encode()
            client.send(response)