import socket
import threading

def request_handler(client, address):
    with client:
        print(f"Connected to ({address[0]}), Port: ({address[1]})")

        client_request: str = client.recv(4096).decode()
        print(f"The Client Request ({client_request})")

        split_client_request: list[str] = client_request.split("\r\n")
        print(f"The Split Request ({split_client_request})")

        method, path, version = split_client_request[0].split(" ")
        print(f"The Method: ({method}), The Path: ({path}), The Version: ({version})")

        if path == "/":
            confirm_response: bytes = "HTTP/1.1 200 OK\r\n\r\n".encode()
            client.send(confirm_response)

        elif path == "/user-agent":
            user_agent = next((client_data.split(" ")[1] for client_data in split_client_request if client_data.startswith("User-Agent")), None)
            print(f"The User Agent ({user_agent})")
            response = (f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: ({len(user_agent)})\r\n\r\n({user_agent})\r\n").encode()
            client.send(response)

        elif path.startswith("/echo"):
            random_path = path[6:]
            response = (f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: ({len(random_path)})\r\n\r\n({random_path})\r\n").encode()
            client.send(response)

        else:
            not_found_response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
            client.send(not_found_response)

        print("""
              Closing Connection...
              Connection Closed""")

def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221))
    print("Server started, waiting for connections...")

    try:
        while True:
            client, address = server_socket.accept()  # wait for client
            print(f"Received connection from: ({address[0]}), port: ({address[1]})")

            # Create a new thread to handle the request
            threading.Thread(target=request_handler, args=(client, address)).start()
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
