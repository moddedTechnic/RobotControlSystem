"""Run the client."""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = []

import os
import sys
from pathlib import Path

__dir__ = Path(__file__).parent
sys.path.insert(0, os.fspath(__dir__))
sys.path.insert(1, os.fspath(__dir__.parent))

from ui import GUI, GUIBuilder, font


class ConnectController(GUI):
    """The GUI which allows the user to connect to the robot"""

    robots = [
        'Drone - Sky',
        'NAO - Jurgen',
        'Tank - Fred',
        'Turtlebot 3 - Ada',
        'Turtlebot 3 - Charles',
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

    def on_refresh_selected(self) -> None:
        """Refresh the list of robots available on the current network"""
        print('Refreshing robots...')
        raise NotImplementedError
        self.update_robot_options()

    def on_add_robot_selected(self) -> None:
        """Open the dialog to add a new robot to the options for the current network"""
        print('Adding a new robot...')
        raise NotImplementedError
        self.update_robot_options()

    def on_connect_clicked(self) -> None:
        """Connect to the robot"""
        robot = self.robot.get()
        if robot not in self.robots:
            return  # send some kind of feedback to the user
        model, name = robot.split('-')
        model = model.strip()
        name = name.strip()
        self.controller.connect(model, name)
        self.quit()


class InteractivePromptController(GUI):
    """The GUI which controls the robots"""

    def connect(self, model: str, name: str):
        """Connect to the given robot"""
        print(type(self).__name__, 'connecting to', model, name)
        raise NotImplementedError

    class Menu:
        """Contains data about the menu bar"""

        disabled = {
            'save', 'save_as',
            'undo', 'redo', 'select_all', 'comment', 'replace'
        }

        # region Menu Item Handlers
        # region File
        @staticmethod
        def on_new_clicked(controller: GUI) -> None:
            """Create a new file"""

        @staticmethod
        def on_open_clicked(controller: GUI) -> None:
            """Open file"""

        @staticmethod
        def on_close_clicked(controller: GUI) -> None:
            """Close the current file"""

        @staticmethod
        def on_quit_clicked(controller: GUI) -> None:
            """Quit the application"""
            controller.quit()

        @staticmethod
        def on_preferences_clicked(controller: GUI) -> None:
            """Open the preferences window"""
        # endregion File

        # region Edit
        @staticmethod
        def on_copy_clicked(controller: GUI) -> None:
            """Copy the selected text"""

        @staticmethod
        def on_cut_clicked(controller: GUI) -> None:
            """Cut the selected text"""

        @staticmethod
        def on_paste_clicked(controller: GUI) -> None:
            """Paste the contents of the clipboard"""

        @staticmethod
        def on_indent_clicked(controller: GUI) -> None:
            """Indent the currently selected lines"""

        @staticmethod
        def on_dedent_clicked(controller: GUI) -> None:
            """Dedent the currently selected lines"""

        @staticmethod
        def on_find_clicked(controller: GUI) -> None:
            """Open the 'find' panel of the find/replace window"""
        # endregion Edit

        # region View
        @staticmethod
        def on_show_robot_info_clicked(controller: GUI) -> None:
            """Show the robot information window"""

        @staticmethod
        def on_show_robot_map_clicked(controller: GUI) -> None:
            """Show the robot map window"""

        @staticmethod
        def on_show_robot_history_clicked(controller: GUI) -> None:
            """Show the robot history window"""
        # endregion View

        @staticmethod
        def on_connect_clicked(controller: GUI) -> None:
            """Open the 'connect' window"""
            controller.open_modal_from_file(ConnectController, 'connect').run()
        # endregion Menu Item Handlers

    def on_help_clicked(self) -> None:
        """Show the help window"""

    def on_execute_clicked(self) -> None:
        """Send the command to the robot"""
        print(self.get_command())


def main():
    """Put code here to be run when the module is run"""
    assets_dir = __dir__ / 'assets'
    font.init(assets_dir)
    gui_builder = GUIBuilder(InteractivePromptController, assets_dir)
    gui = gui_builder.build_from_file('interactive_prompt')
    gui.run()


if __name__ == '__main__':
    main()
