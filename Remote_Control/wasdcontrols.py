import socket
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
import time
import threading 
from Action import Action

class WASDControls(FloatLayout):
    # Configuration
    robot_ip = "192.168.25.243"  # Replace with your robot's IP address
    robot_port = 50514             # Replace with your robot's listening port
    robot_id = 1
    SPEED = 50           # Movement speed
    ROTATION_SPEED = 0.1   
    DRIBBLE = False       # Rotation speed
    is_square_movement = False

    def __init__(self, **kwargs):
        super(WASDControls, self).__init__(**kwargs)
        # Bind the key press and release events
        Window.bind(on_key_down=self.on_keyboard_down)
        Window.bind(on_key_up=self.on_keyboard_up)
        # Create a persistent UDP socket
        self.remote_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f"Initialized UDP socket to {self.robot_ip}:{self.robot_port}")

    def send(self, action: Action):
        """Send an action to the robot via UDP."""
        try:
            msg: bytes = action.encode()
            self.remote_socket.sendto(msg, (self.robot_ip, self.robot_port))
            print(f"Sending Action {action} to IP {self.robot_ip}")
        except socket.error as e:
            print(f"Failed to send action: {e}")

    def on_keyboard_down(self, window, key, scancode, codepoint, modifiers):
        """Handle key press events."""
        if key == 119:  # W key (Move Forward)
            self.movingForward()
            time.sleep(0.05)
        elif key == 97:  # A key (Move Left)
            self.movingLeft()
            time.sleep(0.05)
        elif key == 115:  # S key (Move Backward)
            self.movingBackward()
            time.sleep(0.05)
        elif key == 100:  # D key (Move Right)
            self.movingRight()
            time.sleep(0.05)
        elif key == 113:  # Q key (Rotate Left)
            self.turnLeft()
            time.sleep(0.05)
        elif key == 101:  # E key (Rotate Right)
            self.turnRight()
            time.sleep(0.05)
        elif key == 32:
            self.DRIBBLE = toggle(self.DRIBBLE)
            print(self.DRIBBLE)
        elif key == 122: # z key for square movement 
            self.toggle_square_movement()

    def on_keyboard_up(self, window, key, scancode):
        """Handle key release events to stop the robot."""
        if key in (119, 97, 115, 100, 113, 101):
            self.stop()

    def movingForward(self):
        """Move the robot forward."""
        if self.DRIBBLE == True:
            action = Action(robot_id=self.robot_id, vx=self.SPEED, dribble=1)
        else:
            action = Action(robot_id=self.robot_id, vx=self.SPEED)
        self.send(action)

    def movingBackward(self):
        """Move the robot backward."""
        if self.DRIBBLE == True:
            action = Action(robot_id=self.robot_id, vx=-self.SPEED, dribble=1)
        else:
            action = Action(robot_id=self.robot_id, vx=-self.SPEED)
        self.send(action)

    def movingLeft(self):
        """Move the robot to the left."""
        if self.DRIBBLE == True:
            action = Action(robot_id=self.robot_id, vy=-self.SPEED, dribble=1)
        else:
            action = Action(robot_id=self.robot_id, vy=-self.SPEED)
        self.send(action)

    def movingRight(self):
        """Move the robot to the right."""
        if self.DRIBBLE == True:
            action = Action(robot_id=self.robot_id, vy=self.SPEED, dribble=1)
        else:
            action = Action(robot_id=self.robot_id, vy=self.SPEED)
        self.send(action)

    def turnLeft(self):
        """Rotate the robot to the left."""
        if self.DRIBBLE == True:
            action = Action(robot_id=self.robot_id, w=-self.ROTATION_SPEED, dribble=1)
        else:
            action = Action(robot_id=self.robot_id, w=-self.ROTATION_SPEED)
        self.send(action)

    def turnRight(self):
        """Rotate the robot to the right."""
        if self.DRIBBLE == True:
            action = Action(robot_id=self.robot_id, w=self.ROTATION_SPEED, dribble=1)
        else:
            action = Action(robot_id=self.robot_id, w=self.ROTATION_SPEED)
        self.send(action)

    def stop(self):
        """Stop all robot movement."""
        if self.DRIBBLE == True:
            action = Action(robot_id=self.robot_id, vx=0.0, vy=0.0, w=0.0, dribble=1)
        else:
            action = Action(robot_id=self.robot_id, vx=0.0, vy=0.0, w=0.0)
        self.send(action)

    def toggle_square_movement(self):
        """Make robot move in a square"""
        if self.is_square_movement:
            self.is_square_movement = False
            print("Square movement stopped.")
        else:
            self.is_square_movement = True
            print("Square movement started.")
            threading.Thread(target=self.move_in_square).start()

    def on_stop(self):
        """Close the UDP socket when the app stops."""
        self.remote_socket.close()
        print("UDP socket closed.")
    
def toggle(d):
   d = not d
   return d

class WASDApp(App):
    def build(self):
        return WASDControls()

if __name__ == "__main__":
    WASDApp().run()
