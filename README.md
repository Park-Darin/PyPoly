# PyPoly 💰

## Introduction

PyPoly is a text-based board game inspired by Monopoly, developed using advanced Python concepts. Unlike traditional Monopoly, the goal in PyPoly is to be the first player to purchase a certain number of properties of the same color group and build at least one hotel on each of those properties. Players also have unique move traits, adding a strategic layer to their movement around the game board.

## Features

### 1. Property Management

- **Property Creation**: Properties are categorized into color groups (Blue, Green, Red, Yellow) with attributes like name, cost, hotel cost, rent price, and ownership status.
- **Hotel Construction**: Players can build hotels on their properties to increase rent. A maximum of two hotels can be built per property.

### 2. Player Management

- **Player Attributes**: Players have names, symbols, funds, move traits, positions, and owned properties.
- **Fund Management**: Methods to add or reduce funds based on game events.
- **Property Transactions**: Players can purchase, sell properties, and build hotels if they have sufficient funds.

### 3. Game Board

- **Board Setup**: The game board is an n x n grid with properties and chance grids (penalty/reward).
- **Player Movement**: Players move based on their chosen trait (perpendicular, diagonal, or L-shaped moves).

### 4. AI Player

- **AI Strategy**: AI players make strategic decisions based on property ownership and available funds.
- **Automated Moves**: AI players automatically choose the best move and decide on property transactions.

### 5. Game Dynamics

- **Random Start**: Players start at random positions on the board with an initial fund of $150.
- **Chance Grids**: Landing on a chance grid can result in penalties or rewards.
- **Rent Payments**: Players pay rent when landing on properties owned by other players, with rent increasing by 20% per hotel built.

### 6. Winning Condition

- **Victory Criteria**: The first player to purchase the target number of properties of the same color group and build at least one hotel on each wins the game.

## Example ScreenShots

Here are some screenshots to showcase how the game works:

###### The game starts with players positioned randomly on the board.
<img width="525" alt="Screenshot 2024-08-15 at 5 09 35 AM" src="https://github.com/user-attachments/assets/ba859303-a382-4e78-9c1f-3916acad6145">

###### Players move based on their chosen move traits.
<img width="508" alt="Screenshot 2024-08-15 at 5 10 08 AM" src="https://github.com/user-attachments/assets/357be444-e8e0-4fa6-b087-0fa2bef1bf87">

###### Players can purchase properties when they land on them.
<img width="703" alt="Screenshot 2024-08-15 at 5 10 54 AM" src="https://github.com/user-attachments/assets/0423056a-3b38-4eb9-a2cc-2e8ebc21c4f7">

###### AIs made decision and move by their own.
<img width="545" alt="Screenshot 2024-08-15 at 5 17 27 AM" src="https://github.com/user-attachments/assets/02b0487e-74e3-49c9-b261-d4dd02577b16">

###### Players can build hotels on their properties to increase rent.
<img width="796" alt="Screenshot 2024-08-15 at 5 13 09 AM" src="https://github.com/user-attachments/assets/399fbc0b-3902-4a39-a327-d93db5a4f9a2">

###### Players can sell a properties to increase own fund.
<img width="683" alt="Screenshot 2024-08-15 at 5 14 20 AM" src="https://github.com/user-attachments/assets/57523492-90fa-428a-863a-c11757a1f6c2">

###### The game announces the winner once the victory criteria are met.
<img width="805" alt="Screenshot 2024-08-15 at 5 15 54 AM" src="https://github.com/user-attachments/assets/9a94370c-1030-4ec5-b3c7-b0a64bf89d9e">


## Usage

1. **Start the Game**: Launch the game and follow the prompts to set up players, choose move traits, and define the winning condition.
2. **Gameplay**: Take turns moving around the board, purchasing properties, building hotels, and managing funds.
3. **Winning the Game**: Achieve the victory criteria to win the game.

## Conclusion

PyPoly provides an engaging and strategic twist on the classic Monopoly game, leveraging advanced Python programming concepts. With unique movement traits, AI players, and a dynamic game board, PyPoly offers a challenging and enjoyable gaming experience.

For more details and the complete source code, please refer to the project repository.
