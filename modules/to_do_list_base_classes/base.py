from datetime import datetime

from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogButtonContainer,
    MDDialogContentContainer,
    MDDialogHeadlineText,
)
from kivymd.uix.list import MDListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField

app = MDApp.get_running_app()


class OptionsListItem(MDRelativeLayout):
    headline_text = StringProperty()
    dialog = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BaseDialogContent(MDDialogContentContainer):
    options = None

    def __init__(self, table_name, *args, **kwargs):
        self.table_name = table_name
        super().__init__(*args, **kwargs)

    def set_options(self):
        self.options_items = [
            {
                "viewclass": "OptionsListItem",
                "height": dp(45),
                "headline_text": option,
                "dialog": self,
            }
            for option in self.searched_options
        ]
        self.options_items.insert(
            0,
            {
                "text": "Add new option",
                "height": dp(45),
                "trailing_icon": "plus",
                "on_release": lambda: self.add_new_option(self.ids.name_field.text),
            },
        )

    def options_dropdown_menu_open(self):
        self.set_options()
        if not self.options:
            self.options = MDDropdownMenu(
                caller=self.ids.name_field,
                width=dp(170),
                position="bottom",
                max_height=dp(315),
                items=self.options_items,
            )
            self.options.bind(on_dismiss=self.close_options)
            self.options.open()

    def close_options(self, instance):
        self.options = None

    def choose_name(self, name):
        self.ids.name_field.text = name
        self.ids.name_field.focus = True

    def add_new_option(self, name):
        app.root.db.create_option(self.table_name, name)
        self.on_text_field_text()
        self.ids.name_field.focus = True

    def delete_from_options(self, task):
        app.root.db.delete_option(self.table_name, task)
        self.on_text_field_text()
        self.ids.name_field.focus = True

    # method for searching system in task options
    def on_text_field_text(self):
        all_options = app.root.db.get_all_options(self.table_name)
        self.searched_options = []
        for item_tuple in all_options:
            if item_tuple[0].startswith(self.ids.name_field.text):
                self.searched_options.append(item_tuple[0])
        if self.options:
            self.set_options()
            self.options.items = self.options_items
            pos = self.options.get_target_pos()
            self.options.height = dp(315)
            self.options.set_menu_pos(pos)


class BaseDialog(MDDialog):

    def __init__(self, table_name, headline_text, screen_name):
        # self.content = BaseDialogContent(table_name=table_name)
        super().__init__(
            # -----------------------Headline text-------------------------
            MDDialogHeadlineText(
                text=f"{headline_text}",
            ),
            # -----------------------Custom content------------------------
            MDDialogContentContainer(self.content),
            # ---------------------Button container------------------------
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Cancel"),
                    style="text",
                    on_release=app.root.ids.sm.get_screen(screen_name).close_dialog,
                ),
                MDButton(
                    MDButtonText(text="Accept"),
                    on_release=app.root.ids.sm.get_screen(screen_name).add_item,
                    style="text",
                ),
                spacing="8dp",
            ),
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5, "center_y": 0.7},
        )


class EditField(MDTextField):
    list_item = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ListItemBase(MDListItem):
    def __init__(self, table_name, item_id, headline_text, check=False, **kwargs):
        # list item variables to display them properly
        self.table_name = table_name
        self.item_id = item_id
        self.headline_text = headline_text
        self.check = check

        # dropdown list for additional functions
        self.list_item_additional_functions = [
            {
                "text": "Edit",
                "leading_icon": "notebook-edit",
                "on_release": self.open_edit_dropdown,
            },
            {
                "text": "Delete",
                "leading_icon": "trash-can",
                "on_release": self.delete_item,
            },
        ]

        self.dropdown_options = MDDropdownMenu(
            caller=self, items=self.list_item_additional_functions, position="bottom"
        )

        super().__init__(**kwargs)

    # function to delete itself from the list
    def delete_item(self):
        app.root.db.delete_item(self.table_name, self.item_id)
        self.parent.remove_widget(self)
        self.dropdown_options.dismiss()

    # marking task as finished/unfinished after clicking on checkbox
    def mark(self, active_state):
        item_text = app.root.db.set_item_completed(
            self.table_name, self.item_id, int(active_state)
        )
        if active_state == 1:
            self.ids.list_headline_text.text = f"[s]{item_text}[/s]"
            return
        self.ids.list_headline_text.text = item_text

    # open field to change task name
    def open_edit_dropdown(self):
        # edit name task  - dropdown item on edit click
        self.edit_task_dropdown = MDDropdownMenu(
            caller=self,
            position="bottom",
            items=[
                {"height": dp(15)},
                {
                    "viewclass": "EditField",
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
        app.root.db.update_item_name(self.table_name, self.item_id, new_text)

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


class ListScreen(MDScreen):
    dialog = None

    def __init__(self, table_name, **kw):
        self.table_name = table_name
        super().__init__(**kw)

    def on_pre_enter(self, *args):
        # loading all of items to order them by name
        self.load_database()
        return super().on_pre_enter(*args)

    def close_dialog(self, instance):
        self.dialog.dismiss()

    def dismiss_dialog(self, instance):
        self.dialog = None

    # adding new task to the list after pressing "Accept" in Dialog Window
    def add_item(self, *args):
        # adding task to database
        new_task = app.root.db.create_item(
            self.table_name,
            (self.dialog.content.ids.name_field.text, 0),
        )

        # adding task to the list
        new_list_item = ListItemBase(
            self.table_name,
            new_task[0],
            new_task[1],
        )
        self.ids.list_container.add_widget(new_list_item)

    # loading all of tasks in database when entering this screen
    def load_database(self):
        # clear all elements to then add them in proper order
        self.ids.list_container.clear_widgets()

        # getting all tasks from db to then iterate through them and add them to the list
        tasks = app.root.db.get_all_items(self.table_name)
        for new_task in tasks:
            if new_task[2] == 0:
                loaded_task = ListItemBase(
                    self.table_name,
                    new_task[0],
                    new_task[1],
                )
            else:
                loaded_task = ListItemBase(
                    self.table_name,
                    new_task[0],
                    f"[s]{new_task[1]}[/s]",
                    True,
                )

            self.ids.list_container.add_widget(loaded_task)
