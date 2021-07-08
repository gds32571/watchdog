# watchdog
The watchdog server program

The watchdog program (zerowd.py) runs on a RPi (the home automation server typically) and listens for TCP connections from various computers or applications.  When a connection is made, the program responds with a sequence number, then sends an MQTT message to the HA server.  The HA server uses these messages to display the status (an 'on' icon) of the computer/application in Home Assistant. If a computer/application goes more than 75 (or some configured value) seconds without making a connection, the watchdog sends an 'off' MQTT message to HA which then displays an 'off' icon.

The original version of these programs require a custom copy of deadman on each client computer to identify the port to use.  Now each client can configure itself based on UDP messages exchanged with the watchdog server

## zerowd.sh

Shell script that starts everything on the watchdog computer.  It uses the following components.

### bcast-recv

The program bcast-recv listens for UDP broadcasts to port 12345 (or port 12344) from deadman clients.  They are needing the watchdog server hostname. This program responds with a UDP packet back to the querying comuter with that name.  The watchdog progran can run on different computers, it just listens on a different port.

### zerowd.py

This program runs in different modes, depending on the command line parameter used to start it. As a database server, it listens on port 2999 for a deadman client message.  Each client will send its hostname and ask which port to use.

As a server watchdog, it listens to a specific port, different for each client.  There will be many instances of this program running, each one listening to a different port of its client transmission.  It uses a TCP timer to wait for the deadman to transmit.  Then it uses MQTT to send the "up" message to Home Assistant.  The command line parameter is an index into an array with port numbers and timeout values.
