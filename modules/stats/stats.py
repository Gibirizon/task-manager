from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.tab import MDTabsItem, MDTabsItemIcon, MDTabsItemText

# Get the currently running instance of the app
app = MDApp.get_running_app()


class Stats(MDScreen):
    # Properties to hold the total and consecutive days information
    total_days = StringProperty("0 d")
    consecutive_days = StringProperty("0 d")
    category = StringProperty("")

    def __init__(self, **kw):
        super().__init__(**kw)

    def on_pre_enter(self, *args):
        self.calculate_statistics(self.category)
        return super().on_pre_enter(*args)

    # Function to display two categories
    def create_categories(self):
        categories_info = [
            ["checkbox-marked-circle-auto-outline", "tasks", "Daily Tasks"],
            ["timeline-plus", "goals", "Daily Goals"],
        ]

        for category in categories_info:
            self.ids.categories.add_widget(
                MDTabsItem(
                    MDTabsItemIcon(
                        icon=category[0],
                    ),
                    MDTabsItemText(
                        text=category[2],
                    ),
                    on_release=lambda _, table_name=category[
                        1
                    ]: self.calculate_statistics(table_name),
                )
            )
            self.ids.categories.switch_tab(icon=categories_info[0][0])

    # Function to calculate and update statistics based on selected category
    def calculate_statistics(self, table_name):
        # set category - the same name as tables
        self.category = table_name

        # Retrieve all items from the selected table (e.g., tasks, goals)
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
