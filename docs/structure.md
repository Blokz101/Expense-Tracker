# Project follows MVP (Model, View, Presenter) format. 
The model works with SQLAlchemy objects and communicates them to the presenter in the same format. A lot of the database work is 

## Terms
- **Database transactions/merchants/tags/amounts/etc**: Refers to transactions/merchants/tags/amounts/etc in the database. This data persists if the application is closed.
- **Statement transactions**: Refers to temporary transactions that were generated from a statement csv. This data is lost every time the application is closed.
- **Field** - A data table or field that supports the transaction table and data. For example, merchant/account/tags/etc.

## Model
Broken into two sections, the ORM and everything else. Everything in the ORM directory is SQLAlchemy tables.

Most of the database work is done by SQLAlchemy. Queries are made in the presenter and formatted there as well. This approach is taken because there is very little data processing required past simply making SQLAlchemy queries. To avoid redundant code the presenter just makes the queries. If more complex operations are required before presentation in the future, the code will switch to queries and data processing will be made in the **model**.

## Presenter
As stated before, the presenter gets data from the model in the form of SQLAlchemy objects, with the exception of reconcile, and sends data to the view in the form of a list of tuples of strings. In the list, each tuple of strings is a row in the display table, and each string in the tuple is a cell.

## View
The view consists of a main class `Exptrack_Data_Table` which is extended to create each different required table. Uses **popups** to allow the user to input data and interact in general.

The following methods can be extended in a new instance of `Exptrack_Data_Table`:
- `get_input_popup`: Called to get the popup that can deal with the type of data that a column was clicked requires. 
    - For example take `expense_tracker.view.table.transaction_table.Transaction_Table`, if the date column is clicked then a popup that selects a date and returns a `datetime` object is required.
- `get_row_style`: Extend to format each row. Takes a `row` as its argument, allows the developer to customize what format the entire row should have based on the row information in `row`. By default there is no row style.
- `_get_row_data`: Gets the data for the table, by default it uses its presenter to get all the rows, override this method to filter what data the table receives.
- `action_create`: Does nothing by default, extend to allow the creation of new rows. Should push a new `expense_tracker.view.popup.create_popup.Create_Popup` or child of that class.
- `action_expand`: Does nothing by default, extend to allow the user to expand a row. Should push a new `textual.screen.ModalScreen`.
- `action_delete`: Does nothing by default, extend to allow the user to delete a row.