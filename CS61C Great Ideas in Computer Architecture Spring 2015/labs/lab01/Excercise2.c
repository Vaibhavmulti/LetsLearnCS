#include <stdio.h>
#include <string.h>

// you may ignore the following two lines
#pragma GCC diagnostic ignored "-Wpragmas"
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"

int main(int argc, char** argv) {
	int i;
	char *str = "hello, world!", ch;
	for (i = 0; i < strlen(str); i++)
		ch = str[i];

	printf("%s\n",str);

	return 0;
}



/*
1)How do you pass command line arguments to a program when using gdb?
run arg1 arg2 ..

2)How do you set a breakpoint which only occurs when a set of conditions is true (e.g. when certain variables are a certain value)?
break ... if expression

3)How do you execute the next line of C code in the program after stopping at a breakpoint?
n(next line stepping over function calls)

4)If the next line of code is a function call, you'll execute the whole function call at once if you use your answer to #3. How do you tell GDB that you want to debug the code inside the function instead?
s(next stepping into function calls)

5)How do you resume the program after stopping at a breakpoint?
c (continue)

6)How can you see the value of a variable (or even an expression like 1+2) in gdb?
p expression (display the value of an expression)

7)How do you configure gdb so it prints the value of a variable after every step?
display expression

8) How do you print a list of all variables and their values in the current function?
info locals

9)How do you exit out of gdb?
quit

*/
