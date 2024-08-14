# Authors:
# Team:
# Date Edited:

from property import Property
import random
import property_csv_data_a
import property_csv_data_b
import math


class PropertyGenerator:
    """
    A class responsible for reading data then assigning random locations to the property that has been read from the data and saving them in random locations.

    Attributes:
    - properties: A list that contains our Property instances
    - property_locations: A dictionary whose key is a tuple that contains the location of our Property which is our value
    - number_of_locations: An integer that contains the number of properties

    Behaviours:
    - csv_to_properties: Reads data off of a CSV and then creates a new Property object which later gets appended to a list.
    - property_location_generator: Generates the property locations by fetching the number of properties and assigning a random position to the property.
    """

    def __init__(self) -> None:
        """
        Constructor method for PropertyGenerator class.

        Arguments:
            - None
        Returns:
            - None
        """
        # Set up the variable as a list that contains our Property instances
        self.properties = list()

        # Set up a dictionary whose key is a tuple that contains the location of our Property which is our value
        self.property_locations = dict()

        # Set up an integer that contains the number of properties and set it to zero initially
        self.number_of_locations = 0

    def csv_to_properties(self, data: str, delimiter: str) -> None:
        """
        Reads data off of a CSV and then creates a new Property object which later gets appended to a list.

        Arguments:
            - data: A string that contains our CSV data
            - delimiter: A string that specifies the delimiter we used

        Returns:
            - None
        """
        # First get the column names
        column_name = data[0].split(delimiter)

        # Skip the first entry in the data list as that just contains our column names
        for row in data[1:]:
            # Use the delimiter to split our row into an array
            row = row.split(delimiter)

            # Look for the index of our columns and then fetch the respective data of the row at that index
            rent_price = int(row[column_name.index("rent_price")])
            property_cost = int(row[column_name.index("property_cost")])
            hotel_cost = int(row[column_name.index("hotel_cost")])
            property_name = row[column_name.index("property_name")]
            key = row[column_name.index("key")]
            colour_group = row[column_name.index("colour_group")]

            # Create a property object
            property_obj = Property(property_name, property_cost, hotel_cost, rent_price, colour_group)

            # Append it to the properties list
            self.properties.append(property_obj)

    def property_location_generator(self) -> None:
        """
        Generates the property locations by fetching the number of properties and assigning a random position to the property.

        Arguments:
            - None

        Output:
            - None
        """
        # First find the number of properties that exist
        number_of_properties = len(self.properties)
        # There should at the very least be 4 chance grids, so add the number 4
        number_of_properties += 4

        # Find the square root of number_of_properties
        root_value = math.sqrt(number_of_properties)

        # Check whether it is not a perfect square, if it isn't, then just ceil it to get a whole number that we can square
        if (root_value % 1 != 0):
            root_value = math.ceil(root_value)
            number_of_properties = root_value ** 2

        self.number_of_locations = number_of_properties

        # Start setting up variables
        property_locations = dict()

        # Create a copy of self.properties
        list_of_properties = self.properties.copy()

        # Start creating the chance tiles, the number of chance grids can be found by subtracting the number_of_properties by the len(self.properties)
        number_of_chance_grids = number_of_properties - len(self.properties)

        # Divide by two using floor division, so in the event that we have a decimal, floor it and store that as the number_of_penalty_grids
        number_of_penalty_grids = number_of_chance_grids // 2

        # Set up two instances of penalties and rewards
        penalty_object = Property("Penalty", None, None, None, None)
        reward_object = Property("Reward", None, None, None, None)

        # Create placeholders within the list_of_properties that will be replaced with either penalty or reward instances.
        list_of_properties.extend("P" * number_of_penalty_grids)
        list_of_properties.extend("R" * (number_of_chance_grids - number_of_penalty_grids))

        # Loop through the board and choose random properties for that location.
        for row in range(int(root_value)):
            for column in range(int(root_value)):

                # Choose a random element within that list, it can either be a property, "P" or "R"
                random_element = random.choice(list_of_properties)

                # Check whether the random element is neither a "P" or an "R" which would mean that our current location will contain a normal property
                if random_element != "P" and random_element != "R":
                    self.property_locations[(row, column)] = random_element
                # Check whether the random_element is "R" which would mean our current location would be a reward property
                elif random_element == "R":
                    self.property_locations[(row, column)] = reward_object
                # Check whether the random_element is "P" which would mean our current location would be a penalty property
                elif random_element == "P":
                    self.property_locations[(row, column)] = penalty_object

                # Set the location
                self.property_locations[(row, column)].set_location((row, column))

                # Remove the element from the copied list
                list_of_properties.remove(random_element)
