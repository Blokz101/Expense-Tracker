# expense_tracker/model/coords_utils.py

class Coords_Utils:
    """
    Utility functions for coordinates
    """
    
    @staticmethod
    def decimal_coords(coords, ref):
        """
        Convert coords and ref to decimal degrees format
        """

        decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
        if ref == "S" or ref == "W":
            decimal_degrees = -decimal_degrees

        return decimal_degrees
