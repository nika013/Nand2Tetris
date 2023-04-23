// push constant 10
@10
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 15
@15
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 13
@13
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop local 0
@0
D=A
@LCL
D=M+D
@15
M=D
@SP
AM=M-1
D=M
@15
A=M
M=D

// pop argument 1
@1
D=A
@ARG
D=M+D
@15
M=D
@SP
AM=M-1
D=M
@15
A=M
M=D

// push argument 1
@1
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// push local 0
@0
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
