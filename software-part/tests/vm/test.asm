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
