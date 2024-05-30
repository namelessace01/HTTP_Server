import socket
import re
import threading

def main():
    
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221))
    print("Server started, waiting for connections...")

    client, address = server_socket.accept()  # wait for client
    print(f"""The Client: {client}, The Client Address: {address}
          Received connection from: {address[0]}, port: {address[1]}""")
    
    headers = {}
    response_body = ""
    with client:
        # receving request from the client side using "recv()" method on the client and "decode()" method to decode from bytes to string.
        # using 4096 as buffer size to provide good performance and simple HTTP handling requests.
        client_request: str = client.recv(4096).decode()
        print(f"This is the request {client_request}")

        # splitting the request
        split_client_request: list[str] = client_request.split("\r\n")
        print(f"This is the Split Request {split_client_request}")

        # should expect three set of split request GET /path HTTP/1.1
        method, path, version = split_client_request[0].split(" ")
        print(f"The Method: ({method}), The Path: ({path}), The Version: ({version})")

        if path == "/":
            # using the "encode()" method to convert string to bytes, because the server reads bytes not strings."
            confirm_response: bytes = "HTTP/1.1 200 OK\r\n\r\n".encode()
            client.send(confirm_response)

        elif path == "/user-agent":
            # splitting the client data into a list of strings to give a list where each element is a line from the HTTP request
            user_agent = next((client_data.split(":")[1] for client_data in split_client_request if client_data.startswith("User-Agent")),None)
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}\r\n"
            # using the "encode()" method to convert string to bytes, because the server reads bytes not strings."
            client.send(response.encode())

            headers["Content-Type"] = "text/plain"
            headers["Content-Length"] = len(response_body)

        elif path.startswith("/echo"):
            random_path = path[6:]
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(random_path)}\r\n\r\n{random_path}\r\n"

            # using the "encode()" method to convert string to bytes, because the server reads bytes not strings."
            client.send(response.encode())

            headers["Content-Type"] = "text/plain"
            headers["Content-Length"] = len(response_body)

        else:
            not_found_response = "HTTP/1.1 404 Not Found\r\n\r\n"

            # using the "encode()" method to convert string to bytes, because the server reads bytes not strings."
            client.send(not_found_response.encode())
            print("Error 404: Bad Request")


        client.close()
        print("Connection Closed")
        server_socket.close()


if __name__ == "__main__":
    main()