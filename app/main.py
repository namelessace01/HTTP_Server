import socket
import threading
def main():
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 4221))
    print("Server started, waiting for connections...")
    client, address = server_socket.accept()  # wait for client
    print(
        f"""The Client: {client}, The Client Address: {address}
          Received connection from: {address[0]}, port: {address[1]}"""
    )
    def request_handler(client, address):
        with client:
            print(f"Connected to {address}[0], Port: {address}[1]")
            client_request: str = client.recv(4096).decode()
            print(f"This is the request {client_request}")
            split_client_request: list[str] = client_request.split("\r\n")
            print(f"This is the Split Request {split_client_request}")
            method, path, version = split_client_request[0].split(" ")
            print(
                f"The Method: ({method}), The Path: ({path}), The Version: ({version})"
            )
            if path == "/":
                confirm_response: bytes = "HTTP/1.1 200 OK\r\n\r\n".encode()
                client.send(confirm_response)
            elif path == "/user-agent":
                user_agent = next(
                    (
                        client_data.split(" ")[1]
                        for client_data in split_client_request
                        if client_data.startswith("User_Agent")
                    ),
                    None,
                )
                print(user_agent)
                response = (
                    f"HTTP/1.1 200 OK\r\n\r\nContent-Type: text/plain\r\n\r\nContent-Length: {len(user_agent)}"
                ).encode()
                client.send(response)
            elif path.startswith("/echo"):
                random_path = path[5:]
                response = (
                    f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(random_path)}\r\n\r\n{random_path}\r\n"
                ).encode()
                client.send(response)
            else:
                not_found_response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
                client.send(not_found_response)
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
            user_agent = next(
                (
                    client_data.split(" ")[1]
                    for client_data in split_client_request
                    if client_data.startswith("User-Agent")
                ),
                None,
            )
            print(f"The user agent {user_agent}")
            response = (
                f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}\r\n"
            ).encode()
            # using the "encode()" method to convert string to bytes, because the server reads bytes not strings."
            client.send(response)
        elif path.startswith("/echo"):
            random_path = path[6:]
            response = (
                f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(random_path)}\r\n\r\n{random_path}\r\n"
            ).encode()
            # using the "encode()" method to convert string to bytes, because the server reads bytes not strings."
            client.send(response)
def drecv(conn, buffersize):
    data = conn.recv(buffersize)
    try:
        data = data.decode()
    except:
        return -1
    finally:
        return data
def dsend(conn, data, buffersize=4096):
    conn.send(data.encode())
def status(index, raw=""):
    ok = "HTTP/1.1 200 OK\r\n"
    notok = "HTTP/1.1 404 Not Found\r\n\r\n"
    context = "Content-Type: text/plain\r\nContent-Length: "
    # context="HTTP/1.1 200 OK\r\n\r\nContent-Type: text/plain\r\nContent-Length: "
    if index == "/":
        content = "Default page"
        mes = ok + context + str(len(content)) + "\r\n" * 2 + content + "\r\n" * 2
    elif index == "/echo/abc/":
        content = "abc"
        mes = ok + context + str(len(content)) + "\r\n" * 2 + content + "\r\n" * 2
        # return context+str(len("abc"))+"\r\n"*2+"abc"+"\r\n"*2
    elif index[0:6] == "/echo/":
        content = index[6:]
        mes = ok + context + str(len(content)) + "\r\n" * 2 + content + "\r\n" * 2
    elif index == "/user-agent":
        content = raw.split("\r\n")[2].split(" ", 1)[1]
        mes = ok + context + str(len(content)) + "\r\n" * 2 + content + "\r\n" * 2
    else:
        # return "HTTP/1.1 404 Not Found\r\n\r\n"
        content = "Page was not found"
        mes = notok + context + str(len(content)) + "\r\n" * 2 + content + "\r\n" * 2
    return mes
def c_handler(conn, addr, buffersize=4096):
    def message(data):
        print("sending message: " + str(data))
        return dsend(conn, data)
    data = drecv(conn, buffersize)
    if data != 0 or data != -1:
        print(data)
        # dsend(conn, message)
        print("data: \n")
        print(data)
        p1 = data.split("\r\n")[0].split()[1]
        message(status(p1, data))
        """
        if p1 == "/":
            message("HTTP/1.1 200 OK\r\n\r\n")
        elif p1 == "/echo/abc":
            #message("abc
            mes="HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: "
            content="abc"
            mes+=str(len(abc))+ "r\n"*2
            mes+=content+"\r\n"*2
            message(mes)
        else:
            not_found_response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
            # using the "encode()" method to convert string to bytes, because the server reads bytes not strings."
            client.send(not_found_response)
            print("Error 404: Bad Request")
        client.close()
        print("Connection Closed")
        server_socket.close()
            message("HTTP/1.1 404 Not Found \r\n\r\n")
        """
    else:
        message(status())
    # t = threading.Thread(target=request_handler, args=(client, address))
    # t.start()
def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    # Uncomment this to pass the first stage
    #
    # server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    # server_socket.accept() # wait for client
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    server_address = ("localhost", 4221)
    s.bind(server_address)
    s.listen()
    while True:
        conn, addr = s.accept()
        c_handler(conn, addr)
        # c_handler(conn, addr)
        threading.Thread(target=c_handler, args=(conn, addr)).start()
if __name__ == "__main__":