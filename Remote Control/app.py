from kivy.app import App
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.label import Label 
from kivy.uix.image import Image 
from kivy.uix.button import Button 
from kivy.uix.textinput import TextInput
from kivy.clock import mainthread, Clock
from kivy.uix.widget import Widget
import socket
import time
import Action
import threading

robot_ip = "127.0.0.1"
robot_port = 12342
send_cond = True 

robot_id = 1

def send(action:Action):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    msg:bytes = action.encode()
    remote_socket.sendto(msg,(robot_ip, robot_port))
    print(f'sending Action {action}')


def listen():
    pass


class MyRemote(Widget):
    

    def StartForward(self):
        Clock.schedule_interval(self.movingForward, 0.01)
        
    def StopForward(self):
        Clock.unschedule(self.movingForward)

    def StartBackward(self):
        Clock.schedule_interval(self.movingBackward, 0.01)

    def StopBackward(self):
        Clock.unschedule(self.movingBackward)
    
    def StartLeft(self):
        Clock.schedule_interval(self.movingLeft, 0.01)

    def StopLeft(self):
        Clock.unschedule(self.movingLeft)

    def StartRight(self):
        Clock.schedule_interval(self.movingRight, 0.01)

    def StopRight(self):
        Clock.unschedule(self.movingRight)

    def movingForward(self, dt):
        action = Action.Action(robot_id=robot_id, vy = 5)
        send(action)
        # print(f'{action}')
    
    def movingBackward(self, dt):
        action = Action.Action(robot_id=robot_id , vy = -5)
        send(action)
        # print(f'{action}')
    
    def movingLeft(self, dt):
        action = Action.Action(robot_id=robot_id , vx = -5)
        send(action)
        # print(f'{action}')
    
    def movingRight(self, dt):
        action = Action.Action(robot_id=robot_id, vx = 5)
        send(action)
        # print(f'{action}')

    



class MyApp(App):
    def build(self):
        return MyRemote()
    
if __name__ == "__main__":
   MyApp().run()


    

