import socket
from bulgaria_weather_map.utils.server import find_available_port

def test_find_available_port():
    """Test the port-finding logic from the server utility module"""

    # First, find an available port
    port1 = find_available_port()
    print(f"Found available port: {port1}")

    # Now occupy that port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', port1))
    sock.listen(1)

    try:
        # Try to find another port - should skip the occupied one
        port2 = find_available_port()
        print(f"Found second available port: {port2}")

        # Verify the ports are different
        assert port1 != port2, f"Expected different ports, but got {port1} twice"
        print("Test passed: Port finder correctly skips occupied ports")
    finally:
        # Clean up
        sock.close()

if __name__ == "__main__":
    test_find_available_port()
