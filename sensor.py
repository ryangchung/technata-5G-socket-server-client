import socket
from sys import exit


class Sensor:
    __sensor_total_power = 0
    __sensor_id = None

    def __init__(self):
        while True:
            try:
                self.__sensor_id = input("Sensor ID: ")
                break
            except Exception:
                print("Incorrect ID.")
        self.accept_commands()

    # Sends the message and sensor ID through the given socket
    def send_message(self, message):
        host = "127.0.0.1"
        port = 9999

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(bytes(f"{message},{self.__sensor_id}", "utf-8"))
            return s.recv(1024).decode()

    # Given an action, return the new power that this sensor is using
    def modify_power_draw(self, action, quantity):
        if action == "+":
            self.__sensor_total_power += quantity
        else:
            self.__sensor_total_power += -quantity
        print("Local power:", self.__sensor_total_power, "W")

    def accept_commands(self):
        while True:
            try:
                # Checking user input - Should not have any errors getting passed into the server
                user_input = input("Input action: ")
                if user_input[0] in "+-" and user_input[-1] == "W":
                    quantity = int(user_input[1:-1])

                    if user_input[0] == "-" and self.__sensor_total_power - quantity < 0:
                        raise ValueError

                    # Updating the power needed
                    self.modify_power_draw(user_input[0], quantity)
                    # Sending message to server
                    print(self.send_message(user_input))
                elif user_input == "exit":
                    # Sending message to server
                    print(self.send_message(user_input))
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

    Sensor()
