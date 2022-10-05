import socket
from sys import exit


def send_message(host, port, message, sensor_id):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(bytes(f"{message},{sensor_id}", "utf-8"))
        return s.recv(1024).decode()


def main():
    host = "127.0.0.1"
    port = 9999

    client_total_power = 0

    print(
        """
        ###########################################
        # Welcome to the client for the 5G sensor #
        ###########################################

        """
    )

    while True:
        try:
            # ID has to be a number
            sensor_id = input("Sensor ID: ")
            break
        except Exception:
            print("Incorrect ID.")

    while True:
        try:
            # Checking user input - Should not have any errors getting passed into the server
            user_input = input("Input action: ")
            if user_input[0] in "+-":
                quantity = int(user_input[1:-1])
                if user_input[0] == "+" and user_input[-1] == "W":
                    client_total_power += quantity
                    print("Local power:", client_total_power, "W")
                    print(send_message(host, port, user_input, sensor_id))
                elif user_input[0] == "-" and user_input[-1] == "W":
                    if client_total_power - quantity < 0:
                        raise ValueError
                    else:
                        client_total_power -= quantity
                        print("Local power:", client_total_power, "W")
                        print(send_message(host, port, user_input, sensor_id))
                else:
                    raise ValueError
            elif user_input == "exit":
                print(send_message(host, port, user_input, sensor_id))
                exit()
            else:
                raise ValueError
        except ValueError:
            print("Invalid command")
            continue


if __name__ == "__main__":
    main()
