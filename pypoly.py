import time
import math
import random
from property import Property
from property_generator import PropertyGenerator
from player import Player
from player_move import PerpendicularPlayer, DiagonalPlayer, LPlayer
from ai_player import AIPlayer

import property_csv_data_a
import property_csv_data_b

class PyPoly:
    """
    
    A class that uses methods from other classes to set up and run the game PyPoly.

    Attributes: 
    - list_of_players: A list that contains our player_instances
    - property_locations: A dictionary whose key is a tuple that contains the location of our Property which is our value.
    - win_requirement: An integer that will store our winning condition/requirement
    - ongoing: A boolean that represents whether the game is ongoing or not 

    Behaviours:
    - validate_range_input: Prompts the user to type a value that is within the range, if the value is not within the range, it will keep on prompting until it is.
    - ai_thinking: This function is responsible for printing out that the AI is thinking, it handles generating a random delay to generate suspense.
    - pre_start_game: Essentially asks for the number of players, player names, winning condition and what data it should use.
    - regular_player_turn: This function is responsible for playing a normal player's turn
    - ai_player_turn: This function is responsible for playing an AIPlayer's turn, very similar to regular_player_turn but the options are chosen automatically by the AIPlayer.

    """

    def __init__(self) -> None:
        """
        A constructor method for the PyPoly class.
        Calls self.pre_start_game() as soon as it is done constructing.

        Arguments:
        - none

        Returns:
        - none
        """
        
        # Set up a list that contains our player instances
        self.list_of_players = []

        # Set up a dictionary that will contain our property locations. Our key would be our tuple that represents the coordinate of the property, and our value is our property instance.
        self.property_locations = dict()

        # Set up a variable that will store our winning condition/requirement
        self.win_requirement = 0
        
        # Set up a variable that keeps track of whether the game is ongoing or not, have it set up as True initially
        self.ongoing = True

        # Start up pre_start_game to start getting information regarding the game.
        self.pre_start_game()

######################################   Misc   ######################################

    def validate_range_input(self, prompt: str, range: tuple, display_bounds: bool) -> int:
        """
        Prompts the user to type a value that is within the range, if the value is not within the range, it will keep on prompting until it is.
        
        Arguments:
        - prompt: A string that asks the players to input something.
        - range: A tuple that represents the range of numbers that we will be working with, so suppose (2,6), then we will check whether the input is from 2-6.
        - display_bounds: A boolean that dictates whether we display the bounds initially or not.

        Returns:
        - An integer that is deemed as valid
        """
        
        # If display_bounds is true, then display the boundaries like (1 → 2) alongside the prompt while asking for input, else do not display the bounds only
        if display_bounds:
            input_value = input("{prompt} ({range_low} → {range_high}): ".format(prompt = prompt, range_low = range[0], range_high = range[1]))
        else:
            input_value = input("{prompt}".format(prompt = prompt))

        # This while loop stays True and the only way to exit it is when our input value has been confirmed to be a digit and is within bounds
        while(True):
            
            # Checks whether our input is a digit
            if input_value.isdigit():
                input_value = int(input_value)

                # Checks whether our input_value is within bounds if it is a digit
                if input_value >= range[0] and input_value <= range[1]:
                    break
            
            # Asks the user to enter a valid number if it is not a digit or if it is not within the bounds
            input_value = input("Please enter a valid number ({range_low} → {range_high}): ".format(range_low = range[0], range_high = range[1]))
        
        # Return our input back as a number
        return int(input_value)

    def ai_thinking(self, player_name: str):
        """
        This function is responsible for printing out that the AI is thinking, it handles generating a random delay to generate suspense

        Arguments:
        - none

        Returns:
        - none
        """

        # Set up a string that says that the AI is thinking
        thinking = "{player_name} is thinking..".format(player_name = player_name)

        # Get a random number that will be our delay
        delay = random.randint(2,5)
        
        # Loop three times to add in a couple of dots to our thinking string
        for _ in range(3):
            
            # Divide our random delay by three
            divided_delay = delay/3

            # Print out our thinking string
            print(thinking, end='\r')

            # Add in a dot to our thinking string for the next time around
            thinking += "."

            # Sleep by our divided delay
            time.sleep(divided_delay)

