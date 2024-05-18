from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.appbar import MDActionTopAppBarButton, MDTopAppBar
from kivymd.uix.tab import MDTabsItem, MDTabsItemIcon, MDTabsItemText


class Navigation(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    # change top bar title after changing screen
    def adjust_top_bar_title(self, top_bar_title):
        self.ids.top_bar.ids.top_bar_title.text = top_bar_title


class TopBar(MDTopAppBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def adjust_position_of_trailing_button(self):
        self.ids.trailing_button.pos_hint = {"center_x": 0.5}


class NavigationBar(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    def create_tabs(self):
        app = MDApp.get_running_app()
        tabs_icons = [
            "home",
            "checkbox-marked-circle-auto-outline",
            "timeline-plus",
            "timer",
            "calendar-week",
            "chart-timeline-variant-shimmer",
        ]
        tabs_names = app.root.ids.sm.screen_names_to_titles
        tab_names_icons = zip(tabs_names, tabs_icons)
        for tab_name, tab_icon in list(tab_names_icons):
            self.ids.tabs.add_widget(NavigationBarItem(tab_name, tab_icon))


class NavigationBarItem(MDTabsItem):
    def __init__(self, tab_name, tab_icon, **kwargs):
        self.tab_name = tab_name
        self.tab_icon = tab_icon
        super().__init__(**kwargs)
