# Comp50: Concurrency 
## Final Project
### Authors: Rachel Marison, Sam Heilbron

 This is a game of tag, very similar to Agar.io (check it out in
    your web browser). Basically, users join a game and they move around an
    enclosed space as a spehere trying to "eat" others. When they do, they 
    become larger and as a result slower. If you are eaten, you are eliminated.
    To "eat" someone you must completely overlap their positition with yours. 
    Just touching them doesn't result in anything. There are also small food 
    items sitting around that don't move and allow players to get food easily. 
    Players may also split themselves in half, and have 2 smaller spheres 
    moving around together. This allows them to move faster, but makes it harder
    to eat others since they're smaller.


Included Files:
1. main.py:
	Prints out an opening message
    Prompts the user to choose between mouse input and key input
    Starts the game

2. games.py:
	Contains all possible game classes. A Game is a wrapper for all components of a game. It keeps track of the users alive in the game (userList). It also keeps track of the gameboard, which is described more in boards.py below. It sets up all the users, draws and redraws them on the board, and kills users that have been eaten. It also listens for the game to finish by waiting on the gameOverFlag, which is signaled when the human is eaten, and the gameOverTimeout, which is signaled when the game clock has run out.

3. boards.py:
	Contains all possible board classes. The SyncGameBoard class represents a thread-safe gameboard for the game. It handles creating a pygame display, a board containing the center position of all users, and a board containing locks for each position of the gameboard, thus allowing for atomic access on the gameboard. The SyncGameBoard is in charge of moving users from one place to another on the board as well as removing them once they have been eaten.

4. decisions.py:
	Contains all possible decision classes. Decision classes represent the types of decisions that users make in order to move. All classes are built on top of the Basic class which implements the decision. 
       	- The Stationary class is used to represent the decisions that stationary users (food) make. Since food can't move, all they do is wait in one spot to be eaten by another user. 
        - The KeyInput class represents decisions made by users using the keyboard as their input. It waits for a decision to occur, or in other words, for an arrow key to be pressed, and then the movement class handles the actual turning of the user.
        - The MouseInput class is exactly like the KeyInput class, except instead of waiting for a key to be pressed, the decision is based on the location of the mouse on the screen.
        - The AISmartInput class represents the AI computer players that are "smart" and moves towards the human user. This class looks at the current location of the human on the board, and then calls the movement class to turn in that direction.
        - The AIRandomInput class represents the AI computer players that aren't "smart". We decided to have both smart and random AI players in order to make the game a bit easier to play. This class is just like the AISmartInput class, except it randomly chooses a direction to go in

5. movements.py:
	Contains all the possible movement classes. In this game, all user blobs are circles and the Circle_ class handles the actual movement of the users.
        	•Circle contains attributes like center, (the center position of the circle), radius (the radius of the circle), and direction (the current direction that the circle is going in). The Circle class also has the mutexes positionMutex (has access to the center and radius variables) and directionMutex (has access to the direction variable).
        	•The Circle class handles movement by calling moveUser() in boards.py, which removes the user from it's current position (removes the user ID from the players board, and releases the lock in the lock board), places the user on it's new position (setting the user ID to the new position in the players board and acquiring the new lock in the lock board), and finally sets the center attribute to the new center position. After moving the user, the checkCollisions() function is called. This function checks all positions in the lock board that lie within the user’s radius to see if any of the positions are locked. If there are, that means a collision has occurred, and the bigger user will "eat" the smaller user.
6. users.py:
            •The Blob class is a basic user class, which all other classes inherit from. The Blob class has attributes id, color, decision, movement, and isDead. The attributes decision and movement are the decision and movement classes that the specific user has. isDead is a threading event that represents the life of a blob. It is triggered when the blob is killed.
            •The Human class represent the human user in the game. When the game starts, the Human class will spawn off a thread to move at regular intervals based on the user's decisions. The larger the user is, the slower the intervals will be, thus making bigger users move slowly and smaller users move fast.
            •The AI class is a base class for all non-human users. When the game starts, it will spawn off two threads, one for regularly waiting for decisions, and the other for regularly moving based on the decisions. Again, the larger the user is, the slower the movement intervals will be.
            •The Food class, AISmart class, and AIRandom class all inherit the AI class. Food has the decision class Stationary and the movement class Circle. AISmart has the decision class AISmartInput and the movement class Circle. AIRandom has the decision class AIRandomInput and the movement class Circle. 

7. enums.py:
•This file contains all enumerations, including Direction, Color, InitialUserRaidus, and Timeout.



Program Architecture:
	A game (games.py) consists of a board (boards.py) and a group of users (user.py)
	Users may be either a Human, Food or AI. All Users have a base class called blob.
	Users have a class for decisions and a class for movement. 
		Decisions (decisions.py) may be either Stationary, MouseInput, KeyInput or AiInput.
		Movement (movements.py) may be a Sphere (possible others to come soon)
	For all users, the decision and movement classes run in 2 separate threads.
	For the lone human, the decision (either key input or mouse input) class runs
		in the main thread since that is required. 

	The way the decisions and movement classes work together is that the decision class
		loops every few milliseconds and using the input (key or mouse) updates the intended direction of the user. In another thread, the movement class operates at a frequency based on its size. The larger it gets, the slower the interval. At every interval, the movement class updates the position of the user. These two classes share access to the direction variable so a mutex ensures atomic access to it.
