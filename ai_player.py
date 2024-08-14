#V. final
from player_move import LPlayer
import random
import math
 
class AIPlayer(LPlayer):
    """
    A class representing AI player, like normal player, but it make decision by itself.

    Attributes:
        - WINNING_CONDITION: An integer of how many property needed to win the game.
        - previous_moves: A list of locations stores the places ai has visited.
        - sorted_properties: A tuple that has all properties sorted in order of property cost.
        - first_run: A boolean representing is the ai first move or not.
        - target: A tuple of packed command that ai will always follow.
    
    Behaviours:
        - Constructor: A method that is called when an object is created.
        - ai_move: Method that return the position of next move.
        - buy_or_build: Method that do buy properties or build hotel when needed.
    """

    # AIPlayer should also know the winning condition as player knows too!
    # No discrimination!
    WINNING_CONDITION = 0

    def __init__(self) -> None:
        """
        Constructor method of AIPlayer class.
        
        Arguments:
            - None

        Returns:
            - None
        """

        # Invoke the parent class of AIPlayer class too
        super().__init__()

        # Initialize empty variable that help AI does its decision
        self.previous_moves = list()
        self.sorted_properties = None
        self.first_run = True
        self.target = (-1,-1)

#==================================================================ASSISTANT FUNCTION============================================================================================

    def recurring_colour(self) -> list[str]:
        """
        A method that return the most color of property that player has owned.
        
        Arguments:
            - None

        Return:
            - recurring: A list of color of properties that player owned
        """

        # Get the property that player owned
        my_properties = self.get_properties_owned()

        # Initialize a list with all colour string and empty count
        colours = ["Blue", "Green", "Red", "Yellow"]
        amount = [0,0,0,0]

        # If player does not own any property, return all colours
        if len(my_properties) == 0:
            return colours

        # Else, count the properties each colour have
        for p in my_properties:
            amount[colours.index(p.get_colour_group())]+=1;
        
        # Get maximum count by sorting it and get the last item
        maximum = sorted(amount)[3]

        # Loop through the colours and check if its count is same as maximum, if yes, add to a list
        recurring = [colours[i] for i in range(4) if amount[i] == maximum]

        # Return it
        return recurring

    def get_sorted_properties(self,property_locations: dict):
        """
        A method that return all properties sorted in property_cost and hotel_cost, to assist AIplayer winning ASAP

        Arguments:
            -property_locations: A dicionary of all property_locations

        Returns:
            -properties: All sorted properties packed in tuple
        """

        # Initialize four empty list to store the properties
        properties_RED = list()
        properties_GREEN = list()
        properties_BLUE = list()
        properties_YELLOW = list()

        # Iterate through all properties
        for cord in property_locations.keys():

            # Get the attribute of the property and store them in variable
            p = property_locations[cord]
            p_cost = p.get_property_cost()
            h_cost = p.get_hotel_cost()
            p_colour = p.get_colour_group()

            # Seperate the properties to different list by colour
            if p_colour == 'Red':
                properties_RED.append((p_cost,h_cost,p,p.get_location()))
            if p_colour == 'Green':
                properties_GREEN.append((p_cost,h_cost,p,p.get_location()))
            if p_colour == 'Blue':
                properties_BLUE.append((p_cost,h_cost,p,p.get_location()))
            if p_colour == 'Yellow':
                properties_YELLOW.append((p_cost,h_cost,p,p.get_location()))

        # Sort all list by the price of property
        # key= lambda a:a[0] here represent sorting according to a[0], as the tuple contained multiple datatype, this prevent the program from crashing
        properties_RED.sort(key=lambda a: a[0])
        properties_GREEN.sort(key=lambda a: a[0])
        properties_BLUE.sort(key=lambda a: a[0])
        properties_YELLOW.sort(key=lambda a: a[0])

        # Return them packed in tuple
        properties = (properties_RED,properties_GREEN,properties_BLUE,properties_YELLOW)
        return properties

    def get_low_cost_buyable(self,winning_condition: int):
        """
        This method will find the most 'winable' colour, it will find the lowest cost of properties to win by colour

        Arguments:
            -winning_condition: The properties needed to win the game in integer

        Returns:
            -lowest_cost: Packed cost and colour in tuple
        """

        # Initialize an empty list and add the packed tuple into it
        winning_cost = list()

        # The lowest cost of properties to win by colour is calculated in calculate method
        winning_cost.append( (self.calculate(self.sorted_properties[0],winning_condition),'Red'))
        winning_cost.append( (self.calculate(self.sorted_properties[1],winning_condition),'Green'))
        winning_cost.append( (self.calculate(self.sorted_properties[2],winning_condition),'Blue'))
        winning_cost.append( (self.calculate(self.sorted_properties[3],winning_condition),'Yellow'))

        # Sort the list from lowest cost to highest cost and get the lowest cost
        lowest_cost = sorted(winning_cost)[0]

        # Return the packed lowest cost and colour
        return lowest_cost

    def calculate(self,properties: list,winning_condition: int):
        """
        A method that calculate the sum of cost of property and hotel needed to win

        Arguments:
            -properties: A list of property in the same colour
            -winning_condition: The properties needed to win the game in integer

        Returns:
            -winning_cost: The sum of cost of property and hotel needed to win
        """

        # Initialize empty variable
        buyable_count = 0
        winning_cost = 0

        # Iterate through properties in the list 
        for p in properties:

            # If it is buyable, add cost to sum and 1 to count
            if p[2].get_owner() == 'Bank':
                buyable_count+=1
                winning_cost += p[0]
                winning_cost += p[1]
            
            # If there is any property in this colour belong to the player, add 1 to count
            elif p[2].get_owner() == self:
                buyable_count += 1
            
            # If the amount of properties is enough to win, break loop
            if buyable_count >= winning_condition:
                break
        
        # If buyable_count is less than winning_condition, then this colour is not winable anymore
        if buyable_count < winning_condition:
            return 999999

        # Return the cost
        return winning_cost

    def determine_next_moves(self, x: int, y: int, row_size: int) -> list[tuple]:
        """
        This is a method for the AIPlayer to determine next valid moves

        Arguments:
            -x: AIPlayer current X coordinate
            -y: AIPlayer current Y coordinate
            -row_size: The row size of the game board

        Returns:
            -possible_moves: A list of valid moves
        """

        # Initialize all possible moves in a list
        possible_moves = [(x+2,y+1),(x+2,y-1),(x+1,y+2),(x+1,y-2),(x-1,y+2),(x-1,y-2),(x-2,y+1),(x-2,y-1)]

        # Initialize an empty lsit to store invalid moves
        to_be_pop = list()

        # Iterate through all possible moves
        for move in possible_moves:

            # Check if the move is out of the board
            if move[0]<0 or move[0]>=row_size or move[1]<0 or move[1]>=row_size:

                # If yes, append it into the list
                to_be_pop.append(move)

        # Iterate through the list of invalid moves and remove them from possible_moves 
        for index in to_be_pop:
            possible_moves.remove(index)

        # Return the list of possible_moves, the leftover are valid moves!
        return possible_moves

    def reward_locations(self, property_locations: dict) -> list[tuple]:
        """
        A method that tells AIPlayer which location has reward

        Arguments:
            -property_locations: A dicionary of all property locations

        Rewards:
            -list_of_reward_locations: A list of locations of all property named Reward
        """

        # Set up a variable that will store a tuple that dictates our locations
        list_of_reward_locations = []

        # Loop through the list of property_locations looking for properties whose name is "Reward", if their name is "Reward", add their location to the list of tuples
        for locations in property_locations.keys():
            if property_locations[locations].get_property_name() == "Reward":
                list_of_reward_locations.append(locations)
        
        # Return the list of locations
        return list_of_reward_locations

