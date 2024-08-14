#Author(s):
#Team:
#Date Edited:

from player import Player
 
class PerpendicularPlayer(Player):
    """
    A class representing player with perpendicular move trait.

    Attributes:
        - BASE_MOVE_TRAIT: A string representing default move trait of player
        - move_trait: A string representing how the player move in game.
    
    Behaviours:
        - determine_valid_moves: This is a method for the player to determine valid moves that only allow perpendicular movement.
        - display_moves: This is a method that displays the player's current position and valid moves based on whether valid_flags is true or false on the game board.
    """

    # Set the default move trait to Perpendicular
    BASE_MOVE_TRAIT = "Perpendicular"

    def __init__(self) -> None:
        """
        Constructor method for PerpendicularPlayer class.
        
        Arguments:
            - None
        Returns:
            - None
        """
        # Invoke the parent class
        super().__init__()     

        # Set up the move trait of the PerpendicularPlayer   
        self.move_trait = PerpendicularPlayer.BASE_MOVE_TRAIT

    def determine_valid_moves(self, row_size: int) -> list[tuple]:
        """
        This is a method for the player to determine valid moves that only allow perpendicular movement.
        
        Arguments:
            - row_size: An integer representing the number of horizontal and vertical grids.
        Returns:
            - moves: A list of valid positions that the player can move perpendicularly from their current position.
        """
        # Grab position
        pos_x = self.get_position()[0]
        pos_y = self.get_position()[1]

        # Create the list of tuples, doesn't matter if they are valid or not as the code below will root out invalid moves
        moves = [(pos_x+1, pos_y),(pos_x-1, pos_y),(pos_x, pos_y+1),(pos_x, pos_y-1)]

        # Create a range for the valid x and y positions, basically removing negative numbers from the equation
        valid_positions = range(row_size)

        # Check whether the moves are valid or not, if the moves are invalid, remove them from the list of moves
        for move in moves.copy():
            if (move[0] not in valid_positions) or (move[1] not in valid_positions):
                moves.remove(move)

        # Sort the list to be able to read it easily
        moves.sort()
        
        return moves


    def display_moves(self, row_size: int, valid_flag: bool) -> None:
        """
        This is a method that displays the player's current position and valid moves based on whether valid_flags is true or false on the game board.
        
        Arguments:
            - row_size: An integer representing the number of horizontal and vertical grids.
            - valid_flag: If true, the 'x' indicates a valid movement with the position of player. If false, only the current location of the player is displayed.
        Returns:
            - None
        """

        # Fetch the valid moves
        valid_moves = self.determine_valid_moves(row_size)

        # If we want to print the property owned by current player on board, we have to get all the locations of the property
        properties_owned = self.get_properties_owned()
        properties_locations = list()

        # And the number of hotel built at that property
        properties_hotel_built = list()
        for property in properties_owned:
            properties_locations.append(property.get_location())
            properties_hotel_built.append(str(property.get_hotels_built()))

        # Print the first row, only with number of column
        # [str(x) for x in range(row_size)] this is a list of string number, it is joining with 3 space! 
        print("    " + "   ".join([str(x) for x in range(row_size)]))
        
        # For each row:
        for x in range(row_size):

            # Print the seperate line, likely:' +---+---+---+---+'
            print("  " + "+---" * row_size +"+")

            # Initialize string with number of row
            temp = str(x) + " "

            # For each column:
            for y in range(row_size):

                # If the location is a valid move, append '| x ' as a block
                if valid_flag and (x,y) in valid_moves:
                    temp += "| x "

                # If player is at this location, append '| a ' a is the symbol of player as a block
                elif (x,y) == self.get_position():
                    temp += "| {} ".format(self.get_symbol())
                
                # If player owned a property at this location, append '| a ' a is the hotels built as a block
                elif (x,y) in properties_locations:
                    TWHITE = '\033[37m' # White Text
                    ENDC = '\033[m' # Ends the color

                    # properties_locations.index((x,y)) gives the index of the property in the list!
                    temp+= "| {} ".format(TWHITE+properties_hotel_built[properties_locations.index((x,y))]+ENDC)

                # Else, nothings there, append '|   ' as a block!    
                else:

                    temp += "|   "
            
            # Print the row and close it with '|'
            print(temp + "|")

        # Print another seperate line
        print("  " + "+---" * row_size +"+")

            

 
