import socket
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5555))
    # Authentication
    response = client.recv(1024).decode()
    print(response)
    username = input()
    client.send(username.encode())
    response = client.recv(1024).decode()
    print(response)
    password = input()
    client.send(password.encode())
    response = client.recv(1024).decode()
    print(response)
    while True:
        print("Options:")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            client.send("check_balance".encode())
            balance = client.recv(1024).decode()
            print(balance)
        elif choice == '2':
            amount = float(input("Enter amount to deposit: "))
            client.send(f"deposit {amount}".encode())
            response = client.recv(1024).decode()
            print(response)
        elif choice == '3':
            amount = float(input("Enter amount to withdraw: "))
            client.send(f"withdraw {amount}".encode())
            response = client.recv(1024).decode()
            print(response)
        elif choice == '4':
            client.send("exit".encode())
            print("Exiting.")
            break
        else:
            print("Invalid choice.")
    client.close()

if __name__ == "__main__":
    main()
