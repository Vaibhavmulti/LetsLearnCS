// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

@R0
D=M         //r0 stored in data reg

@n
M=D      //n=r0

@i
M=0     // i=0

@R2
M=0      //r2=0

(LOOP)
	@n
	D=M
	@END
	D;JEQ
	@R1
	D=M
	@R2
	M=M+D
	@i
	M=M+1
	D=M
	@n
	D=M-D
	@LOOP
	D;JGT

(END)
	@END
	0;JMP