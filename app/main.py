import socket


def main():
    
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221))
    print("Server started, waiting for connections...")

    client, address = server_socket.accept()  # wait for client
    print(client, address)
    

    # receving data from the client side using "recv" method on the client
    cli_data: str = client.recv(1024).decode()

    # splitting the client data into a list of strings to give a list where each element is a line from the HTTP request
    split_cli_data = list[str] = cli_data.split("\r\n")


    # response from the server
    response: bytes = "HTTP/1.1 200 OK\r\n\r\n".encode()
    print("Extraction Complete.")

    # if split client data separated by space indexing the second element is not equal to "/"
    if split_cli_data[0].split(" ")[1] != "/":
        # response from the server
        response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
        print("Error 404: Bad Request")


    print(f"Connected, client address: {address}")
    client.sendall(b"HTTP/1.1 200 OK\r\n\r\n")  # wait for client

    
if __name__ == "__main__":
    main()