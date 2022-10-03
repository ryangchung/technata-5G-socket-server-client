import socket


while True:
    try:
        # Checking user input - Should not have any errors getting passed into the server
        user_input = input("Input action (ex: +23 W): ")
        if user_input[0] in "+-":
            int(user_input[1:-2])
        else:
            raise Exception

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("127.0.0.1", 9999))
            s.sendall(bytes(user_input, 'utf-8'))
            data = s.recv(1024)
        print(f"Received {data!r}")
    except Exception:
        print("Invalid command")
        continue