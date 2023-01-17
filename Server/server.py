import socket, threading
host = socket.gethostname()
port = 4000

clients = {}
addresses = {}
print(host)
print("Server est prés...")
serverRunning = True


while True:
    conn,addr = s.accept()
    conn.send("Enter le nom d'\utilisateur: ".encode("utf8"))
    print("%s:%s has connected." % addr)
    addresses[conn] = addr
    print(conn,addr)


class ClientHandler(threading.Thread):
    def __init__(self,conn,addr):
        self.conn = conn
        self.addr = conn
        pass
    
    def client_demande_data(self):
        pass
    def client_choose_room(self,client,room):
        pass
    def client_choose_client(self,client1,client2):
        pass
    def client_send_msg_to_room(self,client,room,message):
        pass
    # the main program for the handler
    def run():
        pass
    def quit():
        pass
    

class Server(threading.Thread):
    def __init__(self,host,port):
        self.host = host
        self.port = port 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host,port))
        s.listen()
    def run():
        while True:
            with self.lock:
                try:
                    connection, address = self.sock.accept()
                except socket.error:
                    time.sleep(0.05)
                    continue

            connection.setblocking(False)
            if connection not in self.connection_list:
                self.connection_list.append(connection)

            self.message_queues[connection] = queue.Queue()
            