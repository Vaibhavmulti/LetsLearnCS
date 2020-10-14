#Clear the whitescapes and the comments and writes to the intermediate file
name_of_file='StackTest'  #Replace with the file name
with open("StackTest.vm") as f:
    with open("Rwhitespaces.vm",'w') as g:
        for line in f:
            if len(line.split())==0:
                continue
            for word in line.split():
                if word[0]=='/' and word[1]=='/':
                    break
                g.write(word+' ')
            if line.split()[0]!="//":
                g.write('\n')

label_index=1 #for marking labels with index so that they get unique
#Start Converting to Assembly level language line by line
with open("Rwhitespaces.vm") as f:
    with open("StackTest.asm",'w') as g:
        for line in f:
            if len(line.split())==0:
                continue
            words=line.split()
            if(words[0]=='push' or words[0]=='pop'):
                if (words[1] == 'constant' or words[1] == 'temp'
                        or words[1] == 'pointer' or words[1] == 'static'):
                    if (words[1] == 'constant'):
                        g.write('@{}\n'.format(words[2]))
                    elif (words[1] == 'temp'):
                        g.write('@{}\n'.format(str((int(words[2]) + 5))))
                    elif (words[1] == 'static'):
                        g.write('@{}.{}\n'.format(name_of_file, words[2]))
                    else:
                        if int(words[2]) == 0:
                            g.write('@THIS\n')
                        else:
                            g.write('@THAT\n')
                    g.write('D=A\n')
                    g.write('@R13\n')  # general purpose register
                    g.write('M=D\n')
                    g.write('A=D\n')
                else:
                    g.write('@{}\n'.format(words[2]))
                    g.write('D=A\n')
                    if (words[1] == 'local'):
                        g.write('@LCL\n')
                    elif (words[1] == 'argument'):
                        g.write('@ARG\n')
                    elif (words[1] == 'this'):
                        g.write('@THIS\n')
                    elif (words[1] == 'that'):
                        g.write('@THAT\n')
                    g.write('D=D+M\n')
                    g.write('@R13\n')  # general purpose register
                    g.write('M=D\n')
                    g.write('A=D\n')
                if(words[0]=='push'):
                    if(words[1]=='constant'):
                        g.write('D=A\n')
                    else:
                        g.write('D=M\n')
                    g.write('@SP\n')
                    g.write('A=M\n')
                    g.write('M=D\n')
                    g.write('@SP\n')
                    g.write('M=M+1\n')
                elif(words[0]=='pop'):
                    g.write('@SP\n')
                    g.write('AM=M-1\n')
                    g.write('D=M\n')
                    g.write('@R13\n')
                    g.write('A=M\n')
                    g.write('M=D\n')
            else:
                if words[0] not in ('neg','not'):
                    g.write('@SP\n')
                    g.write('AM=M-1\n')
                    g.write('D=M\n')
                    g.write('@SP\n')
                    g.write('AM=M-1\n')
                if(words[0]=='add'):
                    g.write('M=D+M\n')
                elif(words[0]=='sub'):
                    g.write('M=M-D\n')
                elif (words[0] =='neg'):
                    g.write('@SP\n')
                    g.write('AM=M-1\n')
                    g.write('M=-M\n')
                elif (words[0] == 'and'):
                    g.write('M=D&M\n')
                elif (words[0] == 'or'):
                    g.write('M=D|M\n')
                elif (words[0] =='not'):
                    g.write('@SP\n')
                    g.write('AM=M-1\n')
                    g.write('M=!M\n')
                elif (words[0] == 'gt'):
                    g.write('D=D-M\n')
                    g.write('@GTZ{}\n'.format(label_index))
                    g.write('D;JLT\n')
                    g.write('@SP\n')
                    g.write('A=M\n')
                    g.write('M=0\n')
                    g.write('@ENDGT{}\n'.format(label_index))
                    g.write('0;JMP\n')
                    g.write('(GTZ{})\n'.format(label_index))
                    g.write('@SP\n')
                    g.write('A=M\n')
                    g.write('M=-1\n')
                    g.write('@ENDGT{}\n'.format(label_index))
                    g.write('0;JMP\n')
                    g.write('(ENDGT{})\n'.format(label_index))
                    label_index+=1
                elif (words[0] == 'lt'):
                    g.write('D=D-M\n')
                    g.write('@LTZ{}\n'.format(label_index))
                    g.write('D;JGT\n')
                    g.write('@SP\n')
                    g.write('A=M\n')
                    g.write('M=0\n')
                    g.write('@ENDLT{}\n'.format(label_index))
                    g.write('0;JMP\n')
                    g.write('(LTZ{})\n'.format(label_index))
                    g.write('@SP\n')
                    g.write('A=M\n')
                    g.write('M=-1\n')
                    g.write('@ENDLT{}\n'.format(label_index))
                    g.write('0;JMP\n')
                    g.write('(ENDLT{})\n'.format(label_index))
                    label_index += 1
                elif (words[0] == 'eq'):
                    g.write('D=D-M\n')
                    g.write('@EQZ{}\n'.format(label_index))
                    g.write('D;JEQ\n')
                    g.write('@SP\n')
                    g.write('A=M\n')
                    g.write('M=0\n')
                    g.write('@ENDEQ{}\n'.format(label_index))
                    g.write('0;JMP\n')
                    g.write('(EQZ{})\n'.format(label_index))
                    g.write('@SP\n')
                    g.write('A=M\n')
                    g.write('M=-1\n')
                    g.write('@ENDEQ{}\n'.format(label_index))
                    g.write('0;JMP\n')
                    g.write('(ENDEQ{})\n'.format(label_index))
                    label_index += 1
                g.write('@SP\n')
                g.write('M=M+1\n')









