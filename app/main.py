import socket


def main():
    
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221))
    print("Server started, waiting for connections...")

    client, address = server_socket.accept()  # wait for client
    print(client, address)
    print(f"Received connection from: {address[0]}, port: {address[1]}")

    with client:
        # using 4096 as buffer size to provide good performance and simple HTTP handling requests.
        request = client.recv(4096).decode()

        # splitting the request
        split_request = request.split("\r\n")

        # should expect three set of split request GET /path HTTP/1.1
        method, path, version = split_request[0].split(" ")

        if path == "/":
            confirm_response = "HTTP/1.1 200 OK\r\n\r\n"
            client.send(confirm_response.encode())

        elif path.startswith("/echo"):
            random_path = path[6:]
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(random_path)}\r\n\r\n{random_path}\r\n"
            client.send(response.encode())

        else:
            not_found_response = "HTTP/1.1 404 Not Found\r\n\r\n"
            client.send(not_found_response.encode())

        client.close()

        
    # # receving data from the client side using "recv()" method on the client and "decode() method to decode from bytes to string"
    # cli_data: str = client.recv(1024).decode()
    # print("Decoding client data...")

    # # splitting the client data into a list of strings to give a list where each element is a line from the HTTP request
    # split_cli_data: list[str] = cli_data.split("\r\n")
    # print("Splitting client data...")


    # # response from the server
    # response: bytes = "HTTP/1.1 200 OK\r\n\r\n".encode() 
    # # using the "encode()" method to convert string to bytes, because the server reads bytes not strings."
    # print("""Encoding Data...
    #       Extraction Complete.""")

    # # if split client data separated by space indexing the second element is not equal to "/"
    # if split_cli_data[0].split(" ")[1] != "/":
        # # response from the server
    #     response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
    #     print("Error 404: Bad Request")
    # client.send(response)

    # print("Disconnected from server.")
    # client.close()
    # server_socket.close()

    # # print(f"Connected, client address: {address}")
    # # client.sendall(b"HTTP/1.1 200 OK\r\n\r\n")  # wait for client

    
if __name__ == "__main__":
    main()