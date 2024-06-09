import socket
import threading
# Sample account details stored on the server
accounts = {
    'user1': {'balance': 1000, 'password': '111'},
    'user2': {'balance': 2000, 'password': '222'}
}
# Function to handle client requests
def handle_client(client_socket):
    # Authentication
    client_socket.send("Enter username: ".encode())
    username = client_socket.recv(1024).decode().strip()
    client_socket.send("Enter password: ".encode())
    password = client_socket.recv(1024).decode().strip()
    if username in accounts and accounts[username]['password'] == password:
        client_socket.send("Authentication successful.".encode())
    else:
        client_socket.send("Invalid credentials. Closing connection.".encode())
        client_socket.close()
        return
    while True:
        # Receive client requests
        request = client_socket.recv(1024).decode().strip()
        if request == "check_balance":
            balance = accounts[username]['balance']
            client_socket.send(f"Your balance is {balance}".encode())
        elif request.startswith("deposit"):
            amount = float(request.split()[1])
            accounts[username]['balance'] += amount
            client_socket.send("Deposit successful.".encode())
        elif request.startswith("withdraw"):
            amount = float(request.split()[1])
            if accounts[username]['balance'] >= amount:
                accounts[username]['balance'] -= amount
                client_socket.send("Withdrawal successful.".encode())
            else:
                client_socket.send("Insufficient funds.".encode())
        elif request == "exit":
            client_socket.send("Exiting.".encode())
            break
        else:
            client_socket.send("Invalid request.".encode())
    # Close client connection
    client_socket.close()
# Main server function
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5555))
    server.listen(5)
    print("[*] Listening on 127.0.0.1:5555")
    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        # Create a new thread to handle client requests
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()
if __name__ == "__main__":
    main()
