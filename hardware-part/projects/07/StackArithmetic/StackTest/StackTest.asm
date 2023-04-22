// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
A=M-1
D=M
A=A-1
D=M-D
@TRUE1
D;JEQ
@SP
A=M-1
A=A-1
M=0
@CONT1
0;JMP
(TRUE1)
@SP
A=M-1
A=A-1
M=-1
(CONT1)
@SP
M=M-1

// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
A=M-1
D=M
A=A-1
D=M-D
@TRUE2
D;JEQ
@SP
A=M-1
A=A-1
M=0
@CONT2
0;JMP
(TRUE2)
@SP
A=M-1
A=A-1
M=-1
(CONT2)
@SP
M=M-1

// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
A=M-1
D=M
A=A-1
D=M-D
@TRUE3
D;JEQ
@SP
A=M-1
A=A-1
M=0
@CONT3
0;JMP
(TRUE3)
@SP
A=M-1
A=A-1
M=-1
(CONT3)
@SP
M=M-1

// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
A=M-1
D=M
A=A-1
D=M-D
@TRUE4
D;JLT
@SP
A=M-1
A=A-1
M=0
@CONT4
0;JMP
(TRUE4)
@SP
A=M-1
A=A-1
M=-1
(CONT4)
@SP
M=M-1

// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
A=M-1
D=M
A=A-1
D=M-D
@TRUE5
D;JLT
@SP
A=M-1
A=A-1
M=0
@CONT5
0;JMP
(TRUE5)
@SP
A=M-1
A=A-1
M=-1
(CONT5)
@SP
M=M-1

// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
A=M-1
D=M
A=A-1
D=M-D
@TRUE6
D;JLT
@SP
A=M-1
A=A-1
M=0
@CONT6
0;JMP
(TRUE6)
@SP
A=M-1
A=A-1
M=-1
(CONT6)
@SP
M=M-1

// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
A=M-1
D=M
A=A-1
D=M-D
@TRUE7
D;JGT
@SP
A=M-1
A=A-1
M=0
@CONT7
0;JMP
(TRUE7)
@SP
A=M-1
A=A-1
M=-1
(CONT7)
@SP
M=M-1

// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
A=M-1
D=M
A=A-1
D=M-D
@TRUE8
D;JGT
@SP
A=M-1
A=A-1
M=0
@CONT8
0;JMP
(TRUE8)
@SP
A=M-1
A=A-1
M=-1
(CONT8)
@SP
M=M-1

// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
A=M-1
D=M
A=A-1
D=M-D
@TRUE9
D;JGT
@SP
A=M-1
A=A-1
M=0
@CONT9
0;JMP
(TRUE9)
@SP
A=M-1
A=A-1
M=-1
(CONT9)
@SP
M=M-1

// push constant 57
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 53
@53
D=A
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
A=M-1
D=M
A=A-1
D=D+M
M=D
@SP
M=M-1
// push constant 112
@112
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
A=M-1
D=M
A=A-1
D=M-D
M=D
@SP
M=M-1
// neg
@SP
A=M-1
M=-M
// and
@SP
A=M-1
D=M
A=A-1
M=D&M
@SP
M=M-1
// push constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
// or
@SP
A=M-1
D=M
A=A-1
M=D|M
@SP
M=M-1
// not
@SP
A=M-1
M=!M
