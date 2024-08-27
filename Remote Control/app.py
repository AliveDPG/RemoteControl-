from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label  # Import Label
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.core.window import Window
import socket
import Action

Window.clearcolor = (1, 1, 1, 1)  # changes the colour of the background to white 

robot_ip = "192.168.200.243"
robot_port = 50514
robot_id = 1

def send(action: Action):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    msg: bytes = action.encode()
    remote_socket.sendto(msg, (robot_ip, robot_port))
    print(f'sending Action {action}')

class MyRemote(FloatLayout):

    def __init__(self, **kwargs):
        super(MyRemote, self).__init__(**kwargs)
        
        self.label = Label(
            text="Remote Control",  
            size_hint=(None, None),  
            pos_hint={'center_x': 0.5, 'top': 1})  
        
        self.add_widget(self.label)

    def StartForward(self, instance):
        Clock.schedule_interval(self.movingForward, 0.05)

    def StopForward(self, instance):
        Clock.unschedule(self.movingForward)

    def StartBackward(self, instance):
        Clock.schedule_interval(self.movingBackward, 0.05)

    def StopBackward(self, instance):
        Clock.unschedule(self.movingBackward)

    def StartLeft(self, instance):
        Clock.schedule_interval(self.movingLeft, 0.05)

    def StopLeft(self, instance):
        Clock.unschedule(self.movingLeft)

    def StartRight(self, instance):
        Clock.schedule_interval(self.movingRight, 0.05)

    def StopRight(self, instance):
        Clock.unschedule(self.movingRight)

    def movingForward(self, dt):
        action = Action.Action(robot_id=robot_id, vy=5)
        send(action)

    def movingBackward(self, dt):
        action = Action.Action(robot_id=robot_id, vy=-5)
        send(action)

    def movingLeft(self, dt):
        action = Action.Action(robot_id=robot_id, vx=-5)
        send(action)

    def movingRight(self, dt):
        action = Action.Action(robot_id=robot_id, vx=5)
        send(action)


class MyApp(App):
    def build(self):
        return MyRemote()


if __name__ == "__main__":
    MyApp().run()
