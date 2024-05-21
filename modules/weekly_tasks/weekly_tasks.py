from modules.to_do_list_base_classes.base import (
    BaseDialog,
    BaseDialogContent,
    ListScreen,
)


class WeeklyTasks(ListScreen):
    """A screen that displays a list of weekly tasks. Inherits from ListScreen."""

    def __init__(self, **kw):
        # Initialize the WeeklyTasks screen with the specified table name "weekly_tasks"
        super().__init__(table_name="weekly_tasks", **kw)

    def open_dialog(self):
        """Opens a dialog to add a new weekly task."""
        if not self.dialog:
            self.dialog = WeeklyTasksDialog()
            self.dialog.bind(on_dismiss=self.dismiss_dialog)
            self.dialog.open()


class WeeklyTasksDialog(BaseDialog):
    """A dialog for adding or editing weekly tasks. Inherits from BaseDialog."""

    def __init__(self):
        # Set the content with options specific to weekly tasks
        self.content = BaseDialogContent(table_name="weekly_tasks_options")
        # Initialize the dialog with table name, headline text, and screen name
        super().__init__(
            table_name="weekly_tasks_options",  # The database table name for weekly task options
            headline_text="Set your next task",  # The headline text for the dialog
            screen_name="weekly_tasks",  # The name of the screen this dialog is associated with
        )
