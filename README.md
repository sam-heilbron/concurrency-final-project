# Concurrency (Comp50) Final Project
#### Authors: Rachel Marison, Sam Heilbron

### Concept

This is a game of tag, very similar to [agar.io](http://agar.io). Users join a game and they move around an enclosed space as a sphere trying to "eat" others. When they do, they become larger and as a result slower. If you are eaten, you are eliminated and the game is over. To "eat" someone you must overlap their center position. There are also small food items sitting around that don't move and allow players to grow easily. There are 2 forms of AI opponents, one type that moves randomly and another that moves towards you. You have 30 seconds to eat all the opponents (AI and Food) or you lose.


### How to Run

In order to run the program, you must first download getch and pygame. Find the "install" folder (/src/install). Inside the "instructions.txt" file describes how to download getch and pygame. Once everything is downloaded, you can run the program by going into the "src" folder and simply running "python main.py" or "./main.py".


### Included Files

* **main.py**: 
	Prints out an opening message explaining the rules of the game to the user. It then prompts the user to select their preferred form of input (mouse or keyboard). A game is then started by creating and running an instance of the Game class

* **games.py**:
	Contains all possible game classes. A **Game** is a wrapper for all components of a game. It keeps track of the users alive in the game (userList). It also keeps track of the gameboard, which is described more in boards.py below. It sets up all the users, draws and redraws them on the board, and kills users that have been eaten. It also listens for the game to finish by waiting on the gameOverFlag, which is signaled when the human is eaten, and the gameOverTimeout, which is signaled when the game clock has run out.

* **boards.py**:
	Contains all possible board classes. The **SyncGameBoard** class represents a thread-safe gameboard for the game. It handles creating a pygame display, a board containing the center position of all users, and a board containing locks for each position of the gameboard, thus allowing for atomic access on the gameboard. The SyncGameBoard is in charge of moving users from one place to another on the board as well as removing them once they have been eaten.

* **decisions.py**:
	Contains all possible decision classes. Decision classes represent the types of decisions that users make in order to move. All classes are built on top of the Basic class which connects the decision that is made to the movement class (see below).
	  * **Stationary** class always decides to stay in place. 
   	  * **KeyInput** class handles keyboard inputs to change the users direction.
      * **MouseInput** class handles mouse movements to change the users direction.
      * **AISmartInput** class decides to move towards where the human player is
      * **AIRandomInput** class randomly chooses a direction to go in

* **movements.py**:
	Contains all the possible movement classes. In this game, all user blobs are circles and the Circle_ class handles the actual movement of the users.
      * **Circle_** contains attributes related to its position (center, radius) and a semphare is required to get and set these values. It also contains a direction attribute which it shares with a decision class and thus another semaphore ensures atomic access to this value. The Circle class tells the board to update with it's new position and then is responsible for handling collisions. The Circle looks for locked positions on the gameboard that are within the radius of the circle.

* **users.py**:
    Contains all the possible user classes. All users are built off the base Blob class. The Blob class has decision and  movement classes (explained above), a color to display to the screen, and id to distinguish them from other blobs and a threading event isDead which is triggered when the user is eaten. This event kills the threads which are controlling the users decision and movement threads.
      * The **Human** class represent the human user in the game. The movement class is handled in a separate thread but pygame requires that IO be handled in the main thread.
      * The **AI** class is a base class for all non-human users. Both movement and decision instances are handled in separate threads.
      * **Food**, **AISmart**, and **AIRandom** all inherit the AI class and just vary in their attributes.

* **enums.py**:
	This file contains all enumerations used in the code. These include **Direction**, **Color**, **InitialUserRaidus**, and **Timeout**.


### Concurrency Decisions

* **Users decisions and movements**:
	Since humans can make a decision with their brain, while also doing something with their body, it makes sense for users of the game to have this capability. Therefore, the decision and movement classes are handled by 2 different threads. This successfully decouples the rates at which decision and movements are made. 

* **User movement**:
	There are 2 ways to handle moving users around. The first is to have all users wait at a turnstile and once everyone has arrived proceed and make a move. However, since users can move at different speeds, users would have to move more than 1 pixel at a time to account for varying speeds. However, this could create scenarios where users jump over eacher because they move so many pixels that they never collide but instead travel through eachother. Therefore, we used the alternative to user movement. Each user moves independently of others at an interval different from others. It is up to the scheduler to fairly allocate resources to each thread. This way, all users travel one pixel per movement. 
	  * **Side Effect**: Since the scheduler controls when the context is switched, 2 users may enter their loop to move, the first eats the second, kills it, and removes it from the board. However, the user that just died has already passed through the turnstile and will remain for 1 movement. We add a try...except to catch this case and throw it away. This is a required side effect of how we handle user movement. However, it is a better one than what would have occurred if we handled movement differently. 

* **User direction**:
	Since the ability to decide and move have been decoupled, the two classes now share a resouce (the user direction). Therefore, a Semaphore is used to ensure atomic access. 

* **User life (and death)**:
	Since there are 2 threads for each user (except the human), there needs to be a clear way to kill both threads. The isDead event is responsible for this. When it is triggered, both the movement and decision loops will terminate, killing the threads.

* **Board movement**:
	Multiple users are sharing a board and therefore a 2D array of Semaphores is required to ensure atomic access to a position. 

* **Collisions**:
	When 2 users collide, it must first be determined which one is larger. The smaller one will be terminated. However, one that is about to be killed will continue operating (and changing position) until it has registered to be killed. Therefore, the larger user must block the smaller user from moving, create a kind of turnstile, so that only after the smaller user has been killed will it be released. To do this, a Semaphore is place on the center of all users. The center is not a shared resouce (only the movement class changes it) but this allows other classes to acquire and hold the lock.

* **Drawing**:
	Drawing the board continually is a separate concept and thus handled in its own thread. This allows flexiblity with frequency of drawing.

* **User placement (on the board)**:
	Users are not guaranteed a placement on the board that is separate from all others. The only user guaranteed to not overlap anyone is the human. This was a design decision. As soon as the game begins, the larger blob will eat the smaller one. This variability (based on probability that 2 randomly chosen locations overlap) adds a level of excitement and randomness in the game.

* **Game termination**:
	There are three ways that the game can end. First, the user may run out of time. Second, they may be eaten by a larger AI. Finally, they may eat everything before the game clock reaches 0 and in doing so, win the game. There are 2 cases that must be handled: a collision triggering the human death and a timeout of the game clock. We treat these two cases in separate threads and then create a rendezvous to ensure that both terminate once one terminates.


### Challenges and Bugs

* **pygame brittleness**:
	We ran into a bug that disappeared only when we changed the size of the pygame display. Users were going out of bounds (outside the dimensions of the 2D array). This was causing and IndexError when the lock was acquired since the lock didn't exist. However, it's not possible that this happen since only the center of users actually acquire the lock and the closest they can make it to the border is their radius away from it. This seemed to flare up when a user ate another by the border but again, the radius would change, not the center as a result. After changing the display size, this error disappeared. We break this down to pygame being brittle because we have account for race conditions (there are none) and edge cases (off by 1 errors).