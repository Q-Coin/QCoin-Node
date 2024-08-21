import socket
import json
import threading

class Client:
    def __init__(self, manager, host_ip: str, host_port: int, timeout: int = 10, max_retries: int = 5) -> None:
        self.manager = manager
        self.host_ip = host_ip
        self.host_port = host_port
        self.timeout = timeout
        self.max_retries = max_retries
        self.client_socket = None
        self.connected = False
        self.lock = threading.Lock()
        self.client_id = id(self)  # Unique ID for this client instance
        
    def _initialize_socket(self):
        """Initialize the client socket."""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(self.timeout)
    
    def connect(self):
        """Establish connection to the server."""
        self._initialize_socket()
        try:
            self.client_socket.connect((self.host_ip, self.host_port))
            self.connected = True
            print(f"Successfully connected to {self.host_ip}:{self.host_port}")
        except (socket.error, socket.timeout) as e:
            print(f"Error connecting to {self.host_ip}:{self.host_port}: {e}")
            self.connected = False
    
    def reconnect(self):
        """Attempt to reconnect to the server or request a new peer if reconnect fails."""
        retries = 0
        while retries < self.max_retries:
            with self.lock:
                if self.connected:
                    self.close()
                self.connect()
            
            if self.connected:
                return True
            
            retries += 1
            print(f"Reconnect attempt {retries}/{self.max_retries} failed. Requesting a new peer.")
            self.request_new_peer()

        print(f"Failed to reconnect after {self.max_retries} attempts. Exiting...")
        self.notify_manager_failure()
        return False

    def request_new_peer(self):
        """Request a new peer from the manager."""
        new_peer = self.manager.get_new_peer(self.client_id)  # Assuming manager provides this method
        if new_peer:
            self.host_ip, self.host_port = new_peer
            print(f"Received new peer: {self.host_ip}:{self.host_port}")
        else:
            print("No valid peer received from the manager. Exiting...")
            self.notify_manager_failure()

    def notify_manager_failure(self):
        """Notify the manager of failure and close the client."""
        self.manager.handle_client_failure(self.client_id)
        self.close()
    
    def send(self, data):
        """Send data to the server."""
        if not self.connected:
            print("Not connected. Attempting to connect...")
            if not self.reconnect():
                return

        try:
            serialized_data = json.dumps(data).encode()
            with self.lock:
                self.client_socket.sendall(serialized_data)
            print(f"Data sent to {self.host_ip}:{self.host_port}")
        except (socket.error, socket.timeout) as e:
            print(f"Error sending data to {self.host_ip}:{self.host_port}: {e}")
            self.reconnect()
    
    def receive(self):
        """Receive data from the server."""
        if not self.connected:
            print("Not connected. Attempting to connect...")
            if not self.reconnect():
                return None

        try:
            with self.lock:
                data = self.client_socket.recv(1024)
            print(f"Data received from {self.host_ip}:{self.host_port}")
            return json.loads(data)
        except (socket.error, socket.timeout) as e:
            print(f"Error receiving data from {self.host_ip}:{self.host_port}: {e}")
            self.reconnect()
            return None
    
    def close(self):
        """Close the connection."""
        if self.client_socket:
            try:
                self.client_socket.close()
            except socket.error as e:
                print(f"Error closing the socket: {e}")
            finally:
                self.connected = False
                print(f"Connection to {self.host_ip}:{self.host_port} closed.")
