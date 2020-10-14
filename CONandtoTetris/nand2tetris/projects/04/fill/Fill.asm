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

(INFLOOP)
	@KBD
	D=M
	@WHITE
	D;JEQ
	@SCREEN   // base location of screen
	D=A
	@addr
	M=D		//addr pointer =base location of screen
	@i
	M=0
	@8192
	D=A
	@n
	M=D   
	// total registers we need for 256*512 sized screen (131072 pixels)
	(LOOP1)
		@i
		D=M
		@addr
		A=M+D
		M=-1
		@i
		M=M+1
		D=M
		@n
		D=M-D
		@LOOP1
		D;JGT
	
	@INFLOOP
	0;JMP

(WHITE)
	@SCREEN   // base location of screen
	D=A
	@addr1
	M=D		//addr pointer =base location of screen
	@i1
	M=0
	@8192
	D=A
	@n1
	M=D 
	// total registers we need for 256*512 sized screen (131072 pixels)
	(LOOP2)
		@i1
		D=M
		@addr1
		A=M+D
		M=0
		@i1
		M=M+1
		D=M
		@n1
		D=M-D
		@LOOP2
		D;JGT
	@INFLOOP
	0;JMP