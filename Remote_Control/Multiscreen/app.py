from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import socket
from Action import Action

Window.clearcolor = (1, 1, 1, 1)  # Set background color to white

INTERVAL = 0.05  # Interval for robot movement updates

class WindowManager(ScreenManager):
    pass

class Setup(Screen):
    def update_ip(self):
        new_ip = self.ids.ip_input.text.strip()
        if new_ip:
            self.manager.get_screen('myremote').update_ip(new_ip)
            print(f"Updated IP to: {new_ip}")
            self.manager.current = 'myremote'  # Switch to MyRemote screen


class MyRemote(Screen):
    DRIBBLE = False
    robot_ip = "192.168.200.243"
    robot_port = 50514
    robot_id = 1
    SPEED = 10

    def update_ip(self, new_ip):
        self.robot_ip = new_ip
        print(f"Robot IP updated to: {self.robot_ip}")

    def update_robot_id(self):
        new_robot_id = self.ids.robot_id_input.text.strip()
        if new_robot_id:
            self.robot_id = int(new_robot_id)
            print(f"Updated Robot ID to: {self.robot_id}")
        else:
            print("Invalid Robot ID. Please enter a valid integer.")

    def send(self, action: Action):
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg: bytes = action.encode()
        remote_socket.sendto(msg, (self.robot_ip, self.robot_port))
        print(f'Sending Action {action} to IP {self.robot_ip}')

    def start_action(self, action_method, *args):
        Clock.schedule_interval(action_method, INTERVAL)

    def stop_action(self, action_method, *args):
        Clock.unschedule(action_method)

    def movingForward(self, dt):
        self.send(Action(robot_id=self.robot_id, vy=self.SPEED))

    def movingBackward(self, dt):
        self.send(Action(robot_id=self.robot_id, vy=-self.SPEED))

    def movingLeft(self, dt):
        self.send(Action(robot_id=self.robot_id, vx=-self.SPEED))

    def movingRight(self, dt):
        self.send(Action(robot_id=self.robot_id, vx=self.SPEED))

    def turnRight(self, dt):
        self.send(Action(robot_id=self.robot_id, w=0.5))

    def turnLeft(self, dt):
        self.send(Action(robot_id=self.robot_id, w=-0.5))

    def kick(self, dt):
        self.send(Action(robot_id=self.robot_id, kick=1))

    def dribble(self, dt):
        dribble_action = 1 if self.DRIBBLE else 0
        self.send(Action(robot_id=self.robot_id, dribble=dribble_action))

    def toggle_dribble(self):
        self.DRIBBLE = not self.DRIBBLE
        if self.DRIBBLE:
            Clock.schedule_interval(self.dribble, INTERVAL)
        else:
            Clock.unschedule(self.dribble)
        print(f"Dribble toggled: {self.DRIBBLE}")

    def stop(self):
        self.send(Action(robot_id=self.robot_id, vx=0., vy=0., w=0.))


# Load the KV file after defining all the necessary classes
kv = Builder.load_file("my.kv")

class MyApp(App):
    def build(self):
        self.title = "Remote"
        return kv


if __name__ == "__main__":
    MyApp().run()
