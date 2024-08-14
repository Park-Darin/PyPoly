#Author(s):
#Team: 
#Date Edited:

from property import Property
import math
import random

class Player:
    """
    A class representing player who participated in the game.

    Attributes:
        - name: A string representing name of the player.
        - symbol: A string representing symbol of the player.
        - fund: An integer representing the amount of fund that self currently own.
        - move_trait: A string representing how the player move in game.
        - position: A tuple representing the coordinate of player, the first element in tuple will be value in x axis , second element will be value in y axis.
        - properties_owned: properties_owned: A list of the properties owned by player.

    Behaviours:
        - Constructor: A method that is called when an object is created.
        - Getters: Methods that returns the provided attributes.
        - Setters: Methods that changes the provided attributes.
        - add_fund: Method of adding the amount(argument) to the funds a player has.
        - reduce_fund: Method of reducing the amount(argument) from the funds a player has.
        - purchase_property: A method that allows the player to purchase the property from the bank.
        - purchase_hotel: A method that is used to build a hotel on property if player owns it and has enough funds to build upon it.
        - sell_property: A method that allows the player to sell the property that they own to bank.
        - display_player_properties: A method used to display properties owned by the player and the total value of them in order of color group
        - check_win: A method for checking if the player fullfills the winning condition.
        - pay_rent: When a player is located on another player's property, he will have to pay rent associated with the property cost and the number of hotels built.
        - determine_action: Determine which action should player do by the property player located on.
    """
    
    # The initial fund that every player have
    STARTING_FUND = 150

    def __init__(self) -> None:
        """
        Constructor method for Player class.
        
        Arguments:
            - None
        Returns:
            - None
        """

        # Set up a variable that is a string which represents the name of the player
        self.name = ""

        # Set up a variable that is a string which represents the symbol of the player
        self.symbol = ""

        # Set up a variable that is an integer which represents the fund that the player starts off with, by default they start off with $150
        self.fund = Player.STARTING_FUND

        # Set up a variable that is a string which represents the move_trait of the player
        self.move_trait = ""

        # Set up a variable that represents the current position of the player
        self.position = (None, None)

        # Set up a list that stores all the properties that the player currently owns
        self.properties_owned = list()
        
    def get_name(self) -> str:
        """
        Getter method for variable name.
        
        Arguments:
            - None

        Returns:
            - name: A string representing name of the player 
        """
        return self.name

    def get_symbol(self) -> str:
        """
        Getter method for variable symbol.
        
        Arguments:
            - None

        Returns:
            - symbol: A string representing symbol of the player
        """
        return self.symbol

    def get_fund(self) -> int:
        """
        Getter method for variable fund.
        
        Arguments:
            - None

        Returns:
            - fund: An integer representing the amount of fund that self currently own 
        """
        return self.fund

    def get_properties_owned(self) -> list:
        """
        Getter method for variable properties_owned.
        
        Arguments:
            - None

        Returns:
            - properties_owned: A list of the properties owned by player
        """
        return self.properties_owned

    def get_position(self) -> tuple:
        """
        Getter method for variable position.
        
        Arguments:
            - None

        Returns:
            - position: A tuple representing the coordinate of player, the first element in tuple will be value in x axis , second element will be value in y axis
        """
        return self.position

    def get_move_trait(self) -> str:
        """
        Getter method for variable move_trait.
        
        Arguments:
            - None

        Returns:
            - move_trait: A string representing how the player move in game
        """
        return self.move_trait

    def set_name(self, name: str) -> None:
        """
        Setter method for variable name.
        
        Arguments:
            - name: A string representing name of the player 

        Returns:
            - None
        """
        self.name = name

    def set_symbol(self, symbol: str) -> None:
        """
        Setter method for variable symbol.
        
        Arguments:
            - symbol: A string representing symbol of the player

        Returns:
            - None
        """
        self.symbol = symbol

    def set_position(self, position: tuple) -> None:
        """
        Setter method for variable position.
        
        Arguments:
            - position: A tuple representing the coordinate of player, the first element in tuple will be value in x axis , second element will be value in y axis

        Returns:
            - None
        """
        self.position = position

    def set_properties_owned(self, property: Property) -> None:
        """
        Setter method for variable properties_owned.
        
        Arguments:
            property: Instances of Class Property

        Returns:
            - None
        """
        self.properties_owned = property

    def set_move_trait(self, move_trait: str) -> None:
        """
        Setter method for variable move_trait.
        
        Arguments:
            - move_trait: A string representing move trait that allow the player to move

        Returns:
            - None
        """
        self.move_trait = move_trait

    def add_fund(self, amount: int) -> None:
        """
        This is a method of adding the amount(argument) to the funds a player has.
        
        Arguments:
            - amount: An integer representing the amount to add to the player's fund.

        Returns:
            - None
        """
        self.fund += amount
    
    def reduce_fund(self, amount: int) -> None:
        """
        This is a method of reducing the amount(argument) from the funds a player has.
        
        Arguments:
            - amount: An integer representing the amount to reduce from the player's fund.

        Returns:
            - None
        """
        self.fund -= amount

    def __str__(self) -> str:
        """
        A special method that is used to define how an object should be represented as a string.
        
        Arguments:
            - None

        Returns:
            - name: A string representing name of the player 
        """
        return self.get_name()

    def __repr__(self) -> str:
        """
        A special method used to represent a class's objects as a string.
        
        Arguments:
            - None

        Returns:
            - __str__(): A method representing string of the object 
        """
        return self.__str__()

    def purchase_property(self, property: Property) -> None:
        """
        A method that allows the player to purchase the property from the bank.
        
        Arguments:
            - property: An object representing the actual property

        Returns:
            - None
        """
        # Check whether the player's fund is greater than or equal to the property cost
        if self.get_fund() >= property.get_property_cost():
            # If it is the case, add the property to the list of properties_owned, reduce their funds by the cost of the property and change the owner of the property
            self.properties_owned.append(property)
            self.reduce_fund(property.get_property_cost())
            property.set_owner(self)
            print("{} purchased {}.".format(self.get_name(), property.get_property_name()))
        else:
            # In the event that the player's funds is less than the cost of the property, just output that the player does not have enough funds
            print("{} cannot purchase {} due to insufficient funds.".format(self.get_name(), property.get_property_name()))
           
    def purchase_hotel(self, property: Property) -> None:
        """
        A method that is used to build a hotel on property if player owns it and has enough funds to build upon it.
        
        Arguments:
            - property: An object representing the actual property

        Returns:
            - None
        """
        # First check whether the player does not own the property, if they do not own the property, print out that they do not own the property and then attempt to buy the said property.
        if property not in self.get_properties_owned():
            print("{} must purchase {} before constructing a hotel.")
            self.purchase_property(property)
        # In the event that the player does own the property
        else:
            # If the player has more than enough funds to purchase a hotel, construct a hotel, reduce their funds by the hotel cost and then print out that the player has purchased the property
            if self.get_fund() >= property.get_hotel_cost():
                property.construct_hotel()
                self.reduce_fund(property.get_hotel_cost())

            # In the event that the player does not have enough funds, tell the player
            else:
                print("{} cannot construct a hotel on {} due to insufficient funds.".format(self.get_name(), property.get_property_name()))

    def sell_property(self, property: Property) -> None:
        """
        A method that allows the player to sell the property that they own to bank 
        
        Arguments:
            - property: An object representing the actual property

        Returns:
            - None
        """
        # Check whether the property is owned by the Player
        if property in self.get_properties_owned():
            
            # Remove the property from the list of properties owned by the player
            self.properties_owned.remove(property)

            # Give the funds back to the player, funds which are calculated by this equation: property_cost + (number of hotels built * hotel_cost)
            property_cost_total = property.get_property_cost() + (property.get_hotels_built() * property.get_hotel_cost())
            self.add_fund(property_cost_total)

            # Reset the property, essentially change the owner
            property.set_owner(Property.ORIGINAL_OWNER)

            #! What about the hotels built in the property? Do they not get reset??
            property.hotels_built = 0

            # Inform the player that the property has been sold
            print("{} sold {} for ${}.".format(self.get_name(), property.get_property_name(), property_cost_total))
            
    def display_player_properties(self) -> None:
        """
        A method used to display properties owned by the player and the total value of them in order of color group.
        
        Arguments:
            - None

        Returns:
            - None
        """

        # Initialize two variables that will contain our total costs
        properties_worth = 0
        hotels_worth = 0

        for color in Property.COLOUR_GROUPS:
            # Initialize a variable that will keep track on whether the color has been printed or not in order to stop printing the same color out multiple of times
            color_printed = False

            # A counter that is just used for cleaner outputs
            counter = 1

            # Loop through every single property that the player owns
            for property_obj in self.get_properties_owned():

                # If the color group of the property matches with the color that we are using right now, switch the color_printed variable to true and print our color out
                if property_obj.get_colour_group() == color:
                    if color_printed == False:  
                        print(color.upper())
                        color_printed = True

                    # Print out the text of what the property is worth, and how much the hotels are worth, even if there are none
                    print("{}. ${} {} (${} Hotels x {})".format(counter, property_obj.get_property_cost(), property_obj.get_property_name(), property_obj.get_hotel_cost(), property_obj.get_hotels_built()))
                    
                    # Add the property cost, hotel costs to our total and increment our counter
                    properties_worth += property_obj.get_property_cost()
                    hotels_worth += property_obj.get_hotel_cost() * property_obj.get_hotels_built()
                    counter += 1
        
        # Print out our totals (Property cost total and hotel cost total)
        print("TOTAL")
        print("${} worth of properties".format(properties_worth))
        print("${} worth of hotels".format(hotels_worth))

    
    def check_win(self, winning_condition: int) -> bool:
        """
        A method for checking if the player fullfills the winning condition.
        
        Arguments:
            - winning_condition: The properties needed to win the game in integer

        Returns:
            - return boolean as whether the player has met the winning condition
        """
        
        # Go through each color group
        for color in Property.COLOUR_GROUPS:
            # Put a counter that keeps track of how many properties we have within the same color group
            number_of_properties_in_color_group = 0
            
            # Loop through all properties that the player owns, in the event that the player's property is within the same color group and the property has a hotel built on it, increment the number_of_properties_in_color_group
            for property in self.get_properties_owned():
                if color == property.get_colour_group() and property.get_hotels_built() >= 1:
                    number_of_properties_in_color_group += 1
            
                # In the event that our counter is greater than or equal to our winning condition, print out that the player has won and return True
                if number_of_properties_in_color_group >= winning_condition:
                    print("Game over! {} WINS!".format(self.get_name()))
                    return True

        # In the event that the condition has not been satisfied, return False
        return False

    
    def pay_rent(self, property: Property) -> None:
        """
        When a player is located on another player's property, he will have to pay rent associated with the property cost and the number of hotels built.
        
        Arguments:
            - property: An object representing the actual property

        Returns:
            - None
        """

        # Fetch the player's balance
        player_balance = self.get_fund()

        # Fetch the owner of the property
        property_owner = property.get_owner()
        
        # Calculate the rent cost.
        rent_cost = round(property.get_rent_price() * (1 + (0.2 * property.get_hotels_built())))

        # If the player has funds that are greater than or equal to the rent_cost, give the owner of the property the rent money and take whatever money that the player who landed on the property owes
        if player_balance >= rent_cost:
            self.reduce_fund(rent_cost)
            property_owner.add_fund(rent_cost)

        # In the event that the player does own a property but has no cash 
        elif len(self.get_properties_owned()) >= 1:

            # Initialize a variable that will contain our value and our index, their indexes are respectively 0 and 1 in our tuple
            lowest_value = (0, 0)

            # Loop through all properties that are owned by the player, and look for the lowest value amongst them
            for owned_property in self.get_properties_owned():
                value = owned_property.get_property_cost() + (owned_property.get_hotel_cost() * owned_property.get_hotels_built())
                if value < lowest_value[0]:
                    lowest_value = (value, self.get_properties_owned().index(owned_property))
            
            # Fetch the object of the lowest valued property
            transacted_property = self.properties_owned[lowest_value[1]]

            # Transfer the lowest valued property over to the property owner where the player landed on, by setting the new property owner and adding it to the player's list of owned properties
            transacted_property.set_owner(property_owner)
            property_owner.properties_owned.append(transacted_property)

            # Remove the property from the previous player
            self.properties_owned.remove(transacted_property)

            print("{} does not have sufficient funds. {} gives {} to {} instead.".format(self, self, transacted_property, property_owner))
        
        # In the event that the player who has landed on the property has no cash or not enough cash and has no property, then transfer all the money from the player to the property owner's fund
        else:
            property_owner.add_fund(player_balance)
            self.reduce_fund(player_balance)

        # If the player's balance has changed compared to what it was initially, print out the string saying that they have paid rent.
        if player_balance != self.get_fund():
            print("{} paid ${} as a rental charge to {} and has ${} left.".format(self, player_balance - self.get_fund(), property_owner, self.get_fund()))

            
    def determine_action(self, property_locations: dict) -> bool:
        """
        Determine which action should player do by the property player located on.
        
        Arguments:
            - property_locations: A dictionary of all property locations

        Returns:
            - purchasable_or_own_property: A boolean represent true if the player can buy the property or build hotel on it otherwise it will be false
        """

        # Set the boolean to be false initially. 
        purchasable_or_own_property = False

        # Fetch the position of the player and fetch the property at that position.
        position = self.get_position()
        property_at_position = property_locations[position]

        # If the property's name at the current player's location is called Reward, then add funds by a random integer ranging from 30 to 150. Then print out that the player has gotten rewarded.
        if property_at_position.get_property_name() == "Reward":
            reward = random.randint(30,150)
            self.add_fund(reward)
            print("{} landed on Reward and has been rewarded ${}.".format(self.get_name(), reward))

        # If the property's name at the current player's location is called Penalty, then reduce funds by current_funds * a random percentage ranging from 5% to 30%
        elif property_at_position.get_property_name() == "Penalty":
            fine = round(self.get_fund() * (random.randint(5, 30) / 100))
            self.reduce_fund(fine)
            print("{} landed on Penalty and has been fined ${}.".format(self.get_name(), fine))
        
        # If the property at current position is either owned by the bank or the player who landed on it, set purchasable_or_own_property to True
        elif property_at_position.get_owner() == "Bank" or property_at_position.get_owner() == self:
            purchasable_or_own_property = True
            
            # Check whether the owner is the bank, if it is then print out that the "{player} has landed on {property_name}"
            if property_at_position.get_owner() == "Bank":
                print("{} landed on {}.".format(self.get_name(), property_at_position.get_property_name()))
            # Else, it would mean that the player who landed on the property is the property owner of said property, in that case we would print out that the "{player} has landed on {property_name}, a property that they own."
            else:
                print("{} landed on {}, a property that they own.".format(self.get_name(), property_at_position.get_property_name()))
        
        # In the event that the property is owned by another player, pay rent to the player.
        else:
            print("{} landed on {}, a property owned by {}.".format(self.get_name(), property_at_position.get_property_name(), property_at_position.get_owner()))
            self.pay_rent(property_at_position)
        
        # Return the boolean that states whether the property is owned by the player or that it is purchasable.
        return purchasable_or_own_property


