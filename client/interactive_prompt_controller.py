"""The controller for the interactive prompt window"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = ['InteractivePromptController']

from client.connect_controller import ConnectController
from client.robot import Robot
from library.network.client import Client
from library.network.message import Message
from library.ui import GUI


class InteractivePromptController(GUI):
    """The GUI which controls the robots"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = None

    def connect(self, robot: Robot):
        """Connect to the given robot"""
        print(type(self).__name__, 'connecting to', robot)
        if self.client is not None:
            self.client.disconnect()
        self.client = Client(hostname=robot.host)
        self.client.connect()

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
        if self.client is None:
            return  # we should probably let the user know that nothing's happened
        self.client.send(Message.code(self.get_command()))

    def destroy(self) -> None:
        """Destroy the window"""
        if self.client is not None:
            self.client = self.client.disconnect()
        return super().destroy()