#==================================================================CORE FUNCTION============================================================================================
    def prefered_move(self):
        """
        This method will tell the AIPlayer what to do is the best in current situation

        Arguments:
            - None

        Returns:
            - Packed commands
        """

        # Get prefered colours from the assistant method above
        prefered_colour1 = self.recurring_colour()
        prefered_colour2 = self.get_low_cost_buyable(AIPlayer.WINNING_CONDITION)[1]

        # Check whether AIPlayer has bought enough property in same colour
        for color in ["Blue", "Green", "Red", "Yellow"]:
            properties = list()
            for owned in self.get_properties_owned():
                if owned.get_colour_group() == color:
                    properties.append(owned)
            
            # If AIPlayer has enough property in same colour
            if len(properties) >= AIPlayer.WINNING_CONDITION:

                # Check which property have not build hotel yet
                for p in properties:

                    # If there are any property that does not have hotel build and have enough money
                    if p.get_hotel_cost() <= self.get_fund() and p.get_hotels_built() == 0:

                        # Tell AIPlayer to build hotel at this location 
                        return ('BUILD',p.get_location())
                    
        # If AIplayer has no enough property to win, try to buy the property in prefered colour 
        if prefered_colour2 in prefered_colour1:

            # For each colour, find the cheapest property and check whether AIPlayer can afford the property,
            # If yes, tell AIPlayer to buy the property
            if prefered_colour2 == 'Red':
                for p in self.sorted_properties[0]:
                    if p[2].get_owner() == 'Bank':
                        if p[0] <= self.get_fund():
                            return ('BUY',p[2].get_location())
            if prefered_colour2 == 'Green':
                for p in self.sorted_properties[1]:
                    if p[2].get_owner() == 'Bank':
                        if p[0] <= self.get_fund():
                            return ('BUY',p[2].get_location())
            if prefered_colour2 == 'Blue':
                for p in self.sorted_properties[2]:
                    if p[2].get_owner() == 'Bank':
                        if p[0] <= self.get_fund():
                            return ('BUY',p[2].get_location())
            if prefered_colour2 == 'Yellow':
                for p in self.sorted_properties[3]:
                    if p[2].get_owner() == 'Bank':
                        if p[0] <= self.get_fund():
                            return ('BUY',p[2].get_location())

        # If the colour of lowest cost is not in the properties that we owned, then the colour might be not winable anymore
        # Thus we tell AIPlayer to sell properties in that colour
        else:
            for colour in prefered_colour1:
                for property in self.get_properties_owned():
                    if property.get_colour_group() == 'colour':
                        return ('SELL',property.get_location())
            
        # Else, AIPlayer does not have money to do anything, tell AIPlayer to find for reward
        return ('GOTO','REWARD')

    def ai_move_util(self,x: int,y: int,depth: int,row_size: int,x1: int,y1: int):
        """
        This method will tell the AIPlayer how to do the best move to archive its target by finding the shortest path toward it

        Arguments:
            -x: AIPlayer current X coordinate
            -y: AIPlayer current Y coordinate
            -depth: the number of step taken
            -row_size: The row size of the game board
            -x1: The X coordinate of target location
            -y1: The Y coordinate of target location
        
        Returns:
            -closest_route: Step needed towards target location and next move packed in tuple
        """

        # If the current location is the target location, return the number of step taken and current location
        if x == x1 and y == y1:
            return (depth,(x,y))
        
        # Determine next valid moves
        next_moves = self.determine_next_moves(x,y,row_size)

        # Initialize an empty list to store the packed tuple of step and location
        temp = list()

        # Append current location into previous_moves to prevent it coming back
        self.previous_moves.append((x,y))

        # If this way cannot reach target location in 5 move, just give up
        if depth > 6:
            # Remove this location from previous_moves as AIPlayer does not really went there
            self.previous_moves.pop()
            return (100,(-1,-1))

        # Iterate through all possible vaild next move
        for moves in next_moves:

            # If AIPlayer has not visited there before,
            if moves not in self.previous_moves:

                # Append current location into previous_moves to prevent it coming back
                self.previous_moves.append(moves)
                
                # Try calling this method again to see if next move can reach the target location or not
                # Note that the current x and current y has changed to the move we are considering and depth increased by one as this is considered as one step!
                move = self.ai_move_util(moves[0],moves[1],depth+1,row_size,x1,y1)

                # After we know the step needed to reach target location, prepare to go to next iteration before that, pop the location from previous_moves
                self.previous_moves.pop()

                # Append the step needed to take and the current move into the list
                # Note that current move is appended but not the next move as next move is unreachable for now!
                temp.append((move[0],moves))

        # Pop the current move from previous_moves as AIPlayer does not actually went there
        self.previous_moves.pop()

        # If there are no valid move for next move, tell AIPlayer this is unreachable
        if len(temp) == 0:
            return (100,(-1,-1))
        
        # Get the closest route by sorting it
        closest_route = sorted(temp)[0]
        return closest_route

    def ai_move(self, possible_moves: list[tuple], property_locations: dict) -> tuple:
        """
        This method will determine which location should AIPlayer go

        Arguments:
            -possible_moves: A list of possible valid moves
            -property_locations: A dicionary of all property locations

        Returns:
            -move: The best move AIPlayer should go
        """

        # If this method is firstly called,
        if self.first_run:

            # Store all the sorted properties into sorted_properties
            # Note that the reason this block of code does not appear in constructor is because it will change the argument taken from constructor!
            self.sorted_properties = self.get_sorted_properties(property_locations)
            self.first_run = False

        # Calculate the row size of the current game board
        row_size = int(math.sqrt(len(property_locations)))

        # Get the command given by prefered_move() function
        move = self.prefered_move()

        # Get AIPlayer's current location
        x,y = self.get_position()

        # If the command is 'GOTO' somewhere, we have to find the exact location
        if move[0] == 'GOTO':
            
            # Initialize an empty list to store the step to reward and the location of reward
            reward_step = list()

            # Iterate through every reward property
            for location in self.reward_locations(property_locations):

                # Unpack the location
                x1,y1 = location

                # Call ai_move_util() method to see the how to go to (x1,y1) from (x,y)
                reward_step.append(self.ai_move_util(x,y,0,row_size,x1,y1))
            
            # Set the current objective as goto the closest reward location after sorting the list
            # sorted(reward_step) is a list,
            # sorted(reward_step)[0] get the least tuple from the list
            # sorted(reward_step)[0][1] get the location from the tuple
            # the tuple has form: (step needed,(x,y))
            closest_reward_location = sorted(reward_step)[0][1]
            self.target = ('GOTO',closest_reward_location)

        # Or else, just update the objective to the command given
        else:
            self.target = move
        
        # Unpack the location AIPlayer trying to go
        x1,y1 = self.target[1]

        # Calculate what is the next step
        move = self.ai_move_util(x,y,0,row_size,x1,y1)[1]

        # If the move given is invalid, random choose a location to jump
        # Usually it should be valid unless the board is too big that the step needed to go is more than 5!
        if move not in possible_moves:
            # ERROR! - Impossible route
            return random.choice(possible_moves)

        # Remember the last step taken to prevent coming back within three rounds
        self.previous_moves.append(move)

        # If there is more than 3 round, forget the most previous step, we can visit there again!
        if len(self.previous_moves) > 3:
            self.previous_moves.pop(0)

        # Debugging message
        #print('AI decided to:',self.target)
        #print('Now going to:',move)
        #print('AI has went: ',self.previous_moves)
        #print('AI now owned: ')
        #self.display_player_properties()

        # Return the final decision
        return move

    def buy_or_build(self, best_move, property_locations: dict) -> None:
        """
        This method will tell the AIPlayer when to buy, sell or build

        Arguments:
            -best_move: The location AIPlayer is currently on
            -property_locations: A dicionary of all property locations

        Returns:
            -None
        """

        # Get the property AIPlayer is currently standing on
        current_property = property_locations[best_move]

        # If we are on the location we are trying to go
        if best_move == self.target[1]:

            # Get the objective
            move = self.target[0]

            # If it is time to buy
            if move == 'BUY':

                # Purchase the property AIPlayer is standing on
                self.purchase_property(current_property)

            # If it is time to buy    
            if move == 'BUILD':

                # Construct a hotel at current location
                self.purchase_hotel(current_property)

            # If it is time to buy
            if move == 'SELL':

                # Sell this property
                self.sell_property(current_property)
            

