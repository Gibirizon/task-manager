from kivy.uix.screenmanager import Screen
from kivymd.uix.appbar import MDActionTopAppBarButton, MDTopAppBar


class TopBar(MDTopAppBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def adjust_position_of_trailing_button(self):
        print("adjusting")
        self.ids.trailing_button.pos_hint = {"center_x": 0.5}


class Navigation(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    # change top bar title after changing screen
    def adjust_top_bar_title(self, top_bar_title):
        self.ids.top_bar.ids.top_bar_title.text = top_bar_title
