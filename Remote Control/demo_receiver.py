"""This pretends it receives the messages as the robot."""
import socket
from Action import Action

def main(): 
    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recv_sock.bind(("127.0.0.1", 12342))
    while True:
        data,_ = recv_sock.recvfrom(2048)
        action = Action.decode(data)
        print(action)
        
if __name__ =="__main__":
    main()