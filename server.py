import socket


class Server:
    __total_needed_power = 0
    __current_usage = {}
    __backup_network = {}

    # Given an action, return the new power that this sensor is using
    def modify_power_draw(self, action, power_quantity, sensor_id):
        if action == "+":
            self.__total_needed_power += power_quantity
            self.__current_usage[sensor_id] += power_quantity
        else:
            self.__total_needed_power -= power_quantity
            self.__current_usage[sensor_id] -= power_quantity

    # Returned an ordered dict based off the key names
    def order_dict(self):
        self.__current_usage = dict(sorted(self.__current_usage.items()))

    # Remove an element from a dict and return a new sorted dict
    def remove_from_dict(self, sensor_id):
        del self.__current_usage[sensor_id]
        self.order_dict()

    def main(self):
        while True:
            # Opens the port at the given host, port has to be above 1023
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("127.0.0.1", 9999))
                s.listen()
                connection, address = s.accept()
                with connection:
                    print("Connected by", address)

                    # Decoded data
                    decoded_data = connection.recv(1024).decode().split(",")
                    sensor_id = decoded_data[1]

                    # If the sensor is shutting down
                    if decoded_data[0] == "exit":
                        # If it exists, then remove from __current_usage and update __total_needed_power
                        print(
                            f"Received request of {decoded_data[0]} by ID: {sensor_id}"
                        )
                        if sensor_id in self.__current_usage.keys():
                            self.remove_from_dict(sensor_id)
                            self.__total_needed_power = sum(self.__current_usage.values()) + sum(self.__backup_network.values())
                            self.__backup_network[sensor_id] = 7500
                            print("Removed ID:", sensor_id, "for exiting.")
                            print("Breakdown of power usage:", self.__current_usage)
                            print("Backup Network:", self.__backup_network)
                        else:
                            connection.send(bytes("Nothing to remove.", "utf-8"))
                            print("Backup Network:", self.__backup_network)

                    # If the command is requesting a difference in power draw
                    elif decoded_data[0][0] in "+-":
                        print(
                            f"Received request of {decoded_data[0]} by ID: {sensor_id}"
                        )
                        # Removing the first and last character to expose the number
                        power_quantity = int(decoded_data[0][1:-1])

                        # Creates a dict entry if the sensor does not have one already
                        if sensor_id not in self.__current_usage.keys():
                            self.__current_usage[sensor_id] = 0
                            self.order_dict()

                        # Updates the __total_needed_power as well as the power draw for the sensor in the dict
                        self.modify_power_draw(
                            decoded_data[0][0], power_quantity, sensor_id
                        )

                        # If it is not currently using power, remove it from the dict
                        if self.__current_usage[sensor_id] == 0:
                            self.remove_from_dict(sensor_id)

                        # Output
                        print("Total power is now", self.__total_needed_power, "W")
                        print("Breakdown of power usage:", self.__current_usage)
                        print("Backup Network:", self.__backup_network)

                        # Send connection success
                        connection.send(
                            bytes(
                                f"Request of {decoded_data[0]} by ID: {sensor_id} was completed",
                                "utf-8",
                            )
                        )


if __name__ == "__main__":
    print(
        """
        ###########################################
        # Welcome to the server for the 5G sensor #
        ###########################################

        """
    )
    print("Receiving signals here:")

    Server().main()