########################################## Pre-start ##########################################

    def pre_start_game(self):
        """
        Initializes variables and sets up the game before it starts.
        Essentially asks for the number of players, player names, winning condition and what data it should use.

        Arguments:
        - none

        Returns:
        - none
        """

        # # # Property Generation # # #

        # Print out a string that will welcome the player into the game
        print("\n")
        print("-"*24)
        print("Welcome to 💰 PyPoly 💰!")
        print("-"*24)
        print("\n")

        # Create a new instance of the PropertyGenerator class in order to generate the property_locations
        property_gen = PropertyGenerator()

        # Delay by 2 seconds
        time.sleep(2)

        # Ask the player what data they'd like to use for the game
        property_data_choice = self.validate_range_input("Please select the data that will be used in order to power the game: \n[1] csv_data_a \n[2] csv_data_b \n[3] Both \n", (1,3), False)

        # If the choice is 1, then use data from csv_data_a
        if property_data_choice == 1:
            property_gen.csv_to_properties(property_csv_data_a.csv_data, property_csv_data_a.delimiter)
        # If the choice is 2, then use data from csv_data_b
        elif property_data_choice == 2:
            property_gen.csv_to_properties(property_csv_data_b.csv_data, property_csv_data_b.delimiter)
        # If the choice is 3, then use data from csv_data_a and csv_data_b
        elif property_data_choice == 3:
            property_gen.csv_to_properties(property_csv_data_a.csv_data, property_csv_data_a.delimiter)
            property_gen.csv_to_properties(property_csv_data_b.csv_data, property_csv_data_b.delimiter)

        # Generate the property locations
        property_gen.property_location_generator()

        # Save the property locations
        self.property_locations = property_gen.property_locations

        # # # Players # # #

        # Ask for the winning requirement and set the win_requirement
        self.win_requirement = self.validate_range_input("\n\nWhat is the number of properties needed to win?", (1,5), True)
        AIPlayer.WINNING_CONDITION = self.win_requirement

        # Start asking for how many players will play, it is bounded from 2 to 6 players
        number_of_players = self.validate_range_input("\n\nHow many players do you want?", (2, 6), True)
        
        # Start asking whether they'd like to play against AI players or Regular players
        player_type_choice = self.validate_range_input("\n\nWould you like to play against: \n[1] AI Players \n[2] Regular players \n", (1, 2), False)

        number_of_ai_players = 0
        number_of_regular_players = 0

        # If the player chose to play with AI players, then ask how many would they like to play with
        if player_type_choice == 1:
            
            # This part asks for how many AI players they'd like to play with, it is bounded from 1 to number_of_players
            number_of_ai_players = self.validate_range_input("\n\nHow many AI players would you like to play against? ", (1, number_of_players-1), True)

            # Check if there are any slots left for regular players, if there are, allocate the slots for the normal players
            if (number_of_players - number_of_ai_players) != 0:
                number_of_regular_players = number_of_players - number_of_ai_players

        # If the player type was 2, then number of players = number of regular players
        else:
            number_of_regular_players = number_of_players

        # Set up a list that will store player_names in order to check for duplicates
        list_of_regular_player_names = []

        # Set up a list that will store the chosen_locations for the players to spawn in
        chosen_locations = []

        # Start generating regular player instances if there are any
        for regular_player_number in range(number_of_regular_players):
            
            # Fetch player name first and once it has been validated as not a duplicate name or an empty name, append it to the list of player names
            player_name = input("\n\nWhat is player {number}'s name? \n".format(number = regular_player_number+1))
            while(player_name in list_of_regular_player_names or player_name == ""):
                if player_name == "":
                    player_name = input("Please enter a different name as a name cannot be empty. \n")
                else:
                    player_name = input("Please enter a different name as that name is taken. \n")
            list_of_regular_player_names.append(player_name)
            
            # Print out an empty line for the sake of cleanliness
            print("\n")
            
            # Ask the user of the player's move trait
            print("\nWhat is {player_name}'s move trait?".format(player_name = player_name))
            move_trait_choice = self.validate_range_input("[1] Perpendicular \n[2] Diagonal \n[3] L \n", (1, 3), False)
            
            # Create a player instance according to their move trait
            if move_trait_choice == 1:
                player_instance = PerpendicularPlayer()
            elif move_trait_choice == 2:
                player_instance = DiagonalPlayer()
            elif move_trait_choice == 3:
                player_instance = LPlayer()
            
            # Set their symbols and names
            player_instance.set_name(player_name)
            player_instance.set_symbol(str(regular_player_number+1))

            # Fetch the property locations and save it as a list
            property_locations = list(self.property_locations.keys())

            # Choose a random location for them to start in by randomly choosing a location from property_locations
            random_location = random.choice(property_locations)
            while(random_location in chosen_locations):
                random_location = random.choice(property_locations)
            
            # Add the chosen random_location to the list of already chosen locations and set the player's position
            chosen_locations.append(random_location)
            player_instance.set_position(random_location)

            # Append their instance to self.list_of_players
            self.list_of_players.append(player_instance)
        

        # This contains the list of possible AI names, courtesy of a random name generator
        list_of_possible_ai_player_names = ['Maverick','Rosemarie', 'Langdon', 'Donny', 'Syd', 'Sibyl', 'Lisbet', 'Suzan', 'Duane', 'Anona', 'Laryn', 'Tory', 'Malcolm', 'Irene']

        # Start generating AIPlayer instances if there are any
        for ai_player_number in range(number_of_ai_players):
            
            # Set up a new instance of AIPlayer
            ai_player_instance = AIPlayer()

            # Choose a random name from the list of possible ai player names and have it removed from the list to avoid duplicate AI player names.
            ai_player_name = random.choice(list_of_possible_ai_player_names)
            ai_player_instance.set_name(ai_player_name + " (AI)")
            list_of_possible_ai_player_names.remove(ai_player_name)

            # Fetch the property locations and save it as a list
            property_locations = list(self.property_locations.keys())

            # Choose a random location for them to start in by randomly choosing a location from property_locations
            random_location = random.choice(property_locations)
            while(random_location in chosen_locations):
                random_location = random.choice(property_locations)

            # Add the chosen random_location to the list of already chosen locations
            chosen_locations.append(random_location)
            ai_player_instance.set_position(random_location)

            # Set the symbol for the ai player using chr to change the ascii value to a character, 97 → 122 corresponds to letters a → z.
            ai_player_instance.set_symbol(chr(97 + ai_player_number))

            # Add the ai_player_instance to our list_of_players
            self.list_of_players.append(ai_player_instance)

        # Print out empty lines for the sake of cleanliness
        print("\n \n")

        # Start the game as the prerequisites have been met.
        self.start_game()
    
