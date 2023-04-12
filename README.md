Assignment 2: 2048
=========
DO NOT FORK THIS REPO
----
Implement a game AI for the 2048 game based on expectimax search. The base game engine uses code from [here](https://gist.github.com/lewisjdeane/752eeba4635b479f8bb2). 

Due date
-----
Apr-30 11:59pm. 

Task To Complete
-----
Model the AI player as a max player, and the computer as a chance player (picking a random open spot to place a 2-tile). Implement a depth-3 game tree and the expectimax algorithm to compute decisions for the AI player. Use the score returned by the game engine as the evaluation function value at the leaf nodes of the depth-3 game trees. 

You can play the game manually using the arrow keys. Pressing 'Enter' will let the AI play, and pressing 'Enter' again will stop the AI player. Read the game engine code from `game.py` and see how it returns the game state, and evaluate its score from an arbitrary game state after an arbitrary player move. 

A depth-3 game tree means the tree should have the following levels: 

- root: player
- level 1: computer 
- level 2: player
- level 3: terminal with payoff (note that we say "terminal" to mean the leaf nodes in the shallow game tree, not the termination of the game itself)

This tree represents all the game states of a player-computer-player sequence (the player makes a move, the computer places a tile, and then the player makes another move, and then evaluate the score) from the current state. Compute the expectimax values of all the nodes in the game tree, and return the optimal move for the player. In the starter code, the AI just returns a random move.

If you have implemented the AI correctly, your depth-3 search should almost always reach 512 tiles and a score over 5000 quite often, as shown in the movie file. 

Usage
-----
To run the program:
```
    python main.py
```

The file 'test.py' contains code for testing that with the depth-3 tree and the expectimax algorithm, your AI returns the right directions and values on 15 test states. Run the tests using:
```
    python main.py -t 1
```

Once your program is running, here are a few keyboard options available in-game:
- 'r': restart the game
- 'u': undo a move
- '3'-'7': change board size
- 'g': toggle grayscale
- 'e': switch to extra credit

NOTE: For grading, we will run tests in the same way on other test states and see if your depth-3 tree and expectimax values are computed correctly. 

Extra credit (3 points)
------
While depth-3 search gives okay performance, it can apparently be improved by searching more depth or improving the evaluation function, or both. For improving the evaluation function, you can implement a heuristic value that takes into account of the difference between a "good" and "bad" game state. You can feel free to use online resources to see what strategies people have been using to reach higher scores in 2048. 

If you want to try this extra credits part, implement a stronger AI in the `compute_decision_ec` function at the bottom of the `ai.py` file. When running the game, pressing `e` will activate/deactivate the decisions made by the `compute_decision_ec` function. 

You can get up to 3 extra points if you can engineer the AI to reach 2048 often (achieving a score of more than 20,000 on at least 4/10 runs), while each step does not take too long when running on a laptop. Note that if you implement a large tree, the search may make each decision so slow that you do not want to watch it play. In that case you want to think about how to improve the implementation, or think about improving the design of the evaluation function instead. 

To test your extra credit implementation, run:

```
    python main.py -t 2
```

NOTE: In order to get the extra credits, you will need to achieve a score of more than 20,000 on at least 4/10 runs. The tester will show whether you have succeeded. 

Submission
----
You only need to submit the `ai.py` file on Gradescope for grading. 

If you have changed other files, make sure that your implementation works properly with the given `main.py` and `game.py`, and `test.py` which we will use for grading. Although you won't be able to see the results of the hidden tests this time, the grading metrics are the same as PA1 (if you code fails the tests in `test.py` it will not get more than the Half grade). 
- Full (15 points): Everything is correct, passing all tests and implementing the right algorithms.
- Almost (13 points): There are minor mistakes that led to failure of some tests. 
- Half (8 points): Major problems, such as not implementing some of the algorithms, but are in the right direction. 
- Null (1 point): Almost no attempt but at least you sent something in. 

In addition, there are 3 extra points (as described in `extra credit` section above).

You can change almost anything in the starter code in `ai.py` except the the `compute_decision` function. This function will be used by the tester. 


Tips & FAQ
-----
- Before you begin, it's wise to first get familiar with the workflow of the program and instance variables across files. We're just going to keep advising you do that in case you don't already :)
- Again, you may find `pdb` extremely helpful to understand and debug your code. It is the Python debugger, similar to `GDB`. Here's a [quick tutorial](https://www.youtube.com/watch?v=VQjCx3P89yk&ab_channel=TutorialEdge).
- Set up a virtual environment (refer to PA1 for setting up Anaconda) if you don't want to pollute your global package space. This is optional, and if it takes too much time, probably not worth it.
