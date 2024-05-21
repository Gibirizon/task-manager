from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.appbar import MDActionTopAppBarButton, MDTopAppBar
from kivymd.uix.tab import MDTabsItem, MDTabsItemIcon, MDTabsItemText


class Navigation(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    # Change top bar title after changing screen
    def adjust_top_bar_title(self, top_bar_title):
        self.ids.top_bar.ids.top_bar_title.text = (
            top_bar_title  # Update the title text of the top bar
        )


class TopBar(MDTopAppBar):
    pass


class NavigationBar(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    # Create tabs for the navigation bar
    def create_tabs(self):
        app = MDApp.get_running_app()  # Get the current running instance of the app
        tabs_icons = [
            "home",
            "checkbox-marked-circle-auto-outline",
            "timeline-plus",
            "timer",
            "calendar-week",
            "chart-timeline-variant-shimmer",
        ]
        tabs_names = (
            app.root.ids.sm.screen_names_to_titles
        )  # Get the tab names from screen manager
        tab_names_icons = zip(
            tabs_names, tabs_icons
        )  # Pair tab names with their respective icons
        for tab_name, tab_icon in list(tab_names_icons):
            self.ids.tabs.add_widget(
                NavigationBarItem(tab_name, tab_icon)
            )  # Add each tab item to the navigation bar


class NavigationBarItem(MDTabsItem):
    def __init__(self, tab_name, tab_icon, **kwargs):
        self.tab_name = tab_name  # Name of the tab
        self.tab_icon = tab_icon  # Icon of the tab
        super().__init__(**kwargs)
