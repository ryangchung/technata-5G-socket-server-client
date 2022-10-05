import socket
from sys import exit

# Sends the message and sensor ID through the given socket
def send_message(message, sensor_id):
    host = "127.0.0.1"
    port = 9999

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(bytes(f"{message},{sensor_id}", "utf-8"))
        return s.recv(1024).decode()

# Given an action, return the new power that this sensor is using
def modify_power_draw(action, quantity, sensor_total_power):
    if action == "+":
        new_sensor_total_power = sensor_total_power + quantity
    else:
        new_sensor_total_power = sensor_total_power - quantity
    print("Local power:", new_sensor_total_power, "W")

    return new_sensor_total_power

def main():
    sensor_total_power = 0

    while True:
        try:
            sensor_id = input("Sensor ID: ")
            break
        except Exception:
            print("Incorrect ID.")

    while True:
        try:
            # Checking user input - Should not have any errors getting passed into the server
            user_input = input("Input action: ")
            if user_input[0] in "+-" and user_input[-1] == "W":
                quantity = int(user_input[1:-1])

                if user_input[0] == "-" and sensor_total_power - quantity < 0:
                    raise ValueError

                # Updating the power needed
                sensor_total_power = modify_power_draw(user_input[0], quantity, sensor_total_power)
                # Sending message to server
                print(send_message(user_input, sensor_id))
            elif user_input == "exit":
                # Sending message to server
                print(send_message(user_input, sensor_id))
                exit()
            else:
                raise ValueError
        except ValueError:
            print("Invalid command")
            continue


if __name__ == "__main__":
    print(
        """
        ###########################################
        # Welcome to the client for the 5G sensor #
        ###########################################

        """
    )

    main()
