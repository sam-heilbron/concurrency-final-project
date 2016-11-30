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
