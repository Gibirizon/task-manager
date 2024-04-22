from datetime import datetime

from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import (
    IconRightWidget,
    ILeftBodyTouch,
    OneLineIconListItem,
    TwoLineAvatarIconListItem,
)
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDTimePicker
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.textfield import MDTextField

app = MDApp.get_running_app()


class ListItem(TwoLineAvatarIconListItem):
    def __init__(self, item_id, check=False, **kwargs):
        self.item_id = item_id
        super().__init__(
            IconRightWidget(icon="trash-can", on_release=self.delete_task),
            **kwargs,
        )
        self.left_checkbox = LeftCheckbox(active=check)
        self.add_widget(self.left_checkbox)

    # function to delete itself from the list
    def delete_task(self, instance):
        app.root.db.delete_task(self.item_id)
        self.parent.remove_widget(self)

    # marking task as finished/unfinished after clicking on checkbox
    def mark_task(self, active_state):
        task_text = app.root.db.set_completed(self.item_id, int(active_state))
        if active_state == 1:
            self.text = f"[s]{task_text}[/s]"
            return
        self.text = task_text

    # editing text of the task on double tap
    def on_touch_down(self, touch):
        if (
            self.collide_point(*touch.pos)
            and touch.is_double_tap
            and not self.left_checkbox.active
        ):
            y_coordinates = (self.parent.parent.y - 10) / app.root.ids.sm.height
            self.text_field = MDTextField(
                pos_hint={"x": 0.1, "top": y_coordinates},
                size_hint_x=0.8,
                hint_text="Change task name",
                text=self.text,
                mode="fill",
                on_text_validate=self.change_task_name,
            )
            app.root.ids.sm.get_screen("tasks").add_widget(self.text_field)
            print(f"double tap {self}")
        return super().on_touch_down(touch)

    def change_task_name(self, instance):
        # change text of item list
        self.text = self.text_field.text

        # changing text in database
        app.root.db.update_task_name(self.item_id, self.text)

        # remove widget to changing task text
        app.root.ids.sm.get_screen("tasks").remove_widget(self.text_field)


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    pass


class DropdownMenuItem(OneLineIconListItem):
    icon = StringProperty()


class DialogContent(MDBoxLayout):
    time_picker = None
    start_time = StringProperty("17:00")
    finish_time = StringProperty("18:00")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        menu_items = [
            {
                "viewclass": "DropdownMenuItem",
                "icon": "git",
                "text": "Maths",
            },
            {
                "viewclass": "DropdownMenuItem",
                "icon": "git",
                "text": "Polish",
            },
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.task_name_field,
            items=menu_items,
            position="bottom",
            width_mult=4,
        )

    def show_time_picker(self, icon_name, default_start_finish_time):
        # Define default time
        default_time = datetime.strptime(default_start_finish_time, "%H:%M").time()
        # if not self.time_picker:
        self.time_picker = MDTimePicker()
        self.time_picker.bind(
            on_save=lambda instance, time: self.change_time(time, icon_name)
        )
        # set default time
        self.time_picker.set_time(default_time)
        self.time_picker.open()

    def change_time(self, time, icon_name):
        # The method changes the time to that which was set.
        if icon_name == "start_time_icon":
            self.start_time = str(time)[:5]
        else:
            self.finish_time = str(time)[:5]


class Tasks(Screen):
    dialog = None

    def __init__(self, **kw):
        super().__init__(**kw)

    def on_pre_enter(self, *args):
        # loading all of tasks to order them by start_time
        self.load_database_tasks()
        return super().on_pre_enter(*args)

    def open_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Create task",
                type="custom",
                content_cls=DialogContent(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_release=self.close_dialog,
                    ),
                    MDRaisedButton(
                        text="OK",
                        on_release=self.add_task,
                    ),
                ],
            )
        self.dialog.open()

    def close_dialog(self, *args):
        self.dialog.dismiss()
        self.dialog = None

    # adding new task to the list after pressing "OK" in Dialog Window
    def add_task(self, *args):
        # adding task to database
        new_task = app.root.db.create_task(
            (
                self.dialog.content_cls.ids.task_name_field.text,
                self.dialog.content_cls.start_time,
                self.dialog.content_cls.finish_time,
                0,
            )
        )

        # adding task to the lis
        new_list_item = ListItem(
            new_task[0],
            text=new_task[1],
            secondary_text=f"{new_task[2]}-{new_task[3]}",
        )
        self.ids.list_container.add_widget(new_list_item)

        # update of start_time and finish_time (start time is now finish time and finish is +1 hour)
        finish = self.dialog.content_cls.finish_time
        self.dialog.content_cls.start_time = finish
        finish_to_list = finish.split(":")
        if int(finish_to_list[0]) < 23:
            finish_to_list[0] = str(int(finish_to_list[0]) + 1)
        self.dialog.content_cls.finish_time = ":".join(finish_to_list)

    # loading all of tasks in database when entering this screen
    def load_database_tasks(self):
        # clear all elements to then add them in proper order
        self.ids.list_container.clear_widgets()

        # getting all tasks from db to then iterate through them and add them to the list
        tasks = app.root.db.get_all_tasks()
        for new_task in tasks:
            if new_task[4] == 0:
                loaded_task = ListItem(
                    new_task[0],
                    text=new_task[1],
                    secondary_text=f"{new_task[2]}-{new_task[3]}",
                )
            else:
                loaded_task = ListItem(
                    new_task[0],
                    check=True,
                    text=f"[s]{new_task[1]}[/s]",
                    secondary_text=f"{new_task[2]}-{new_task[3]}",
                )

            self.ids.list_container.add_widget(loaded_task)
