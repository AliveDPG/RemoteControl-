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

INTERVAL = 0.05 # second

class MyRemote(FloatLayout):
    DRIBBLE= False
    robot_ip = "192.168.200.243"
    robot_port = 50514
    robot_id = 1

    def send(self,action: Action):
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg: bytes = action.encode()
        remote_socket.sendto(msg, (self.robot_ip, self.robot_port))
        print(f'sending Action {action}')
        
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
        action = Action(robot_id=self.robot_id, vy=5)
        self.send(action)

    def movingBackward(self, dt):
        action = Action(robot_id=self.robot_id, vy=-5)
        self.send(action)

    def movingLeft(self, dt):
        action = Action(robot_id=self.robot_id, vx=-5)
        self.send(action)

    def movingRight(self, dt):
        action = Action(robot_id=self.robot_id, vx=5)
        self.send(action)
    
    def turnRight(self,dt):
        action = Action(robot_id=self.robot_id,w=0.5)
        self.send(action)
        
    def turnLeft(self,dt):
        action = Action(robot_id=self.robot_id,w=-0.5)
        self.send(action)
    
    def kick(self, dt):
        action = Action(robot_id=self.robot_id,kick=1)
        self.send(action)
        
    def dribble(self,dt):
        d = toggle(self.DRIBBLE)
        if d is True:
            action = Action(robot_id=self.robot_id, dribble=1)
        else:
            action = Action(robot_id=self.robot_id,dribble=0)
        self.send(action)

def toggle(d):
    if d is False:
        d = True
    elif d is True:
        d = False
    return d

class MyApp(App):
    def build(self):
        return MyRemote()


if __name__ == "__main__":
    MyApp().run()
