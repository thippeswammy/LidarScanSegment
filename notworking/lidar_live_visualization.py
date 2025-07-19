import socket

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Replace with the IP and port of your SICK LiDAR
LIDAR_IP = "192.168.0.168"  # example IP
LIDAR_PORT = 2112  # common port for SICK LiDARs


def connect_lidar(ip, port):
    """Connect to the LiDAR sensor."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    return sock


def send_command(sock, command):
    """Send command to LiDAR."""
    sock.send(command.encode('ascii'))
    response = sock.recv(4096)  # Adjust buffer size as needed
    return response


def parse_data(data):
    """Parse LiDAR data into polar coordinates (angle, distance)."""
    # Implement parsing based on SICK's data protocol.
    # Here's a placeholder example to simulate data.
    # Replace this with actual parsing code according to your LiDAR's protocol.
    num_points = 360
    angles = np.linspace(0, 2 * np.pi, num_points)  # 0 to 360 degrees in radians
    distances = np.random.uniform(0.5, 10.0, num_points)  # Random distances for demo
    return angles, distances


def update_plot(frame, sock, scatter):
    """Update plot with new LiDAR data."""
    data_command = "\x02sRN LMDscandata\x03"  # replace as per your sensor protocol
    response = send_command(sock, data_command)

    angles, distances = parse_data(response)  # Parse polar coordinates

    # Convert polar to Cartesian coordinates for plotting
    x = distances * np.cos(angles)
    y = distances * np.sin(angles)

    scatter.set_offsets(np.c_[x, y])
    return scatter,


def main():
    sock = connect_lidar(LIDAR_IP, LIDAR_PORT)

    fig, ax = plt.subplots()
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    scatter = ax.scatter([], [], s=5, color='red')

    ani = FuncAnimation(fig, update_plot, fargs=(sock, scatter), interval=100, cache_frame_data=False)
    plt.xlabel("X (meters)")
    plt.ylabel("Y (meters)")
    plt.title("Live LiDAR Data Visualization")
    plt.show()

    sock.close()


if __name__ == "__main__":
    main()
