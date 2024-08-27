from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label  # Import Label
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.core.window import Window
import socket
from Action import Action

class IpId(BoxLayout):
    pass

Window.clearcolor = (1, 1, 1, 1)  # changes the colour of the background to white 

robot_ip = "192.168.200.243"
robot_port = 50514
robot_id = 1
DRIBBLE = False
INTERVAL = 0.05 # second

def send(action: Action):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    msg: bytes = action.encode()
    remote_socket.sendto(msg, (robot_ip, robot_port))
    print(f'sending Action {action}')

class MyRemote(FloatLayout):
    def StartForward(self, instance):
        Clock.schedule_interval(self.movingForward, INTERVAL)

    def StopForward(self, instance):
        Clock.unschedule(self.movingForward)

    def StartBackward(self, instance):
        Clock.schedule_interval(self.movingBackward, INTERVAL)

    def StopBackward(self, instance):
        Clock.unschedule(self.movingBackward)

    def StartLeft(self, instance):
        Clock.schedule_interval(self.movingLeft, INTERVAL)

    def StopLeft(self, instance):
        Clock.unschedule(self.movingLeft)

    def StartRight(self, instance):
        Clock.schedule_interval(self.movingRight, INTERVAL)

    def StopRight(self, instance):
        Clock.unschedule(self.movingRight)
    
    def StartTurningRight(self,instance):
        Clock.schedule_interval(self.turnRight,INTERVAL)
    
    def StartTurningLeft(self,instance):
        Clock.schedule_interval(self.turnLeft,INTERVAL)
    
    def StopTurningRight(self,instance):
        Clock.unschedule(self.turnRight)
        
    def StopTurningLeft(self,instance):
        Clock.unschedule(self.turnLeft)

    def StartKick(self,instance):
        Clock.schedule_interval(self.kick,INTERVAL)

    def ToggleDribble(self,instance):
        Clock.schedule_interval(self.dribble,INTERVAL)
    

    def movingForward(self, dt):
        action = Action(robot_id=robot_id, vy=5)
        send(action)

    def movingBackward(self, dt):
        action = Action(robot_id=robot_id, vy=-5)
        send(action)

    def movingLeft(self, dt):
        action = Action(robot_id=robot_id, vx=-5)
        send(action)

    def movingRight(self, dt):
        action = Action(robot_id=robot_id, vx=5)
        send(action)
    
    def turnRight(self,dt):
        action = Action(robot_id,w=0.5)
        send(action)
        
    def turnLeft(self,dt):
        action = Action(robot_id,w=-0.5)
        send(action)
    
    def kick(self, dt):
        action = Action(robot_id,k=1)
        send(action)
        
    def dribble(self,dt):
        d = toggle()
        if d is True:
            action = Action(robot_id, d=1)
        else:
            action = Action(robot_id,d=0)
        send(action)

def toggle():
    if DRIBBLE is False:
        DRIBBLE = True
    elif DRIBBLE is True:
        DRIBBLE = False
    return DRIBBLE

class MyApp(App):
    def build(self):
        return MyRemote()


if __name__ == "__main__":
    MyApp().run()
