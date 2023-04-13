// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

// /** 
//     if (R1 == 0) {
//         R2 = 0;
//         return;
//     }
//     int res = 0;
//     while (R1 != 0) {
//         res += R0;
//         R1 -= 1;
//     }
//     R2 = res
// */

// Assign 0 by default on register 2
    @R2
    M = 0

// load second register to D
    @R1 
    D = M

// Check if second is zero
    @END 
    D;JEQ

// initialize result at first it should be 0
    @result
    M = 0
(LOOP)
// load second number and decrease it
    @result
    D = M

    @R0
    D = D + M

    @result
    M = D

    @R1
    M = M - 1

    @R1
    D = M

    @LOOP
    D; JGT  

// Assign result to R2 register
    @result
    D = M

    @R2 
    M = D  

(END)
    @END
    0;JMP
