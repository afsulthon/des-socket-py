import socket
import des

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
host = socket.gethostname()
port = 5050
client_socket.connect((host, port))

# Generate the round key
key = "A1B4C7D2E5F80913"
round_key = des.generate_round_key(key)

while True:
    # Get input from the user and validate it
    while True:
        message_to_send = input("Enter a message to send to the server: ")
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

    # Send the message to the server
    client_socket.sendall(message_to_send.encode())

    # Receive data from the server
    data = client_socket.recv(1024)
    if not data:
        break
    data = data.decode('utf-8')
    print(f"Received from server: {data}")

    # Decrypt the message using DES
    data = des.decrypt(data, round_key)
    print(f"Decrypted message: {data}\n")