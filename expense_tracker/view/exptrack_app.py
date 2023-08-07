# expense_tracker/view/exptrack_app.py

from textual.app import App, ComposeResult
from textual.validation import Regex

from expense_tracker.constants import Constants
from expense_tracker.view.text_input_popup import Text_Input_Popup
from expense_tracker.view.exptrack_data_table import Exptrack_Data_Table


class Exptrack_App(App):
    """
    Main app
    """

    CSS_PATH = Constants.CSS_FILE_PATH

    regex = lambda: Regex("helloing", failure_description="Input must be helloing")

    HEADERS = [
        Exptrack_Data_Table.Column_Info(
            "swimmer",
            "Swimmer",
            lambda: Text_Input_Popup(
                "Enter helloing", "A value here good sir", Exptrack_App.regex()
            ),
        ),
        Exptrack_Data_Table.Column_Info(
            "country",
            "Country",
            lambda: Text_Input_Popup("Enter helloing", "A value here good sir"),
        ),
        Exptrack_Data_Table.Column_Info(
            "time",
            "Time",
            lambda: Text_Input_Popup(
                "Enter helloing", "A value here good sir", Exptrack_App.regex()
            ),
        ),
    ]

    ROWS = [
        (4, "Joseph Schooling", "Singapore", 50.39),
        (2, "Michael Phelps", "United States", 51.14),
        (5, "Chad le Clos", "South Africa", 51.14),
        (6, "László Cseh", "Hungary", 51.14),
        (3, "Li Zhuhao", "China", 51.26),
        (8, "Mehdy Metella", "France", 51.58),
        (7, "Tom Shields", "United States", 51.73),
        (1, "Aleksandr Sadovnikov", "Russia", 51.84),
        (10, "Darren Burns", "Scotland", 51.84),
    ]

    def compose(self) -> ComposeResult:
        yield Exptrack_Data_Table(
            Exptrack_App.HEADERS,
            Exptrack_Data_Table.Table_Info("internal name", "external name"),
        )

    def on_mount(self) -> None:
        table = self.query_one(Exptrack_Data_Table)

        for row in Exptrack_App.ROWS:
            table.add_row(*row[0:], key=row[0])

        print(table.cursor_coordinate)

    def on_exptrack_data_table_edit_request(
        self, message: Exptrack_Data_Table.Edit_Request
    ) -> None:
        def check_input(new_value: str) -> None:
            print(new_value)

        self.push_screen(message.popup, check_input)
