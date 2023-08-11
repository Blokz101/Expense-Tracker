# expense_tracker/presenter/presenter.py

from enum import Enum

class Presenter:
    
    class Column(Enum):
        ID: int = 0
    
    @staticmethod
    def _format(object_list: list[any]) -> list[tuple[int, ...]]:
        """
        Formats the raw database objects into a tuple
        """
        
        return []
    
    @staticmethod
    def get_all() -> list[tuple[int, ...]]:
        """
        Returns a list of all objects in a table
        """
    
        raise RuntimeError("Presenter class does not extend get_all.")
    
    @staticmethod
    def set_value(id: int, column: Column, new_value: any) -> any:
        """
        Updates a cell in the database
        """
        
        if new_value == None:
            raise TypeError("new_value must have a value")
        
        raise ValueError(f"Unable to handel an edit of database column '{column}'.")
    