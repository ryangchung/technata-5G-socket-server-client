import socket


while True:
    try:
        user_input = input("Input action and quantity: ")
        split_input = user_input.split()
        commands = ["add", "remove"]
        if split_input[0] not in commands:
            raise Exception
        quantity = int(split_input[1])

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("127.0.0.1", 9999))
            s.sendall(bytes(user_input, 'utf-8'))
            data = s.recv(1024)
        print(f"Received {data!r}")
    except Exception:
        print("Invalid command")
        continue