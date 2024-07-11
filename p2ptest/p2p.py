import socket
import threading
import json
import time

def handle_peer_connection(peer_socket, peer_type):
    buffer = ""
    while True:
        try:
            data = peer_socket.recv(1024).decode('utf-8')
            if data:
                buffer += data
                while '\n' in buffer:
                    message, buffer = buffer.split('\n', 1)
                    handle_json_rpc(peer_socket, message, peer_type)
            else:
                break
        except Exception as e:
            print(f"Error ({peer_type}): {e}")
            break

def handle_json_rpc(peer_socket, data, peer_type):
    try:
        message = json.loads(data)
        if 'method' in message and 'params' in message and 'id' in message:
            # C'est une requête JSON-RPC
            method = message['method']
            params = message['params']
            request_id = message['id']
            response = {
                'jsonrpc': '2.0',
                'id': request_id
            }

            if method == 'echo':
                response['result'] = params
                print(f"{peer_type} received: {params}")
                peer_socket.sendall((json.dumps(response) + '\n').encode('utf-8'))

                time.sleep(1)  # Pause de 1 seconde avant de renvoyer un message

                if peer_type == "Server":
                    send_hello_world(peer_socket, request_id + 1)
            else:
                response['error'] = {'code': -32601, 'message': 'Method not found'}
                peer_socket.sendall((json.dumps(response) + '\n').encode('utf-8'))
        elif 'result' in message or 'error' in message:
            # C'est une réponse JSON-RPC
            print(f"{peer_type} received response: {message}")
            if peer_type == "Client":
                time.sleep(1)  # Pause de 1 seconde avant d'envoyer un nouveau message
                send_hello_world(peer_socket, message['id'] + 1)
        else:
            raise ValueError("Invalid JSON-RPC message")
    except Exception as e:
        error_response = {
            'jsonrpc': '2.0',
            'error': {'code': -32600, 'message': 'Invalid Request'},
            'id': None
        }
        peer_socket.sendall((json.dumps(error_response) + '\n').encode('utf-8'))
        print(f"Error handling JSON-RPC message: {e}")

def send_hello_world(peer_socket, request_id):
    message = json.dumps({
        'jsonrpc': '2.0',
        'method': 'echo',
        'params': 'hello world',
        'id': request_id
    }) + '\n'
    peer_socket.sendall(message.encode('utf-8'))
    print(f"Message sent: hello world")

def connect_to_peer(peer_host, peer_port, peer_type):
    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer_socket.connect((peer_host, peer_port))
    threading.Thread(target=handle_peer_connection, args=(peer_socket, peer_type)).start()
    return peer_socket

def start_server(server_host, server_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen(5)
    print(f"Listening on {server_host}:{server_port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        threading.Thread(target=handle_peer_connection, args=(client_socket, "Server")).start()

def start_client(server_host, server_port):
    client_socket = connect_to_peer(server_host, server_port, "Client")
    send_hello_world(client_socket, 1)

def main():
    server_host = 'localhost'
    server_port = 12345

    server_thread = threading.Thread(target=start_server, args=(server_host, server_port))
    server_thread.start()

    client_thread = threading.Thread(target=start_client, args=(server_host, server_port))
    client_thread.start()

    client_thread.join()

if __name__ == '__main__':
    main()
