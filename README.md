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
