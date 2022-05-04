"""The controller for the connection window"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = ['AddRobotController']

from client.robot import Robot
from library.ui import GUI


class AddRobotController(GUI):
    """The GUI which allows the user to connect to the robot"""

    def on_save_clicked(self) -> None:
        """Handle the save button being clicked"""
        self.controller.add_robot(Robot('Unknown', self.get_name(), self.get_address()))
        self.destroy()

    def on_connect_clicked(self) -> None:
        """Handle the connect button being clicked"""
        self.controller.add_robot(Robot('Unknown', self.get_name(), self.get_address()))
        self.controller.connect(Robot('Unknown', self.get_name(), self.get_address()))
        self.controller.destroy()
        self.destroy()