######################################### Player turns #########################################

    def regular_player_turn(self, player_obj):
        """
        This function is responsible for playing a normal player's turn

        Arguments:
        - player_obj: An instance of either PerpendicularPlayer, DiagonalPlayer or LPlayer

        Returns:
        - none
        """

        # Calculate the row_size by square rooting the number of elements that are present in property_locations.
        row_size = int(math.sqrt(len(self.property_locations)))
        
        # Print out where the player is currently
        print("\nPlayer {player_name} is currently at location {position}.".format(player_name = player_obj.get_name(), position = player_obj.get_position()))

        # Display the board for the player and the possible positions that they can move towards to.
        player_obj.display_moves(row_size, True)

        # Print out two empty lines for the sake of cleanliness
        print("\n \n")

        # Start asking for the player for them to choose a location to move towards to
        # Start by fetching the valid moves
        valid_moves_list = player_obj.determine_valid_moves(row_size)

        # Display the options of the positions
        print("Pick one valid move:")
        for index in range(len(valid_moves_list)):
            print("[{index}] - {element}".format(index = index + 1, element = valid_moves_list[index]))
        
        # Check whether the input is valid or not and if it is valid, sleep for 3 seconds, then move towards the new location
        choice = self.validate_range_input("",(1, len(valid_moves_list)), False)
        time.sleep(3)
        player_obj.set_position(valid_moves_list[choice-1])
        
        # Print out two empty lines for the sake of cleanliness
        print("\n \n")

        # Print out that the player has moved towards a new location
        print("Player {player_name} has moved to {position}".format(player_name = player_obj.get_name(), position = player_obj.get_position()))

        # Display the board
        player_obj.display_moves(row_size, False)

        # Determine what action to take based on the player's location while also checking whether the property is purchasable or owned by the player
        purchasable_or_own_property = player_obj.determine_action(self.property_locations)

        # Create a list that will contain our options that the player can choose from
        options_list = []

        # If it is either a purchasable or own property
        if purchasable_or_own_property:
            
            # Fetch the property owner by grabbing the player's current location and then using that as a key to get our property instance
            property = self.property_locations[player_obj.get_position()]

            # Check whether it is owned by the bank as that would mean that it is a purchasable property.
            if property.get_owner() == "Bank":
                # If it owned by the bank, it would mean that you can buy the property
                options_list.append("Purchase the Property")

            # Check whether the player can build a hotel at the current property location, the max amount of hotels that can be built at a location is 2
            elif property.get_hotels_built() != 2:
                # If it is owned by the player and has not reached the max number of hotels allowed, allow the player to build a hotel
                options_list.append("Build a Hotel")

        # Check if the player has any properties or not
        if len(player_obj.get_properties_owned()) != 0:

            # If the player does own a property or more, add in property related options
            options_list.append("Display Owned Properties")
            options_list.append("Sell A Property")

        # Append the rest of the default options
        options_list.append("Next Player")
        options_list.append("Quit Game")

        # Keep on looping until the player either choose to quit the game or chooses next player
        while True:

            # Check whether the player has met the win condition, if they have, break out of the while loop and set self.ongoing to False
            if player_obj.check_win(self.win_requirement):
                self.ongoing = False
                break

            # Sleep for 2 seconds to add some suspense
            time.sleep(2)
            
            # Fetches the property at current location
            property = self.property_locations[player_obj.get_position()]

            # Create a variable that will store the user_prompt
            user_prompt = ""

            # Print out that the user should pick a choice
            print("\n\nYou have ${funds} in your fund, make a smart pick:".format(funds = player_obj.get_fund()))

            # This will start concatenating our options to user_prompt
            for index in range(len(options_list)):
                # Our index here gets added up by one and our elements are our options that are within the options_list
                user_prompt += "[{index}] - {element} ".format(index = index+1, element = options_list[index])
                
                # Add in a colon at the last element
                if index == len(options_list) - 1:
                    user_prompt += ": "
            
            # Prompt the user and ask for a valid input
            choice = self.validate_range_input(user_prompt, (1, len(options_list)), False)

            # Fetch the user's choice
            user_choice = options_list[choice-1]

            # If the player would like to purchase the property, attempt to buy the property and then remove the option from the list
            if user_choice == "Purchase the Property":

                # Tell the user the price of the property and the color group that it belongs to
                yes_or_no = self.validate_range_input("\n\nThe price of the property is ${property_cost} and it belongs to the {color_group} color group. \n[1] - Purchase it! \n[2] - Nevermind. \n".format(property_cost = property.get_property_cost(), color_group = property.get_colour_group()), (1,2), False)

                # If the user said yes, then proceed with purchase of the property and remove the option from the list
                if yes_or_no == 1:
                    player_obj.purchase_property(property)

                    # Check whether "Display Owned Properties" does not exist within the list, if it does not, then add it in and if "Display Owned Properties" does not exist within the list, it is right to assume that "Sell a Property" does not exist either.
                    if not "Display Owned Properties" in options_list and len(player_obj.get_properties_owned()):
                        options_list.insert(0, "Sell A Property")
                        options_list.insert(0, "Display Owned Properties")

                    # Remove "Purchase the Property" from the list
                    options_list.remove(user_choice)
            
            # If the player would like to build a hotel at the current location,
            elif user_choice == "Build a Hotel":

                # Calculate the rent before building the hotel and after
                rent_before = round(property.get_rent_price() * (1 + (0.2 * property.get_hotels_built())))
                rent_after = round(property.get_rent_price() * (1 + (0.2 * (property.get_hotels_built() + 1 ))))

                # Tell the user the price of building a hotel at the property and the amount the rent would increase to
                yes_or_no = self.validate_range_input("\n\nThe cost of building the hotel is {hotel_cost} and the rent will increase from {rent_before} → {rent_after} \n[1] - Build a hotel! \n[2] - Nevermind. \n".format(hotel_cost = property.get_hotel_cost(), rent_before = rent_before, rent_after = rent_after), (1,2), False)

                # If the user said yes, then proceed with building a hotel
                if yes_or_no == 1:
                    player_obj.purchase_hotel(property)
                    options_list.remove(user_choice)

            elif user_choice == "Display Owned Properties":
                
                # Print out an empty line for the sake of cleanliness
                print("\n")

                # Print out dashed lines
                print("-"*50 + "\n")

                # Display player properties
                player_obj.display_player_properties()

                # Print out an empty line for the sake of cleanliness
                print("\n")

                owned_properties = player_obj.get_properties_owned()

                # Start printing out the locations of the properties
                print("Locations:")
                for index in range(len(owned_properties)):
                    print("{property_number}. {property_name}, its location {location} and belongs to the color group {color_group}.".format(property_number = index + 1, property_name = owned_properties[index].get_property_name(), location = owned_properties[index].get_location(), color_group = owned_properties[index].get_colour_group()))

                # Print out dashed lines
                print("\n" + "-"*50)
            

            # If the player would like to sell a property
            elif user_choice == "Sell A Property":
                
                # Get a copy of the properties owned by the player and add "Nevermind" to the list of options
                sell_property_options = player_obj.get_properties_owned().copy()
                sell_property_options.append("Nevermind.")

                # Set up a variable that will contain our user prompt
                user_prompt = ""

                # Print out
                print("\nChoose a property to sell:")

                # This will start concatenating our options to user_prompt
                for index in range(len(sell_property_options)):
                    if sell_property_options[index] != "Nevermind.":

                        # Calculate the property value 
                        property_value = sell_property_options[index].get_property_cost() + (sell_property_options[index].get_hotel_cost() * sell_property_options[index].get_hotels_built())

                        # Concatenate the string below if our element from the list is not "Nevermind".
                        user_prompt += "\n[{index}] - {property_name}, its location {location} and by selling it you will get ${property_value} back.".format(index = index+1, property_name = sell_property_options[index].get_property_name(), location = sell_property_options[index].get_location(), property_value = property_value)
                    else:
                        user_prompt += "\n[{index}] - Nevermind.\n".format(index = index+1)
                    
                # Prompt the user and ask for a valid input
                choice = self.validate_range_input(user_prompt, (1, len(options_list)), False)

                # If our option selected is not nevermind, proceed with selling the property
                if sell_property_options[choice-1] != "Nevermind.":

                    # Print out an empty line for the sake of cleanliness
                    print("\n")

                    # Sell the property
                    player_obj.sell_property(sell_property_options[choice-1])

                    # Remove the option
                    options_list.remove(user_choice)

                    # Also check whether the player owns any more properties or not, if not, remove the option of displaying their own properties
                    if len(player_obj.get_properties_owned()) == 0:
                        options_list.remove("Display Owned Properties")
                        
                        # Check if the option of building hotels still exists, if it does, remove it
                        if "Build a Hotel" in options_list:
                            options_list.remove("Build a Hotel")

            # If the player has chosen to pass the turn to the next player
            elif user_choice == "Next Player":
                break

            # If the player has chosen to quit the game
            elif user_choice == "Quit Game":

                # Print out two empty lines for the sake of cleanliness
                print("\n \n")

                # Start selling the properties that the player owns, that is if they own any
                for property in player_obj.get_properties_owned():
                    player_obj.sell_property(property)

                # If the player has money, print out that they have donated it to charity
                if player_obj.get_fund() > 0:
                    print("\n{player_name} has donated ${amount} to charity!".format(player_name = player_obj.get_name(), amount = player_obj.get_fund()))

                # Print out that the player has quit the game
                print("\n{player_name} has quit the game!".format(player_name = player_obj.get_name()))

                # Remove the player from the list of players
                self.list_of_players.remove(player_obj)

                # Break the loop
                break

    def ai_player_turn(self, player_obj: AIPlayer):
        """
        This function is responsible for playing an AIPlayer's turn.
        It displays where the AIPlayer is currently and what move it has taken.

        Arguments:
        - player_obj: An instance of AIPlayer

        Returns: 
        - None
        """

        # Print out the board 
        # Calculate the row_size by square rooting the number of elements that are present in property_locations.
        row_size = int(math.sqrt(len(self.property_locations)))
        
        # Print out where the player is currently
        print("\nPlayer {player_name} is currently at location {position}.".format(player_name = player_obj.get_name(), position = player_obj.get_position()))

        # Display the board for the player and the possible positions that they can move towards to.
        player_obj.display_moves(row_size, True)

        # Start fetching the valid moves and display them to the user
        valid_moves_list = player_obj.determine_valid_moves(row_size)

        # Display the moves that are available
        for index in range(len(valid_moves_list)):
            print("[{index}] - {element}".format(index = index + 1, element = valid_moves_list[index]))

        # Print out an empty line for the sake of cleanliness
        print("\n")
        
        # Print out that the AI is thinking, the function handles delays and adds a bit of suspense
        self.ai_thinking(player_obj.get_name())

        # Have the AI decide on a location that it would like to move towards to.
        move = player_obj.ai_move(valid_moves_list, self.property_locations)

        # Print out empty lines
        print("")

        # Print out the option that the AI has picked
        print(valid_moves_list.index(move)+1)
        
        # Print out two empty lines for the sake of cleanliness.
        print("\n \n")
        
        # Sleep for 3 seconds
        time.sleep(3)

        # Move the AI and display current location
        player_obj.set_position(move)

        # Print out that the player has moved towards a new location
        print("Player {player_name} has moved to {position}".format(player_name = player_obj.get_name(), position = player_obj.get_position()))

        # Print out the board
        player_obj.display_moves(row_size, False)

        # Determine what action to take based on the player's location 
        purchasable_or_own_property = player_obj.determine_action(self.property_locations)

        # Set up an options list that will contain our options
        options_list = []

        # Set up the user_prompt which will store our prompt
        user_prompt = ""

        # Start setting up the illusion that the AI would pick an option, whether to buy, build, sell, etc.

        # Fetch the property at current location
        property_at_location = self.property_locations[player_obj.get_position()]

        # If the property is purchasable or their own property then, check if property owner is the AIPlayer themselves
        if purchasable_or_own_property:

            # In the event that the property is owned by the Bank, then allow the AI to purchase it
            if property_at_location.get_owner() == "Bank":
                options_list.append("Purchase the Property")

            # In the event that it is not owned by the bank, it would mean that it is owned by the player which would allow them to build a hotel on the property given that they do not have more than 2
            elif property_at_location.get_hotels_built() != 2:
                options_list.append("Build a Hotel")
        
        # Check whether the AIPlayer owns any properties then add the option of selling properties
        if len(player_obj.get_properties_owned()) != 0:
            options_list.append("Display Owned Properties")
            options_list.append("Sell A Property")

        # Append the rest of the options
        options_list.append("Next Player")
        options_list.append("Quit Game")

        # Print out that the user should pick a choice
        print("\n\nYou have ${funds} in your fund, make a smart pick:".format(funds = player_obj.get_fund()))

        # This will start concatenating our options to user_prompt which would print out the options that the AI is able to pick
        for index in range(len(options_list)):
            # Our index here gets added up by one and our elements are our options that are within the options_list
            user_prompt += "[{index}] - {element} ".format(index = index+1, element = options_list[index])
            
            # Add in a colon at the last element
            if index == len(options_list) - 1:
                user_prompt += ": "

        # Print out our prompt
        print(user_prompt)

        # Put in a delay and have the AI "think"
        self.ai_thinking(player_obj.get_name())

        # Fetch what the AI would like to do in the event that its target has the same location as our move
        if player_obj.target[1] == move:

            # Fetch the plan that the AI has for the location
            plan = player_obj.target[0]
            
            # If the plan is to buy, have the AI print out that it has chosen the option of buying the property
            if plan == "BUY":

                # Print out our choice
                print("\n" + str(options_list.index("Purchase the Property") + 1))

                # Print out the property cost and its color group
                print("\n\nThe price of the property is ${property_cost} and it belongs to the {color_group} color group. \n[1] - Purchase it! \n[2] - Nevermind. \n".format(property_cost = property_at_location.get_property_cost(), color_group = property_at_location.get_colour_group()))

                # Add in a delay to make selecting options more natural
                time.sleep(2)

                # Print out that it has selected the option 1
                print(1)

                # Check whether "Display Owned Properties" does not exist within the list, if it does not, then add it in and if "Display Owned Properties" does not exist within the list, it is right to assume that "Sell a Property" does not exist either.
                if not "Display Owned Properties" in options_list and len(player_obj.get_properties_owned()):
                    options_list.insert(0, "Sell A Property")
                    options_list.insert(0, "Display Owned Properties")

                # Remove the option of purchasing the property again
                options_list.remove("Purchase the Property")

            # If the plan is to build, have the AI print out that it has chosen the option of building a hotel
            elif plan == "BUILD":
                
                # Print out our choice
                print("\n" + str(options_list.index("Build a Hotel") + 1))

                # Calculate the rent before building the hotel and after
                rent_before = round(property_at_location.get_rent_price() * (1 + (0.2 * property_at_location.get_hotels_built())))
                rent_after = round(property_at_location.get_rent_price() * (1 + (0.2 * (property_at_location.get_hotels_built() + 1 ))))

                # Print out the price of building a hotel and the rent increase, and print out the option that it chose
                print("\n\nThe cost of building the hotel is {hotel_cost} and the rent will increase from {rent_before} → {rent_after} \n[1] - Build a hotel! \n[2] - Nevermind. \n".format(hotel_cost = property_at_location.get_hotel_cost(), rent_before = rent_before, rent_after = rent_after))
                
                # Add in a delay to make selecting options more natural
                time.sleep(2)
                
                # Print out the option that the AI has chosen
                print(1)

                # Remove the option of building a hotel
                options_list.remove("Build a Hotel")
            
            # If the plan is to Sell, have the AI print out that it has chosen the option of selling a property.
            elif plan == "SELL":

                # Print out our choice
                print("\n" + str(options_list.index("Sell A Property") + 1))
                
                # Get a copy of the properties owned by the player and add "Nevermind" to the list of options
                sell_property_options = player_obj.get_properties_owned().copy()
                sell_property_options.append("Nevermind.")

                # Set up a variable that will contain our user prompt
                user_prompt = ""

                # Print out
                print("\nChoose a property to sell:")

                # This will start concatenating our options to user_prompt
                for index in range(len(sell_property_options)):
                    if sell_property_options[index] != "Nevermind.":

                        # Calculate the property value 
                        property_value = sell_property_options[index].get_property_cost() + (sell_property_options[index].get_hotel_cost() * sell_property_options[index].get_hotels_built())

                        # Concatenate the string below if our element from the list is not "Nevermind".
                        user_prompt += "\n[{index}] - {property_name}, its location {location} and by selling it you will get ${property_value} back.".format(index = index+1, property_name = sell_property_options[index].get_property_name(), location = sell_property_options[index].get_location(), property_value = property_value)
                    else:
                        user_prompt += "\n[{index}] - Nevermind.\n".format(index = index+1)
                
                # Add in a delay to make selecting options more natural
                time.sleep(2)

                # Print out what option it has chosen, and as how the AI has been built, it will only sell the property that it is on currently
                print(sell_property_options.index(property_at_location) + 1)
                options_list.remove("Sell A Property")

                # Also check whether the player owns any more properties or not, if not, remove the option of displaying their own properties
                if len(player_obj.get_properties_owned()) == 0:
                    options_list.remove("Display Owned Properties")
                    
                    # Check if the option of building hotels still exists, if it does, remove it
                    if "Build a Hotel" in options_list:
                        options_list.remove("Build a Hotel")

            # Given that an option has been chosen have it buy, build, sell or skip a turn.
            player_obj.buy_or_build(move, self.property_locations)
            
            # Reset the user_prompt
            user_prompt = ""

            # If the AI has not won the game, then rebuild our options list and have it select "Next Player", else make the AI a winner
            if not player_obj.check_win(self.win_requirement):

                # This will start concatenating our options to user_prompt which would print out the options that the AI is able to pick
                for index in range(len(options_list)):
                    # Our index here gets added up by one and our elements are our options that are within the options_list
                    user_prompt += "[{index}] - {element} ".format(index = index+1, element = options_list[index])
                    
                    # Add in a colon at the last element
                    if index == len(options_list) - 1:
                        user_prompt += ": "

                # Have it select next player
                print(user_prompt + str(options_list.index("Next Player") + 1))
            
            # In the event that the AI did win, set self.ongoing to False
            else:
                self.ongoing = False
        
        # In the event that the target is not equal to our current location, have it select "Next Player"
        else:
            print("\n"+ str(options_list.index("Next Player") + 1))


