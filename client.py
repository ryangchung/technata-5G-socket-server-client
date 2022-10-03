import socket

host = "127.0.0.1"
port = 9999
client_total_power = 0

def send_message(host, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(bytes(message, 'utf-8'))
        return s.recv(1024).decode()

while True:
    try:
        # Checking user input - Should not have any errors getting passed into the server
        user_input = input("Input action (ex: +23W): ")
        command = user_input[0]
        quantity = int(user_input[1:-1])
        if command == "+":
            client_total_power += quantity
            print("Local power:", client_total_power, "W")
            print(send_message(host, port, user_input), "\n")
        elif command == "-":
            if client_total_power - quantity < 0:
                raise Exception
            else:
                client_total_power -= quantity
                print("Local power:", client_total_power, "W")
                print(send_message(host, port, user_input))
        else:
            raise Exception
    except Exception:
        print("Invalid command")
        continue