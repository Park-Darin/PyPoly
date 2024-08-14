class Property:
    """
    Class that represents a property.

    Attributes:
        - ORIGINAL_OWNER: A string representing the owner of property before game.
        - COLOUR_GROUPS: A list of all possible colour group of properties.
        - property_name: A string of the name of property.
        - property_cost: An integer of the cost of property.
        - hotel_cost: An integer of the cost of building a hotel.
        - rent_price: An integer of the rental price when other player landed on this property.
        - colour_group: A string of colour group where this property belongs.
        - hotels_built: An integer of how many hotel has been built on this property.
        - location: A tuple representing (row,column) of the property.
        - owner: A string of the ORIGINAL_OWNER or A class of player after being purchased.

    Behaviour:
        - Constructor: A method that is called when an object is created.
        - Getters: Methods that returns the provided attributes.
        - Setters: Methods that changes the provided attributes.
        - construct_hotel: Methods that construct hotel on this property upon called.
    """

    # The original owner of the properties is the Bank, so set up ORIGINAL_OWNER = "Bank"
    ORIGINAL_OWNER = "Bank"

    # We only have four colour groups and they are "Blue", "Green", "Red" and "Yellow".
    COLOUR_GROUPS = ["Blue", "Green", "Red", "Yellow"]

    def __init__(self, property_name: str, property_cost: int, hotel_cost: int, rent_price: int, colour_group: str) -> None:
        """
        Constructor method for Property class.
    
        Arguments:
            - property_name: A string representing name of the property
            - property_cost: An integer representing the cost of the property acquisition
            - hotel_cost: An integer representing the cost of hotel construction 
            - rent-price: An integer representing the cost a player must pay when entering another player's property
            - colour_group: A string representing the colour group the property belongs to

        Returns:
            - None
        """
        # Set up a string that represents the name of the property
        self.property_name = property_name.title()

        # Set up an integer that represents the cost of the property 
        self.property_cost = property_cost

        # Set up an integer that represents the cost of building a hotel on that property
        self.hotel_cost = hotel_cost

        # Set up an integer that represents the rent price which a player must pay when entering another player's property
        self.rent_price = rent_price

        # Set up a string that represents the colour group which the property belongs to
        self.colour_group = colour_group

        # Set up an integer that represents how many hotels have been built on the property
        self.hotels_built = 0

        # Set up a tuple that represents the location at which the property is at
        self.location = (None, None)

        # Set up a string that represents the original owner of the property
        self.owner = Property.ORIGINAL_OWNER

    def get_property_name(self) -> str:
        """
        Getter method for variable property_name.
        
        Arguments:
            - None

        Returns:
            - property_name: A string representing name of the property
        """
        return self.property_name

    def get_property_cost(self) -> int:
        """
        Getter method for variable property_cost.
        
        Arguments:
            - None

        Returns:
            - property_cost: An integer representing the cost of the property acquisition
        """
        return self.property_cost

    def get_hotel_cost(self) -> int:
        """
        Getter method for variable hotel_cost.
        
        Arguments:
            - None

        Returns:
            - hotel_cost: An interger representing the cost of hotel construction 
        """
        return self.hotel_cost

    def get_hotels_built(self) -> int:
        """
        Getter method for variable hotels_built.
        
        Arguments:
            - None

        Returns:
            - hotels_built: An interger representing the numebr of hotels built on the property
        """
        return self.hotels_built

    def get_rent_price(self) -> int:
        """
        Getter method for variable rent_price.
        
        Arguments:
            - None

        Returns:
            - rent-price: An integer representing the cost a player must pay when entering another player's property
        """
        return self.rent_price

    def get_colour_group(self) -> str:
        """
        Getter method for variable colour_group.
        
        Arguments:
            - None

        Returns:
            - colour_group: A string representing the colour group the property belongs to
        """
        return self.colour_group

    def get_owner(self) -> object:
        """
        Getter method for variable owner.
        
        Arguments:
            - None

        Returns:
            - owner: An object representing the owner of the property
        """
        return self.owner

    def get_location(self) -> tuple:
        """
        Getter method for variable location.
        
        Arguments:
            - None

        Returns:
            - location: A tuple representing the location of the property
        """
        return self.location

    def set_owner(self, owner) -> None:
        """
        Setter method for variable owner.
        
        Arguments:
            - owner: An object representing the owner of the property

        Returns:
            - None
        """
        self.owner = owner

    def set_rent_price(self, rent_price: int) -> None:
        """
        Setter method for variable rent_price.
        
        Arguments:
            - rent-price: An integer representing the cost a player must pay when entering another player's property

        Returns:
            - None
        """
        self.rent_price = rent_price

    def set_location(self, location: tuple) -> None:
        """
        Setter method for variable location.
        
        Arguments:
            - location: A tuple representing the location of the property

        Returns:
            - None
        """
        self.location = location

    def construct_hotel(self) -> None:
        """
        This is a method for determine whether a hotel can be built and for constructing one if it can.
        
        Arguments:
            - None

        Returns:
            - None
        """
        # Check whether the player has built two hotels on the same property or not, if they have, then print out they've built the maximum number of hotels allowed on the property.
        if self.get_hotels_built() != 2:
            self.hotels_built = self.get_hotels_built() + 1
            
            # Check whether hotels_built is greater than 1 in order to print the appropriate string
            if self.get_hotels_built() > 1:
                print("{} hotels have been built on {}.".format(self.hotels_built,self.property_name))
            else:
                print("{} hotel has been built on {}.".format(self.hotels_built,self.property_name))
        else:
            print("The maximum number of hotels have been built on {}.".format(self.property_name))
    
    def __str__(self) -> str:
        """
        A special method that is used to define how an object should be represented as a string.
        
        Arguments:
            - None

        Returns:
            - property_name: A string representing name of the property
        """
        return self.property_name

    def __repr__(self) -> str:
        """
        This method allows you to see the same string of your property rather than <property.Property object at 0x000001931DB72890> in the error log or when printing the property directly. 
        
        Arguments:
            - None

        Returns:
            - A string representing the name of this property
        """
        return self.__str__()
