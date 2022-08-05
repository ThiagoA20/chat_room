import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '127.0.0.1'
PORT = 14532

server.bind((HOST, PORT))
server.listen()

print(f"Server escutando na porta: {PORT}")

clients = []
usernames = []

def sendMessage(message):
    for client in clients:
        client.send(message)

def handle(client, username):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            sendMessage(f"[{username}] {message}".encode('utf-8'))
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            usernames.remove(username)
            sendMessage(f"{username} desconectou do servidor.".encode('utf-8'))
            break

def receive():
    while True:
        client, address = server.accept()
        client.send("USERNAME".encode('utf-8'))
        username = client.recv(1024).decode('utf-8')
        usernames.append(username)

        print(f"O usuário {username} se conectou no servidor! endereço: {address}")
        sendMessage(f"{username} entrou no chat.".encode('utf-8'))
        clients.append(client)
        client.send("Conectado ao servidor".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client, username, ), daemon=True)
        thread.start()

receive()