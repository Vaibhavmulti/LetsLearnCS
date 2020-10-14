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
	(LOOP)
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
		@LOOP
		D;JGT
	(INF)
	@INF
	0;JMP
