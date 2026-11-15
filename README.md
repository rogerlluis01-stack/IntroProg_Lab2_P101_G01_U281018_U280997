ab 2: Pong Game Report

Team and Contribution: 
  Roger: the game functions (movement, collisions and ball reset), the GitHub repository, and the Problems and Solutions and Testing sections.
  Maya: the configuration menu, the AI opponent, and the rest of the report.
We tested the game and reviewed the final version together.

Overview of the Design: 
  The program is divided into functions, each responsible for one part of the game. When it starts, the configuration menu asks whether the player wants to change the default settings and colours, and the chosen values are used to initialise the game before the main loop begins.
  In the main loop, move_paddle() and move_ball() update the positions of the paddles and the ball, while collide_ball_walls() and collide_ball_paddle() detect collisions and adjust the ball's movement. compute_ai_direction() moves the right paddle in one-player mode, and reset_ball() returns the ball to the centre after a point. The program uses no global variables: all information is passed through parameters and return values.

Key Implementation Decisions: 
  Ball–Paddle Collision: 
    collide_ball_paddle() uses a bounding-box method. It calculates the edges of the ball from its centre and radius, and the edges of the paddle from its position, width and height. A collision occurs when the two boxes overlap:
    if ball_right >= pad_left and ball_left <= pad_right and ball_bottom >= pad_top and ball_top <= pad_bottom:
    To stop the ball from getting stuck and detecting the same collision repeatedly, the ball is first moved just outside the paddle, on the side it came from, and then its horizontal velocity is reversed (vx = -vx). The function returns the new position and velocity, and a Boolean indicating whether a collision occurred.

Input Validation: 
  ask_yes_no() repeats the question until it gets a valid answer, ignoring capital letters and extra spaces. 
  read_int_in_range() uses try and except to check that the input is an integer, then checks that it is within the allowed range, and repeats until both conditions are met. We use it for the red, green and blue values of the colours, which have no default. 
  read_int_in_range_w_default() works the same way but lets the user press Enter to keep the default value, and get_config() uses it for paddle height, paddle speed, ball speed and ball radius. 
  change_colors() either returns the default colours (black and white) or lets the user choose new ones through read_color().

Problems and Solutions: 
  Uploading to GitHub 
    Our first push uploaded the whole IntroProg_Lab2_P101_G01_U280997_U281018 folder, so pong.py ended up inside extra folders, and the next push was rejected with "rejected (fetch first)". We noticed both by checking the repository on GitHub and reading the terminal. The cause was that we ran Git from an outer folder that was already a repository, and Git uploads the whole repository it is run from; GitHub then held commits that our local copy did not have. We fixed it by running git init inside the lab folder, connecting it to the correct repository and pushing again.
  Ball Angle After Hitting a Paddle
    During long rallies, the ball sometimes came off the paddle perfectly flat, and after many hits it became steeper and faster. The cause was that the hit position was added to the ball's current vertical speed instead of setting a new one, so the speed could reach zero or keep growing. 
    Staying Inside the Play Area
    Paddles could move partly off the screen, and the ball could flicker at the top or bottom wall. We saw this by holding the keys at the screen edges and watching fast bounces. Positions were updated without checking the window limits, and the ball could pass the wall within one frame, so reversing its speed left it outside and it was reversed again on the next frame. We now clamp each paddle between 0 and the window height minus the paddle height, and when the ball hits a wall we reverse its vertical speed and move it back inside by its radius.


Testing: 
  We tested each part separately while writing it, and then played full games. In the configuration menu, we entered letters, decimals, negative numbers, empty input and out-of-range values, and the program always asked again instead of crashing. Pressing Enter kept the default values, and the chosen settings changed the game. We moved both paddles to the screen edges with different paddle heights, watched the ball bounce off the walls at different speeds, and hit it with the centre and ends of the paddle to check the bounce angle and that it never got stuck. 
  We also checked that the correct player scored, that the ball reset to the centre, and that both the AI and two-player modes worked.

Optional Features: 
  -AI-Controlled Opponent
    In one-player mode, compute_ai_direction() compares the ball's vertical position with the centre of the right paddle. It returns -1 to move up if the ball is above it, 1 to move down if it is below it, and 0 otherwise. A 10-pixel tolerance stops the paddle from constantly making small movements. Before the main loop, the program asks whether the user wants to play against the machine, and the loop then either calls compute_ai_direction() or reads the keyboard for the right paddle.
  -Default Values
    read_int_in_range_w_default() lets users keep the predefined settings by pressing Enter instead of typing every value.

Use of AI Tools: 
  We used Claude, an AI assistant, to answer questions and understand concepts. It did not write the game, and all the functions in pong.py were written by us. We used it to solve setup problems (pygame not installing on Python 3.15, which led us to pygame-ce, and VS Code using the wrong Python), to understand Git and fix our upload problems, and to clear up doubts about the game logic, such as why the ball must be moved back inside the wall and how to keep the paddles on the screen. We also asked it to review functions we had written, and it pointed out that the ball's vertical speed could reach zero. 
  Finally, it helped us organise and word some sections of this report, which we reviewed and edited so they describe what we actually did. We understood every answer before using it and can explain every line of our code.
