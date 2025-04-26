"""
Utility functions for server operations.
"""
import socket

def find_available_port(start_port=5000, max_attempts=10):
    """
    Find an available port for the server to listen on.
    
    Args:
        start_port (int): The port to start checking from
        max_attempts (int): Maximum number of ports to check
        
    Returns:
        int: An available port number
        
    Raises:
        RuntimeError: If no available port is found after max_attempts
    """
    for port in range(start_port, start_port + max_attempts):
        try:
            # Try to create a socket on the port
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except socket.error:
            print(f"Port {port} is already in use, trying next port...")
            continue
    # If we get here, no ports were available
    raise RuntimeError(f"Could not find an available port after {max_attempts} attempts")