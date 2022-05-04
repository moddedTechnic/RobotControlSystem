"""The controller for the connection window"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = ['ConnectController']

from pathlib import Path

from client.add_robot_controller import AddRobotController
from library.functions import unused
from library.iterables import first
from library.network import current_network
from library.ui import GUI

from client.robot import Robot


class ConnectController(GUI):
    """The GUI which allows the user to connect to the robot"""

    @property
    def robots(self) -> list[tuple[Robot]]:
        """Get the robots of the currently connected network"""
        robot_addresses_file = Path(self.assets_dir / 'devices' / f'{current_network.get_ssid()}.network')
        if not robot_addresses_file.parent.exists():
            robot_addresses_file.parent.mkdir(parents=True)
        if not robot_addresses_file.exists():
            robot_addresses_file.write_text('')
            return []
        return [
            (Robot(*item.split(';')),) for item in robot_addresses_file.read_text().split('\n')
            if item.strip()
        ]

    robot_options_actions = [
        ('↻ Refresh', 'refresh'),
        ('+ Add robot', 'add_robot'),
    ]

    def get_robot_options(self) -> list[str, tuple[str, str]]:
        """Get the options for the robot dropdown"""
        return [
            *self.robots,
            *self.robot_options_actions,
        ]

    def add_robot(self, robot: Robot) -> None:
        """Add a robot for the current network"""
        robot_addresses_file = Path(self.assets_dir / 'devices' / f'{current_network.get_ssid()}.network')
        if not robot_addresses_file.parent.exists():
            robot_addresses_file.parent.mkdir(parents=True)
        robot_addresses_file.write_text(f'{robot_addresses_file.read_text()}\n{robot.device};{robot.name};{robot.host}')
        self.update_robot_options()

    def connect(self, robot: Robot) -> None:
        """Connect to the given robot"""
        self.controller.connect(robot)

    def on_refresh_selected(self, robot: Robot) -> None:
        """Refresh the list of robots available on the current network"""
        unused(robot)
        print('Refreshing robots...')
        raise NotImplementedError

    def on_add_robot_selected(self, robot: Robot) -> None:
        """Open the dialog to add a new robot to the options for the current network"""
        unused(robot)
        self.open_modal_from_file(AddRobotController, 'add_robot').run()

    def on_connect_clicked(self) -> None:
        """Connect to the robot"""
        device, name = self.robot.get().split(' - ')
        candidates = list(filter(lambda r: r.device == device and r.name == name, map(first, self.robots)))
        if not candidates:
            return  # send some kind of feedback to the user
        self.controller.connect(candidates[0])
        self.destroy()
