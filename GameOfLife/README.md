# Game of Life Challenge

The game is a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input. One interacts with the Game of Life by creating an initial configuration and observing how it evolves, or, for advanced players, by creating patterns with particular properties.

check out the wikipedia page for more information
https://hu.wikipedia.org/wiki/%C3%89letj%C3%A1t%C3%A9k

or check out a couple of cool videos on youtube:
* https://www.youtube.com/watch?v=C2vgICfQawE&t=136s
* https://www.youtube.com/watch?v=awmwgwkZ0q0
* https://www.youtube.com/watch?v=FWSR_7kZuYg

## Rules:

* Any live cell with fewer than two live neighbors dies, as if by under population.
* Any live cell with two or three live neighbors lives on to the next generation.
* Any live cell with more than three live neighbors dies, as if by overpopulation.
* Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.

## Challange
* Implement a working version of conway's game of life.
* Your solution should automatically run generation after generation, displaying the state of the word with an ascii art representation of the table.
* Try to stick to the OO principles we talked about last time.
* optionally it should take a seed to represent the initial state of the table.
* Use 'o' for living cells and '*' for dead/empty cells.
* Use a 20 * 20 matrix as table. 
* (optional) your solution should take an argument describing the dimensions of the table.
* (optional) try implement a color version of the game.
* (optional) make your solution available as a cli app (click)
* (optional) try to create a web api exposing your game of life (flask), in a maner the api returns a generation of your table every call of the api. Make reseting or seeding the game available though the api.

You will most likely need Table and Cell classes, but try to think about what else you could abstract away?
