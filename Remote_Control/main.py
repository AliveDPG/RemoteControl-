from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
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
    SPEED = 20
    rotation = 0.1


    
    def __init__(self, **kwargs):
        super(MyRemote, self).__init__(**kwargs)
        self.ip_input = self.ids.ip_input  # Link the TextInput
        self.robot_id_input = self.ids.robot_id_input
        

    def update_robot_id(self):
        new_robot_id = self.robot_id_input.text.strip()
        if new_robot_id:  
            self.robot_id = int(new_robot_id)  
            print(f"Updated Robot ID to: {self.robot_id}")
        else:
            print("Invalid Robot ID. Please enter a valid integer.")


    def update_ip(self):
        new_ip = self.ip_input.text.strip()  # Get and strip the new IP from TextInput
        if new_ip:
            self.robot_ip = new_ip  # Update the instance variable
            print(f"Updated IP to: {self.robot_ip=}")

    def send(self, action: Action):
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg: bytes = action.encode()
        remote_socket.sendto(msg, (self.robot_ip, self.robot_port))
        print(f'Sending Action {action} to IP {self.robot_ip=}')

        
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
        self.DRIBBLE = toggle(self.DRIBBLE)
        Clock.schedule_interval(self.dribble,INTERVAL)
    
    def ExitDribble(self,instance):
        if self.DRIBBLE is False:
            Clock.unschedule(self.dribble)
    
    def Stop(self, instance):
        # if self.Stop is False:
        #     Clock.unschedule(self.Stop)
        action = Action(robot_id=self.robot_id, vx = 0., vy = 0. , w= 0. )
        self.send(action)
        

    def movingForward(self, dt):
        action = Action(robot_id=self.robot_id, vx=self.SPEED)
        self.send(action)

    def movingBackward(self, dt):
        action = Action(robot_id=self.robot_id, vx=-self.SPEED)
        self.send(action)

    def movingLeft(self, dt):
        action = Action(robot_id=self.robot_id, vy=-self.SPEED)
        self.send(action)

    def movingRight(self, dt):
        action = Action(robot_id=self.robot_id, vy=self.SPEED)
        self.send(action)
    
    def turnRight(self,dt):
        action = Action(robot_id=self.robot_id,w=self.rotation)
        self.send(action)
        
    def turnLeft(self,dt):
        action = Action(robot_id=self.robot_id,w=-self.rotation)
        self.send(action)
    
    def kick(self, dt):
        action = Action(robot_id=self.robot_id,kick=1)
        self.send(action)
        
    def dribble(self,dt):
       
        if self.DRIBBLE is True:
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
