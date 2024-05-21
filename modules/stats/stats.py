from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen

# Get the currently running instance of the app
app = MDApp.get_running_app()


class Stats(MDScreen):
    # Properties to hold the total and consecutive days information
    total_days = StringProperty("0 d")
    consecutive_days = StringProperty("0 d")

    def __init__(self, **kw):
        super().__init__(**kw)

    # Function to open the dropdown menu in the statistics screen
    def tabs_menu_open(self):
        # Define the menu items with icons, table names, and display text
        menu_elements_info = [
            ["checkbox-marked-circle-auto-outline", "tasks", "Daily Tasks"],
            ["timeline-plus", "goals", "Daily Goals"],
            ["calendar-week", "weekly_tasks", "Weekly Tasks"],
        ]

        # Create menu items for the dropdown menu
        menu_items = [
            {
                "text": element[2],
                "leading_icon": element[0],
                "leading_icon_color": "#4d89fb",  # Icon color
                "on_release": lambda text=element[2], table_name=element[
                    1
                ]: self.calculate_statistics(text, table_name),
            }
            for element in menu_elements_info
        ]

        # Initialize and open the dropdown menu
        MDDropdownMenu(caller=self.ids.btn, items=menu_items).open()

    # Function to calculate and update statistics based on selected category
    def calculate_statistics(self, text, table_name):
        # Change button text to the selected category
        self.ids.btn_text.text = text

        # Retrieve all items from the selected table (e.g., tasks, goals, weekly tasks)
        all_elements = app.root.db.get_all_items(table_name)

        # Check if all planned tasks in the selected category are completed
        completed = all([x[-1] for x in all_elements])

        # Update the database with the completion status and retrieve updated statistics
        total, consecutive = app.root.db.create_or_change_item_realisation(
            table_name, int(completed)
        )

        # Update the properties with the new statistics
        self.total_days = f"{total} d"
        self.consecutive_days = f"{consecutive} d"
