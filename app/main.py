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


    print(f"Connected, client address: {address}")
    client.sendall(b"HTTP/1.1 200 OK\r\n\r\n")  # wait for client

    
if __name__ == "__main__":
    main()