from datetime import datetime

from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import (
    IconLeftWidget,
    ILeftBodyTouch,
    IRightBodyTouch,
    TwoLineAvatarIconListItem,
)
from kivymd.uix.pickers import MDTimePicker
from kivymd.uix.selectioncontrol import MDCheckbox


class ListItem(TwoLineAvatarIconListItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_widget(LeftCheckbox())
        self.add_widget(RightIcons())

    def on_size(self, *args):
        self.ids._right_container.width = self.width
        self.ids._right_container.x = self.width


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    pass


class RightIcons(IRightBodyTouch, MDFloatLayout):
    pass


class DialogContent(MDBoxLayout):
    time_picker = None
    start_time = StringProperty("17:00")
    finish_time = StringProperty("18:00")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def show_time_picker(self, default_start_finish_time):
        # Define default time
        default_time = datetime.strptime(default_start_finish_time, "%H:%M").time()
        # if not self.time_picker:
        self.time_picker = MDTimePicker()
        self.time_picker.bind(
            on_save=lambda instance, time: self.change_time(
                instance, time, default_start_finish_time
            )
        )
        # set default time
        self.time_picker.set_time(default_time)
        self.time_picker.open()

    def change_time(self, instance, time, property):
        # The method changes the time to that which was set.
        if property == self.start_time:
            self.start_time = str(time)[:5]
        else:
            self.finish_time = str(time)[:5]


class Tasks(Screen):
    dialog = None

    def __init__(self, **kw):
        super().__init__(**kw)

    def open_dialog(self):
        print("opening dialog")
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
        new_list_item = ListItem(
            text=self.dialog.content_cls.ids.task_name_field.text,
            secondary_text=f"{self.dialog.content_cls.start_time}-{self.dialog.content_cls.finish_time}",
        )
        self.ids.list_container.add_widget(new_list_item)
