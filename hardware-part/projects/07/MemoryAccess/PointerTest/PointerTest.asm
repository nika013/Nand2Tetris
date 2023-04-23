// push constant 3030
@3030
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 0
@3
D=A
@15
M=D
@SP
AM=M-1
D=M
@15
A=M
M=D

// push constant 3040
@3040
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1
@4
D=A
@15
M=D
@SP
AM=M-1
D=M
@15
A=M
M=D

// push constant 32
@32
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop this 2
@2
D=A
@THIS
D=M+D
@15
M=D
@SP
AM=M-1
D=M
@15
A=M
M=D

// push constant 46
@46
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop that 6
@6
D=A
@THAT
D=M+D
@15
M=D
@SP
AM=M-1
D=M
@15
A=M
M=D

// push pointer 0
@3
D=M
@SP
A=M
M=D
@SP
M=M+1
// push pointer 1
@4
D=M
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
// push this 2
@2
D=A
@THIS
A=M+D
D=M
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
// push that 6
@6
D=A
@THAT
A=M+D
D=M
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
