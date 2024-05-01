from datetime import datetime

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogButtonContainer,
    MDDialogContentContainer,
    MDDialogHeadlineText,
    MDDialogIcon,
    MDDialogSupportingText,
)
from kivymd.uix.divider import MDDivider
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemSupportingText
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDTimePickerDialVertical
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText

app = MDApp.get_running_app()


class TaskOptionsListItem(MDRelativeLayout):
    headline_text = StringProperty()
    dialog = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DialogContent(MDDialogContentContainer):
    time_picker = None
    start_time = StringProperty("17:00")
    finish_time = StringProperty("18:00")
    task_options = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_options(self):
        self.options_items = [
            {
                "viewclass": "TaskOptionsListItem",
                "height": dp(45),
                "headline_text": option,
                "dialog": self,
            }
            for option in self.searched_options
        ]
        self.options_items.insert(
            0,
            {
                "text": "Add new task option",
                "height": dp(45),
                "trailing_icon": "plus",
                "on_release": lambda: self.add_task_to_options(
                    self.ids.task_name_field.text
                ),
            },
        )

    def task_options_dropdown_menu_open(self):
        self.set_options()
        if not self.task_options:
            self.task_options = MDDropdownMenu(
                caller=self.ids.task_name_field,
                width=dp(240),
                position="bottom",
                max_height=dp(315),
                items=self.options_items,
            )
            self.task_options.bind(on_dismiss=self.close_options)
            self.task_options.open()

    def close_options(self, instance):
        print(instance)
        self.task_options = None

    def choose_task_name(self, name):
        self.ids.task_name_field.text = name
        self.ids.task_name_field.focus = True

    def add_task_to_options(self, name):
        app.root.db.create_task_option(name)
        # self.task_options.dismiss()
        self.on_text_field_text()
        self.ids.task_name_field.focus = True

    def delete_task_from_options(self, task):
        app.root.db.delete_task_option(task)
        self.on_text_field_text()
        self.ids.task_name_field.focus = True

    # method for searching system in task options
    def on_text_field_text(self):
        all_options = app.root.db.get_all_tasks_options()
        self.searched_options = []
        for task_tuple in all_options:
            if task_tuple[0].startswith(self.ids.task_name_field.text):
                self.searched_options.append(task_tuple[0])
        if self.task_options:
            self.set_options()
            self.task_options.items = self.options_items
            pos = self.task_options.get_target_pos()
            self.task_options.height = dp(315)
            self.task_options.set_menu_pos(pos)

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


class Dialog(MDDialog):

    def __init__(self):
        self.content = DialogContent()
        super().__init__(
            # -----------------------Headline text-------------------------
            MDDialogHeadlineText(
                text="Create task",
            ),
            # -----------------------Custom content------------------------
            MDDialogContentContainer(self.content),
            # ---------------------Button container------------------------
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Cancel"),
                    style="text",
                    on_release=app.root.ids.sm.get_screen("tasks").close_dialog,
                ),
                MDButton(
                    MDButtonText(text="Accept"),
                    on_release=app.root.ids.sm.get_screen("tasks").add_task,
                    style="text",
                ),
                spacing="8dp",
            ),
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5, "center_y": 0.7},
        )


class EditTaskField(MDTextField):
    list_item = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ListItem(MDListItem):
    def __init__(self, item_id, headline_text, supporting_text, check=False, **kwargs):
        # list item variables to display them properly
        self.item_id = item_id
        self.headline_text = headline_text
        self.supporting_text = supporting_text
        self.check = check

        # dropdown list for additional functions
        self.list_item_additional_functions = [
            {
                "text": "Edit",
                "leading_icon": "notebook-edit",
                "on_release": self.open_edit_task_dropdown,
            },
            {
                "text": "Delete",
                "leading_icon": "trash-can",
                "on_release": self.delete_task,
            },
        ]

        self.dropdown_options = MDDropdownMenu(
            caller=self,
            items=self.list_item_additional_functions,
        )

        super().__init__(**kwargs)

    # function to delete itself from the list
    def delete_task(self):
        app.root.db.delete_task(self.item_id)
        self.parent.remove_widget(self)
        self.dropdown_options.dismiss()

    # marking task as finished/unfinished after clicking on checkbox
    def mark_task(self, active_state):
        task_text = app.root.db.set_completed(self.item_id, int(active_state))
        if active_state == 1:
            self.ids.list_headline_text.text = f"[s]{task_text}[/s]"
            return
        self.ids.list_headline_text.text = task_text

    # open field to change task name
    def open_edit_task_dropdown(self):
        # edit name task  - dropdown item on edit click
        self.edit_task_dropdown = MDDropdownMenu(
            caller=self,
            # position="bottom",
            items=[
                {"height": dp(15)},
                {
                    "viewclass": "EditTaskField",
                    "list_item": self,
                    "text": self.ids.list_headline_text.text,
                },
                {"height": dp(15)},
            ],
        )
        self.dropdown_options.dismiss()
        self.edit_task_dropdown.open()

    # changing name of the task
    def change_task_name(self, new_text):
        # change text of item list
        self.ids.list_headline_text.text = new_text

        # changing text in database
        app.root.db.update_task_name(self.item_id, new_text)

        # remove dropdown edit task field
        self.edit_task_dropdown.dismiss()

    # displaying dropdown list on double tap: edit and delete task
    def on_touch_down(self, touch):
        if (
            self.collide_point(*touch.pos)
            and touch.is_double_tap
            and not self.ids.list_checkbox.active
        ):
            self.dropdown_options.open()
        return super().on_touch_down(touch)


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
            self.dialog = Dialog()
            self.dialog.bind(on_dismiss=self.dismiss_dialog)
            self.dialog.open()

    def close_dialog(self, instance):
        self.dialog.dismiss()

    def dismiss_dialog(self, instance):
        self.dialog = None

    # adding new task to the list after pressing "OK" in Dialog Window
    def add_task(self, *args):
        # adding task to database
        new_task = app.root.db.create_task(
            (
                self.dialog.content.ids.task_name_field.text,
                self.dialog.content.start_time,
                self.dialog.content.finish_time,
                0,
            )
        )

        # adding task to the list
        new_list_item = ListItem(
            new_task[0],
            new_task[1],
            f"{new_task[2]}-{new_task[3]}",
        )
        self.ids.list_container.add_widget(new_list_item)

        # # update of start_time and finish_time (start time is now finish time and finish is +1 hour)
        finish = self.dialog.content.finish_time
        self.dialog.content.start_time = finish
        finish_to_list = finish.split(":")
        if int(finish_to_list[0]) < 23:
            finish_to_list[0] = str(int(finish_to_list[0]) + 1)
        self.dialog.content.finish_time = ":".join(finish_to_list)

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
                    new_task[1],
                    f"{new_task[2]}-{new_task[3]}",
                )
            else:
                loaded_task = ListItem(
                    new_task[0],
                    f"[s]{new_task[1]}[/s]",
                    f"{new_task[2]}-{new_task[3]}",
                    True,
                )

            self.ids.list_container.add_widget(loaded_task)
