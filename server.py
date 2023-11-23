import socket
import des

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
host = socket.gethostname()
port = 5050
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(1)
print(f"Server listening on {host}:{port}...")

# Wait for a connection from a client
print("Waiting for connection...")
client_socket, addr = server_socket.accept()
print(f"Got connection from: {addr}\n")

# Generate the round key
key = "A1B4C7D2E5F80913"
round_key = des.generate_round_key(key)

while True:
    # Receive data from the client
    data = client_socket.recv(1024)
    if not data:
        break
    data = data.decode('utf-8')
    print(f"Received from client: {data}")

    # Decrypt the message using DES
    data = des.decrypt(data, round_key)
    print(f"Decrypted message: {data}\n")

    # Get input from the user and validate it
    while True:
        message_to_send = input("Enter a message to send to the client: ")
        try:
            if not message_to_send:
                raise ValueError("please enter a non-empty message\n")
            if len(message_to_send) != 16:
                raise ValueError("please enter a 64-bit hex string\n")
            if not all(char in "0123456789ABCDEF" for char in message_to_send):
                raise ValueError("please enter a 64-bit hex string\n")
            break
        except ValueError as e:
            print("Error:", e)
            continue
    
    # Encrypt the message using DES
    message_to_send = des.encrypt(message_to_send, round_key)
    print(f"Encrypted message: {message_to_send}\n")

    # Send the message to the client
    client_socket.sendall(message_to_send.encode())