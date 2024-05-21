from modules.to_do_list_base_classes.base import (
    BaseDialog,
    BaseDialogContent,
    ListScreen,
)


class Goals(ListScreen):
    """A screen that displays a list of goals. Inherits from ListScreen."""

    def __init__(self, **kw):
        super().__init__(
            table_name="goals", **kw
        )  # Initialize with table_name set to "goals"

    def open_dialog(self):
        """Opens a dialog to add a new goal."""
        if not self.dialog:
            self.dialog = GoalsDialog()
            self.dialog.bind(on_dismiss=self.dismiss_dialog)
            self.dialog.open()


class GoalsDialog(BaseDialog):
    """A dialog for adding goals. Inherits from BaseDialog."""

    def __init__(self):
        self.content = BaseDialogContent(
            table_name="goals_options"
        )  # Set the content with options specific to goals
        super().__init__(
            table_name="goals_options",  # The database table name for goal options
            headline_text="Set your next goal",  # The headline text for the dialog
            screen_name="goals",  # The name of the screen this dialog is associated with
        )
