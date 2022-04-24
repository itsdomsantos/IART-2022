# IART-2022

## Requirements

Make sure that this modules are installed to run the program

- [Python](https://www.python.org/downloads/)
- [pygame](https://www.pygame.org/wiki/GettingStarted#Pygame%20Installation)
- [Numpy](https://numpy.org/install/)

## Running the program

Run using the command
``` 
python main.py
```

## Instructions

- Choose if you want to play in the terminal or in a more interactive way using pygame
- Choose in terminal if you want to see ai working or do the puzzle by yourself


### Single player mode - pygame

- Before playing the game you are asked to choose the level in terminal (1-10 5x5) (11-20 6x6)
- The board will appear next
- Now choose the tile for your move, if it is accepted it will turn green otherwise nothing will append
- To ask an hint enter 'H'
  - If you have a possible solution move, the corresponding tile will appear in **blue**
  - Otherwise, the current position will become **red**, indicating that you are in the wrong way, so it's better to undo last move.
- To undo last movement enter 'U'
- If you reach an dead-state, which means no more moves allowed the board will automatically reset
- To exit game enter press 'Esc' 


### Single player mode - terminal

- Before playing the game you are asked to choose the level in terminal (1-10 5x5) (11-20 6x6)
- The board will appear next
- Now choose the move to perform (w-up, a-left, s-down, d-right) and press enter
- If you reach an dead-state, which means no more moves allowed the board will automatically reset
- To exit game enter press 'Esc' 


### AI mode 

- Choose the algorithm you want to use
- If you choose greedy or a-star choose also and heuristic
- Then, depending if you choose terminal or pygame you'll see an animated calculation of the algorithm