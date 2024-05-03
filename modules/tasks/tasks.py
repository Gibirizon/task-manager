from datetime import datetime

from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.pickers import MDTimePickerDialVertical
from modules.to_do_list_base_classes.base import (
    BaseDialog,
    BaseDialogContent,
    ListItemBase,
    ListScreen,
)

app = MDApp.get_running_app()


class TasksDialogContent(BaseDialogContent):
    time_picker = None
    start_time = StringProperty("17:00")
    finish_time = StringProperty("18:00")

    def __init__(self, table_name, *args, **kwargs):
        super().__init__(table_name=table_name, *args, **kwargs)

    def show_time_picker(self, item_name, time_variable):
        # Define default time and which of list item is it
        default_time = datetime.strptime(time_variable, "%H:%M").time()
        self.time_picker = MDTimePickerDialVertical()

        # bind events
        self.time_picker.bind(
            on_ok=lambda time_picker: self.change_time(item_name, time_picker)
        )
        self.time_picker.bind(on_cancel=self.close_time_picker)

        # set default time
        self.time_picker.set_time(default_time)
        self.time_picker.open()

    def change_time(self, name, time_picker):
        # The method changes the time to that which was set.
        time = time_picker.time
        if name == "Start":
            self.start_time = str(time)[:5]
        else:
            self.finish_time = str(time)[:5]
        self.close_time_picker(time_picker)

    def close_time_picker(self, time_picker):
        time_picker.dismiss()
        self.time_picker = None


class TasksDialog(BaseDialog):

    def __init__(self):
        self.content = TasksDialogContent(table_name="tasks_options")
        super().__init__(
            table_name="tasks_options",
            headline_text="Create your new task",
            screen_name="tasks",
        )


class ListItem(ListItemBase):
    def __init__(
        self, table_name, item_id, headline_text, supporting_text, check=False, **kwargs
    ):
        # list item variables to display them properly
        self.supporting_text = supporting_text
        super().__init__(
            table_name=table_name,
            item_id=item_id,
            headline_text=headline_text,
            check=check,
            **kwargs,
        )


class Tasks(ListScreen):
    def __init__(self, **kw):
        super().__init__(table_name="tasks", **kw)

    def open_dialog(self):
        if not self.dialog:
            self.dialog = TasksDialog()
            self.dialog.bind(on_dismiss=self.dismiss_dialog)
            self.dialog.open()

    # adding new task to the list after pressing "OK" in Dialog Window
    def add_item(self, *args):
        # adding task to database
        new_task = app.root.db.create_task(
            (
                self.dialog.content.ids.name_field.text,
                self.dialog.content.start_time,
                self.dialog.content.finish_time,
                0,
            )
        )

        # adding task to the list
        new_list_item = ListItem(
            self.table_name,
            new_task[0],
            new_task[1],
            f"{new_task[2]}-{new_task[3]}",
        )
        self.ids.list_container.add_widget(new_list_item)

        # update of start_time and finish_time (start time is now finish time and finish is +1 hour)
        finish = self.dialog.content.finish_time
        self.dialog.content.start_time = finish
        finish_to_list = finish.split(":")
        if int(finish_to_list[0]) < 23:
            finish_to_list[0] = str(int(finish_to_list[0]) + 1)
        self.dialog.content.finish_time = ":".join(finish_to_list)

    # loading all of tasks in database when entering this screen
    def load_database(self):
        # clear all elements to then add them in proper order
        self.ids.list_container.clear_widgets()

        # getting all tasks from db to then iterate through them and add them to the list
        tasks = app.root.db.get_all_tasks()
        for new_task in tasks:
            if new_task[4] == 0:
                loaded_task = ListItem(
                    self.table_name,
                    new_task[0],
                    new_task[1],
                    f"{new_task[2]}-{new_task[3]}",
                )
            else:
                loaded_task = ListItem(
                    self.table_name,
                    new_task[0],
                    f"[s]{new_task[1]}[/s]",
                    f"{new_task[2]}-{new_task[3]}",
                    True,
                )

            self.ids.list_container.add_widget(loaded_task)
