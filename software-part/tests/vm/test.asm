// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 100
@100
D=A
@SP
A=M
M=D
@SP
M=M+1
// not
@SP
A=M-1
M=!M
