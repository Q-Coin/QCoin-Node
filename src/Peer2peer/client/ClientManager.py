import threading

class Manager:
    def __init__(self):
        self.peers = []  # List of available peers as tuples (host_ip, host_port)
        self.active_clients = {}  # Dictionary to track active clients {client_id: (host_ip, host_port)}
        self.lock = threading.Lock()
    
    def add_peer(self, host_ip: str, host_port: int):
        """Add a new peer to the pool."""
        with self.lock:
            self.peers.append((host_ip, host_port))
            print(f"Peer added: {host_ip}:{host_port}")
    
    def get_new_peer(self, client_id: int):
        """Provide a new peer to a client."""
        with self.lock:
            if self.peers:
                # Check if client is already assigned to a peer
                if client_id in self.active_clients:
                    print(f"Client {client_id} is switching to a new peer.")
                
                # Assign a new peer to the client
                new_peer = self.peers.pop(0)
                self.active_clients[client_id] = new_peer
                print(f"Assigned peer {new_peer[0]}:{new_peer[1]} to client {client_id}")
                return new_peer
            else:
                print("No peers available.")
                return None
    
    def handle_client_failure(self, client_id: int):
        """Handle a client's failure and clean up."""
        with self.lock:
            if client_id in self.active_clients:
                print(f"Client {client_id} reported failure. Cleaning up.")
                del self.active_clients[client_id]
            else:
                print(f"Unknown client {client_id} reported failure.")
    
    def remove_peer(self, host_ip: str, host_port: int):
        """Remove a peer from the pool."""
        with self.lock:
            peer = (host_ip, host_port)
            if peer in self.peers:
                self.peers.remove(peer)
                print(f"Peer removed: {host_ip}:{host_port}")
            else:
                print(f"Peer {host_ip}:{host_port} not found in the pool.")
    
    def list_active_clients(self):
        """List all active clients and their assigned peers."""
        with self.lock:
            for client_id, peer in self.active_clients.items():
                print(f"Client {client_id} is connected to {peer[0]}:{peer[1]}")
    
    def list_available_peers(self):
        """List all available peers."""
        with self.lock:
            if self.peers:
                print("Available peers:")
                for peer in self.peers:
                    print(f" - {peer[0]}:{peer[1]}")
            else:
                print("No peers available.")
