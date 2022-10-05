import socket


def main():
    host = "127.0.0.1"
    port = 9999

    total_needed_power = 0
    current_usage = {}

    print(
        """
        ###########################################
        # Welcome to the server for the 5G sensor #
        ###########################################

        Receiving signals here:
        """
    )

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))  # localhost, port above 1023
            s.listen()
            connection, address = s.accept()
            with connection:
                # print("Connected by", address)
                decoded_data = connection.recv(1024).decode().split(",")
                sensor_id = decoded_data[1]

                if decoded_data[0] == "exit":
                    if sensor_id in current_usage.keys():
                        del current_usage[sensor_id]
                        print("Removed ID:", sensor_id, "for exiting.")
                        print("Breakdown of power usage:", current_usage)
                    else:
                        connection.send(bytes("Nothing to remove.", "utf-8"))

                if decoded_data[0][0] in "+-":
                    power_quantity = int(decoded_data[0][1:-1])
                    print(f"Received request of {decoded_data[0]} by ID: {sensor_id}")

                    if sensor_id not in current_usage.keys():
                        current_usage[sensor_id] = 0
                        current_usage = dict(sorted(current_usage.items()))

                    if decoded_data[0][0] == "+":
                        total_needed_power += power_quantity
                        current_usage[sensor_id] += power_quantity
                    else:
                        total_needed_power -= power_quantity
                        current_usage[sensor_id] -= power_quantity

                    if current_usage[sensor_id] == 0:
                        del current_usage[sensor_id]
                        current_usage = dict(sorted(current_usage.items()))

                    print("Total power is now", total_needed_power, "W")
                    print("Breakdown of power usage:", current_usage)

                    connection.send(
                        bytes(
                            f"Request of {decoded_data[0]} by ID: {sensor_id} was completed",
                            "utf-8",
                        )
                    )


if __name__ == "__main__":
    main()