########################################## Game ##########################################

    def start_game(self):
        """
        This function starts up the game full-fledged assuming that the prerequisites have been met beforehand.
        This will function will continue on looping until a player has won, or there aren't enough players to continue the game.

        Arguments:
        - none

        Returns:
        - none
        """

        # Loop through the game while the game is ongoing
        while self.ongoing:

            # Copy self.list_of_players
            list_of_players_copy = self.list_of_players.copy()

            # Work on a copy instead of the actual thing as it is easier to handle when a player quits the game and has to be removed from the list of players.
            for player in list_of_players_copy:

                 # Check if the number of players is 1, as the number of players may reduce if they decide to quit the game, in the event it is one, the remaining player will be the winner of the game.
                if len(self.list_of_players) == 1:
                    print("Game Over! {player_name} WINS!".format(player_name = self.list_of_players[0]))
                    self.ongoing = False

                    # Break out of the for loop
                    break

                # Also check if the number of players is 0
                elif len(self.list_of_players) == 0:
                    print("Everyone has quit the game.")
                    self.ongoing = False

                    # Break out of the for loop
                    break
                
                # Check the instance of the player, whether it is an AI player or not
                if isinstance(player, AIPlayer):
                    self.ai_player_turn(player)
                    print("\n\n")
                else:
                    # If it is not an AI player, then it is a regular player, so run the regular player turn method.
                    self.regular_player_turn(player)

                # Check whether self.ongoing has turned to False, if so break out of the for loop
                if self.ongoing == False:
                    break

####################################################################################
if __name__ == "__main__":
    # Test your function here
    game = PyPoly()
    # game.<add method name here>()
    pass

