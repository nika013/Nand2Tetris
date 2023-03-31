// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// Screen (16384 - [0, 8191]) - memory map unit
// addKeyListeners();
// while (true) {
//    if (keyIsPressed) {
//      makeColor(black);
//    } else {
//      makeColor(white);        
//    }
// void makeColor(int[] color) {
//      for (int i = 0; i < 255; i++) {
//          for (int j = 0; j < 512; j++) {
//              Screen[32*i + col / 16] = color;
//          }    
//      }
//  }
//}


// infinite loop for recognizing key pressing
// loop for modifying screen

(LISTENER)
@KBD
D = M

// if key is not pressed color shuld be 0
@WHITE
D; JEQ

@color
M = -1

// if key is not 0 go to screen loop
@SCREEN_LOOP_INIT
D; JGT

(WHITE)
@color 
M = 0

(SCREEN_LOOP_INIT)
@SCREEN
D = A // save screen offset

@i 
M = D

// for determining ending registers
@8191
D = A

@screen_end
M = D + 1

(SCREEN_LOOP)

@color
D = M

// assign color
@i
A = M
M = D

// increase index
@i 
M = M + 1

// decrease count of screen registers
@screen_end
M = M -1

// check if there is still one iteration
@screen_end
D = M

@SCREEN_LOOP
D;JGT

(RESET)
@LISTENER
0;JMP