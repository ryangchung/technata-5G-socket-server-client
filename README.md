# technata-hacks-python-backend

## Objective
This project was part of a team pitch for the Technata Hacks 2022 Hackathon. The project was awarded 4th place.
This is a socket programming project aimed at being a proof of concept of the underlying features of our project, explained below.

## Project
The hackathon was to find a solution for water and electricity waste using 5G. The focus of the project was the electricity waste side of the prompt.

On average, 10% of power is lost from the power grid during distribution to the end user. However, the current system sends a constant stream of power that will never be fully utilized. By limiting the amount of power sent overall to the buildings to what is actually needed, the 10% of power lost would be a great saving. Using URLLC, a very reliable subset of 5G, requests would be able to be transmitted in real time using a 1-10 millisecond latency.

## Proof of Concept
This proof of concept focuses on what would happen internally within the sensor, with user input being an abstraction of the power load tracking. It sends a ping in real time to the socket server and receives feedback from the server aknowledging the request.

## Commands
Requesting Power: +<number>W
Releasing Power: -<number>W
Exit (simulating failure or offline sensor): exit

## How to use
1. Clone the repository.
2. Open two or more terminals, running the server.py and sensor.py files in each terminal.