class DiagonalPlayer(Player):
    """
    A class representing player with diagonal move trait.

    Attributes:
        - BASE_MOVE_TRAIT: A string representing default move trait of player
        - move_trait: A string representing how the player move in game.
    
    Behaviours:
        - determine_valid_moves: This is a method for the player to determine valid moves that only allow diagonal movement.
        - display_moves: This is a method that displays the player's current position and valid moves based on whether valid_flags is true or false on the game board.
    """

    # Set the default move trait to Diagonal
    BASE_MOVE_TRAIT = "Diagonal"
    
    def __init__(self) -> None:
        """
        Constructor method for DiagonalPlayer class.

        Arguments:
            - None
        Returns:
            - None
        """
        # Invoke the parent class
        super().__init__()

        # Set up the move trait of the DiagonalPlayer   
        self.move_trait = DiagonalPlayer.BASE_MOVE_TRAIT

    def determine_valid_moves(self, row_size: int) -> list[tuple]:
        """
        This is a method for the player to determine valid moves that only allow diagonal movement.
        
        Arguments:
            - row_size: An integer representing the number of horizontal and vertical grids.
        Returns:
            - moves: A list of valid positions that the player can move diagonally from their current position.
        """
        # Grab position
        pos_x = self.get_position()[0]
        pos_y = self.get_position()[1]

        # Create the list of tuples, doesn't matter if they are valid or not as the code below will root out invalid moves
        moves = [(pos_x+1, pos_y+1),(pos_x-1, pos_y+1),(pos_x+1, pos_y-1),(pos_x-1, pos_y-1)]

        # Create a range for the valid x and y positions, basically removing negative numbers from the equation
        valid_positions = range(row_size)

        # Check whether the moves are valid or not, if the moves are invalid, remove them from the list of moves
        for move in moves.copy():
            if (move[0] not in valid_positions) or (move[1] not in valid_positions):
                moves.remove(move)
        
        # Sort the list to be able to read it easily
        moves.sort()

        return moves

    def display_moves(self, row_size: int, valid_flag: bool) -> None:
        """
        This is a method that displays the player's current position and valid moves based on whether valid_flags is true or false on the game board.
        
        Arguments:
            - row_size: An integer representing the number of horizontal and vertical grids.
            - valid_flag: If true, the 'x' indicates a valid movement with the position of player. If false, only the current location of the player is displayed.
        Returns:
            - None
        """

        # Fetch the valid moves
        valid_moves = self.determine_valid_moves(row_size)

        # If we want to print the property owned by current player on board, we have to get all the locations of the property
        properties_owned = self.get_properties_owned()
        properties_locations = list()

        # And the number of hotel built at that property
        properties_hotel_built = list()
        for property in properties_owned:
            properties_locations.append(property.get_location())
            properties_hotel_built.append(str(property.get_hotels_built()))

        # Print the first row, only with number of column
        # [str(x) for x in range(row_size)] this is a list of string number, it is joining with 3 space! 
        print("    " + "   ".join([str(x) for x in range(row_size)]))
        
        # For each row:
        for x in range(row_size):

            # Print the seperate line, likely:' +---+---+---+---+'
            print("  " + "+---" * row_size +"+")

            # Initialize string with number of row
            temp = str(x) + " "

            # For each column:
            for y in range(row_size):

                # If the location is a valid move, append '| x ' as a block
                if valid_flag and (x,y) in valid_moves:
                    temp += "| x "

                # If player is at this location, append '| a ' a is the symbol of player as a block
                elif (x,y) == self.get_position():
                    temp += "| {} ".format(self.get_symbol())
                
                # If player owned a property at this location, append '| a ' a is the hotels built as a block
                elif (x,y) in properties_locations:
                    TWHITE = '\033[37m' # White Text
                    ENDC = '\033[m' # Ends the color

                    # properties_locations.index((x,y)) gives the index of the property in the list!
                    temp+= "| {} ".format(TWHITE+properties_hotel_built[properties_locations.index((x,y))]+ENDC)

                # Else, nothings there, append '|   ' as a block!    
                else:

                    temp += "|   "
            
            # Print the row and close it with '|'
            print(temp + "|")

        # Print another seperate line
        print("  " + "+---" * row_size +"+")
    
