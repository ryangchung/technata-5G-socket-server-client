import socket

# Given an action, return the new power that this sensor is using
def modify_power_draw(
    action, power_quantity, total_needed_power, current_usage, sensor_id
):
    new_current_usage = current_usage
    if action == "+":
        new_total_needed_power = total_needed_power + power_quantity
        new_current_usage[sensor_id] += power_quantity
    else:
        new_total_needed_power = total_needed_power - power_quantity
        new_current_usage[sensor_id] -= power_quantity

    return new_total_needed_power, new_current_usage


# Returned an ordered dict based off the key names
def order_dict(dictionary):
    return dict(sorted(dictionary.items()))


# Remove an element from a dict and return a new sorted dict
def remove_from_dict(dictionary, sensor_id):
    new_dictionary = dictionary
    del new_dictionary[sensor_id]
    return order_dict(dictionary)


def main():
    total_needed_power = 0
    current_usage = {}

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
                    # If it exists, then remove from current_usage and update total_needed_power
                    print(f"Received request of {decoded_data[0]} by ID: {sensor_id}")
                    if sensor_id in current_usage.keys():
                        current_usage = remove_from_dict(current_usage, sensor_id)
                        total_needed_power = sum(current_usage.values())
                        print("Removed ID:", sensor_id, "for exiting.")
                        print("Breakdown of power usage:", current_usage)
                    else:
                        connection.send(bytes("Nothing to remove.", "utf-8"))

                # If the command is requesting a difference in power draw
                elif decoded_data[0][0] in "+-":
                    print(f"Received request of {decoded_data[0]} by ID: {sensor_id}")
                    # Removing the first and last character to expose the number
                    power_quantity = int(decoded_data[0][1:-1])

                    # Creates a dict entry if the sensor does not have one already
                    if sensor_id not in current_usage.keys():
                        current_usage[sensor_id] = 0
                        current_usage = order_dict(current_usage)

                    # Updates the total_needed_power as well as the power draw for the sensor in the dict
                    total_needed_power, current_usage = modify_power_draw(
                        decoded_data[0][0],
                        power_quantity,
                        total_needed_power,
                        current_usage,
                        sensor_id,
                    )

                    # If it is not currently using power, remove it from the dict
                    if current_usage[sensor_id] == 0:
                        current_usage = remove_from_dict(current_usage, sensor_id)

                    # Output
                    print("Total power is now", total_needed_power, "W")
                    print("Breakdown of power usage:", current_usage, )

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

    main()
