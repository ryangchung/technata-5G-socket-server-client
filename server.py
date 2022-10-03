import socket

total_needed_power = 0

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 9999))  # localhost, port above 1023
        s.listen()
        connection, address = s.accept()
        with connection:
            print("Connected by", address)
            data = connection.recv(1024)
            decoded_data = data.decode()
            print("Received request of", decoded_data)

            if decoded_data[0] == "+":
                total_needed_power += int(decoded_data[1:-1])
            else:
                total_needed_power -= int(decoded_data[1:-1])
            print("Total power is now", total_needed_power, "W")

            connection.send(bytes(f"Request of {decoded_data} was completed", 'utf-8'))
