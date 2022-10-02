import socket


while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 9999))  # localhost, port above 1023
        s.listen()
        connection, address = s.accept()
        with connection:
            print("Connected by", address)
            while True:
                data = connection.recv(1024)
                if not data:
                    break
                connection.sendall(data)
