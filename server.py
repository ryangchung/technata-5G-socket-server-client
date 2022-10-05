import socket


class Server:
    total_needed_power = 0
    current_usage = {}

    # Given an action, return the new power that this sensor is using
    def modify_power_draw(self, action, power_quantity, sensor_id):
        if action == "+":
            self.total_needed_power += power_quantity
            self.current_usage[sensor_id] += power_quantity
        else:
            self.total_needed_power -= power_quantity
            self.current_usage[sensor_id] -= power_quantity

    # Returned an ordered dict based off the key names
    def order_dict(self):
        self.current_usage = dict(sorted(self.current_usage.items()))

    # Remove an element from a dict and return a new sorted dict
    def remove_from_dict(self, sensor_id):
        del self.current_usage[sensor_id]
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
                    print(sensor_id)

                    # If the sensor is shutting down
                    if decoded_data[0] == "exit":
                        # If it exists, then remove from current_usage and update total_needed_power
                        print(
                            f"Received request of {decoded_data[0]} by ID: {sensor_id}"
                        )
                        if sensor_id in self.current_usage.keys():
                            self.current_usage = self.remove_from_dict(sensor_id)
                            self.total_needed_power = sum(self.current_usage.values())
                            print("Removed ID:", sensor_id, "for exiting.")
                            print("Breakdown of power usage:", self.current_usage)
                        else:
                            connection.send(bytes("Nothing to remove.", "utf-8"))

                    # If the command is requesting a difference in power draw
                    elif decoded_data[0][0] in "+-":
                        print(
                            f"Received request of {decoded_data[0]} by ID: {sensor_id}"
                        )
                        # Removing the first and last character to expose the number
                        power_quantity = int(decoded_data[0][1:-1])

                        # Creates a dict entry if the sensor does not have one already
                        if sensor_id not in self.current_usage.keys():
                            self.current_usage[sensor_id] = 0
                            self.order_dict()

                        # Updates the total_needed_power as well as the power draw for the sensor in the dict
                        self.modify_power_draw(
                            decoded_data[0][0], power_quantity, sensor_id
                        )

                        # If it is not currently using power, remove it from the dict
                        if self.current_usage[sensor_id] == 0:
                            self.remove_from_dict(sensor_id)

                        # Output
                        print("Total power is now", self.total_needed_power, "W")
                        print("Breakdown of power usage:", self.current_usage)

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
