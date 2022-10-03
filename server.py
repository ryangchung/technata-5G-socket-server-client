import socket


while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 9999))  # localhost, port above 1023
        s.listen()
        connection, address = s.accept()
        with connection:
            print("Connected by", address)
            data = connection.recv(1024)
            decoded_data = data.decode()
            connection.send("Request of \"{decoded_data}\" was completed ")