class LPlayer(Player):
    """
    A class representing player with L-shaped move trait.

    Attributes:
        - BASE_MOVE_TRAIT: A string representing default move trait of player
        - move_trait: A string representing how the player move in game.
    
    Behaviours:
        - determine_valid_moves: This is a method for the player to determine valid moves that only allow L-shaped movement.
        - display_moves: This is a method that displays the player's current position and valid moves based on whether valid_flags is true or false on the game board.
    """

    # Set the default move trait to L-shaped
    BASE_MOVE_TRAIT = "L"
    
    def __init__(self) -> None:
        """
        Constructor method for LPlayer class.

        Arguments:
            - None
        Returns:
            - None
        """
        # Invoke the parent class
        super().__init__()

        # Set up the move trait of the LPlayer
        self.move_trait = LPlayer.BASE_MOVE_TRAIT

    def determine_valid_moves(self, row_size: int) -> list[tuple]:
        """
        This is a method for the player to determine valid moves that only allow L-shaped movement.
        
        Arguments:
            - row_size: An integer representing the number of horizontal and vertical grids.
        Returns:
            - moves: A list of valid positions that the player can move in an L shape from their current position.
        """
        # Grab position
        pos_x = self.get_position()[0]
        pos_y = self.get_position()[1]

        # Create the list of tuples that contains the possible moves, doesn't matter if they are valid or not as the code below will root out invalid moves
        moves = [(pos_x-2, pos_y+1),(pos_x-1, pos_y+2), (pos_x+1, pos_y+2), (pos_x+2, pos_y+1), (pos_x-2, pos_y-1), (pos_x-1, pos_y-2), (pos_x+1, pos_y-2), (pos_x+2, pos_y-1)]

        # Create a range for the valid x and y positions, basically removing negative numbers from the equation
        valid_positions = range(row_size)

        # Check whether the moves are valid or not, if the moves are invalid, remove them from the list of moves
        for move in moves.copy():
            if (move[0] not in valid_positions) or (move[1] not in valid_positions):
                moves.remove(move)
        
        # Sort the list to be able to read it easily
        moves.sort()

        return moves

    def display_moves(self, row_size: int, valid_flag: bool) -> None:
        """
        This is a method that displays the player's current position and valid moves based on whether valid_flags is true or false on the game board.
        
        Arguments:
            - row_size: An integer representing the number of horizontal and vertical grids.
            - valid_flag: If true, the 'x' indicates a valid movement with the position of player. If false, only the current location of the player is displayed.
        Returns:
            - None
        """

        # Fetch the valid moves
        valid_moves = self.determine_valid_moves(row_size)

        # If we want to print the property owned by current player on board, we have to get all the locations of the property
        properties_owned = self.get_properties_owned()
        properties_locations = list()

        # And the number of hotel built at that property
        properties_hotel_built = list()
        for property in properties_owned:
            properties_locations.append(property.get_location())
            properties_hotel_built.append(str(property.get_hotels_built()))

        # Print the first row, only with number of column
        # [str(x) for x in range(row_size)] this is a list of string number, it is joining with 3 space! 
        print("    " + "   ".join([str(x) for x in range(row_size)]))
        
        # For each row:
        for x in range(row_size):

            # Print the seperate line, likely:' +---+---+---+---+'
            print("  " + "+---" * row_size +"+")

            # Initialize string with number of row
            temp = str(x) + " "

            # For each column:
            for y in range(row_size):

                # If the location is a valid move, append '| x ' as a block
                if valid_flag and (x,y) in valid_moves:
                    temp += "| x "

                # If player is at this location, append '| a ' a is the symbol of player as a block
                elif (x,y) == self.get_position():
                    temp += "| {} ".format(self.get_symbol())
                
                # If player owned a property at this location, append '| a ' a is the hotels built as a block
                elif (x,y) in properties_locations:
                    TWHITE = '\033[37m' # White Text
                    ENDC = '\033[m' # Ends the color

                    # properties_locations.index((x,y)) gives the index of the property in the list!
                    temp+= "| {} ".format(TWHITE+properties_hotel_built[properties_locations.index((x,y))]+ENDC)

                # Else, nothings there, append '|   ' as a block!    
                else:

                    temp += "|   "
            
            # Print the row and close it with '|'
            print(temp + "|")

        # Print another seperate line
        print("  " + "+---" * row_size +"+")
