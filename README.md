# shooting_game
A 2D side-scrolling shooting game built with Python and the Pygame library, inspired by the anime 86 - Eighty Six. Players control an Undertaker mech to dodge enemies and fire bullets to attack incoming forces on the battlefield.

## 🔷 Game Flow and Control Logic

### Screen Initialization and Main Menu
* Use pygame.display.set_mode to create the game window (600x400)
* Load image assets: background, player mech, enemy units, and bullets
* Use pygame.font to display the title, game instructions, and prompts
* Click the mouse to start the game (detect MOUSEBUTTONDOWN)

### Player Control and Shooting
* The player uses the left and right arrow keys to move the mech horizontally
* Press the up arrow key (↑) to shoot a bullet upward
* The mech cannot move outside the screen boundaries; its position is automatically restricted

### Enemy Generation and Movement
* Each game session spawns 8 enemies automatically
* Enemies appear randomly from the top of the screen and move downward and sideways at random speeds
* Once they move off-screen, they respawn at a random top position

### Bullet and Enemy Collision Logic
* Use groupcollide() to detect when bullets hit enemies
* When hit, both the bullet and enemy disappear, the score increases by 10, and a new enemy is spawned

### Player Collision and Life Management
* Use spritecollide() with circular collision (collide_circle) to detect collisions with enemies
* When hit, the player's life decreases by 10; if life reaches 0, the game enters the Game Over state

## 🔷 Game Over Handling and Restart
* When the player dies, a Game Over screen and message are displayed
* The player can click the mouse to return to the initial screen and start a new game
* A while game_over: loop is used to pause game updates and freeze the screen while waiting for input

