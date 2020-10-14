import os
function_return_index=1 #return address for every function call
label_index = 1  # for marking labels with index so that they get unique

def calling_function(words):
    # push return address first
    global function_return_index
    g.write('@{}$ret.{}\n'.format(words[1], function_return_index))
    function_return_index += 1
    g.write('D=A\n')
    g.write('@SP\n')
    g.write('A=M\n')
    g.write('M=D\n')
    g.write('@SP\n')
    g.write('M=M+1\n')
    # saving local,arg,this,that of the caller
    g.write('@LCL\n')
    g.write('D=M\n')
    g.write('@SP\n')
    g.write('A=M\n')
    g.write('M=D\n')
    g.write('@SP\n')
    g.write('M=M+1\n')
    # arg
    g.write('@ARG\n')
    g.write('D=M\n')
    g.write('@SP\n')
    g.write('A=M\n')
    g.write('M=D\n')
    g.write('@SP\n')
    g.write('M=M+1\n')
    # this
    g.write('@THIS\n')
    g.write('D=M\n')
    g.write('@SP\n')
    g.write('A=M\n')
    g.write('M=D\n')
    g.write('@SP\n')
    g.write('M=M+1\n')
    # that
    g.write('@THAT\n')
    g.write('D=M\n')
    g.write('@SP\n')
    g.write('A=M\n')
    g.write('M=D\n')
    g.write('@SP\n')
    g.write('M=M+1\n')
    # replacing ARG for called f'
    g.write('@5\n')
    g.write('D=A\n')
    g.write('@SP\n')
    g.write('D=M-D\n')
    nargs = int(words[2])
    g.write('@{}\n'.format(nargs))
    g.write('D=D-A\n')
    g.write('@ARG\n')
    g.write('M=D\n')
    # replacing LCL for called f'
    g.write('@SP\n')
    g.write('D=M\n')
    g.write('@LCL\n')
    g.write('M=D\n')

    # goto function now
    g.write('@' + name_of_file.split('\\')[-1].split('.')[0] + '.' + words[1] + '\n')
    g.write('0;JMP\n')
    # return label
    g.write('({}$ret.{})\n'.format(words[1], function_return_index - 1))


for (root,dirs,files) in os.walk('08', topdown=True):
        if len(files)==0:
            continue

        else:
            # Clear the whitescapes and the comments and writes to the intermediate file
            counter=0
            name_of_file=''
            for file in files:
                if file.split('.')[1] == 'vm':
                    counter+=1
                    name_of_file=root+'\\'+file.split('.')[0]+'.asm'
            if counter>1:
                name_of_file=root+'.asm'
            for file in files:
                if file.split('.')[1]!='vm':
                    continue
                else:
                    # Clear the whitescapes and the comments and writes to the intermediate file
                    with open(root+'\\'+file) as f:
                        with open(root+'\\'+"Rwhitespaces.vm", 'w') as g:
                            for line in f:
                                if len(line.split()) == 0:
                                    continue
                                for word in line.split():
                                    if word[0] == '/' and word[1] == '/':
                                        break
                                    g.write(word + ' ')
                                if line.split()[0] != "//":
                                    g.write('\n')


                    # Start Converting to Assembly level language line by line
                    with open(root+'\\'+"Rwhitespaces.vm") as f:
                        with open(name_of_file, 'a') as g:
                            #set SP
                            #call sys.init if multiple files there(sys.vm file there)
                            if counter>1:
                                g.write('@256\n')
                                g.write('D=A\n')
                                g.write('@0\n')
                                g.write('M=D\n')
                                words_temp=['call','Sys.init',0]
                                calling_function(words_temp)
                            for line in f:
                                if len(line.split()) == 0:
                                    continue
                                words = line.split()
                                if (words[0] == 'push' or words[0] == 'pop'):
                                    if (words[1] == 'constant' or words[1] == 'temp'
                                            or words[1] == 'pointer' or words[1] == 'static'):
                                        if (words[1] == 'constant'):
                                            g.write('@{}\n'.format(words[2]))
                                        elif (words[1] == 'temp'):
                                            g.write('@{}\n'.format(str((int(words[2]) + 5))))
                                        elif (words[1] == 'static'):
                                            g.write('@{}.{}\n'.format(file.split('.')[0], words[2]))
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
                                    if (words[0] == 'push'):
                                        if (words[1] == 'constant'):
                                            g.write('D=A\n')
                                        else:
                                            g.write('D=M\n')
                                        g.write('@SP\n')
                                        g.write('A=M\n')
                                        g.write('M=D\n')
                                        g.write('@SP\n')
                                        g.write('M=M+1\n')
                                    elif (words[0] == 'pop'):
                                        g.write('@SP\n')
                                        g.write('AM=M-1\n')
                                        g.write('D=M\n')
                                        g.write('@R13\n')
                                        g.write('A=M\n')
                                        g.write('M=D\n')
                                elif (words[0] == 'neg' or words[0] == 'not' or words[0] == 'add'
                                or words[0] == 'sub' or words[0] == 'and' or words[0] == 'or'
                                or words[0] == 'not' or words[0] == 'gt'
                                or words[0] == 'lt' or words[0] == 'eq'):
                                    if words[0] not in ('neg', 'not'):
                                        g.write('@SP\n')
                                        g.write('AM=M-1\n')
                                        g.write('D=M\n')
                                        g.write('@SP\n')
                                        g.write('AM=M-1\n')
                                    if (words[0] == 'add'):
                                        g.write('M=D+M\n')
                                    elif (words[0] == 'sub'):
                                        g.write('M=M-D\n')
                                    elif (words[0] == 'neg'):
                                        g.write('@SP\n')
                                        g.write('AM=M-1\n')
                                        g.write('M=-M\n')
                                    elif (words[0] == 'and'):
                                        g.write('M=D&M\n')
                                    elif (words[0] == 'or'):
                                        g.write('M=D|M\n')
                                    elif (words[0] == 'not'):
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
                                        label_index += 1
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

                                elif(words[0] == 'label'):
                                    g.write('('+name_of_file.split('\\')[-1].split('.')[0]+'.'+words[1]+')\n')
                                elif(words[0] == 'goto'):
                                    g.write('@'+name_of_file.split('\\')[-1].split('.')[0]+'.'+words[1]+'\n')
                                    g.write('0;JMP\n')
                                elif(words[0] == 'if-goto'):
                                    g.write('@SP\n')
                                    g.write('AM=M-1\n')
                                    g.write('D=M\n')
                                    g.write('@' + name_of_file.split('\\')[-1].split('.')[0]+'.'+words[1] + '\n')
                                    g.write('D;JNE\n')
                                elif(words[0]=='call'):
                                    calling_function(words)
                                elif (words[0] == 'function'):
                                    g.write('('+name_of_file.split('\\')[-1].split('.')[0]+'.'+words[1]+')\n')
                                    for _ in range(int(words[2])):
                                        g.write('@0\n')
                                        g.write('D=A\n')
                                        g.write('@SP\n')
                                        g.write('A=M\n')
                                        g.write('M=D\n')
                                        g.write('@SP\n')
                                        g.write('M=M+1\n')
                                elif(words[0]=='return'):
                                    g.write('@LCL\n')
                                    g.write('D=M\n')
                                    g.write('@endFrame\n')
                                    g.write('M=D\n')
                                    g.write('@5\n')
                                    g.write('D=A\n')
                                    g.write('@endFrame\n')
                                    g.write('D=M-D\n')
                                    g.write('A=D\n')
                                    g.write('D=M\n')
                                    g.write('@retAddr\n')
                                    g.write('M=D\n')
                                    #place the returned value at *args
                                    g.write('@SP\n')
                                    g.write('AM=M-1\n')
                                    g.write('D=M\n')
                                    g.write('@ARG\n')
                                    g.write('A=M\n')
                                    g.write('M=D\n')
                                    #SP just one above reutrned value
                                    g.write('D=A+1\n')
                                    g.write('@SP\n')
                                    g.write('M=D\n')
                                    #reposition that
                                    g.write('@1\n')
                                    g.write('D=A\n')
                                    g.write('@endFrame\n')
                                    g.write('D=M-D\n')
                                    g.write('A=D\n')
                                    g.write('D=M\n')
                                    g.write('@THAT\n')
                                    g.write('M=D\n')
                                    # reposition this
                                    g.write('@2\n')
                                    g.write('D=A\n')
                                    g.write('@endFrame\n')
                                    g.write('D=M-D\n')
                                    g.write('A=D\n')
                                    g.write('D=M\n')
                                    g.write('@THIS\n')
                                    g.write('M=D\n')
                                    # reposition arg
                                    g.write('@3\n')
                                    g.write('D=A\n')
                                    g.write('@endFrame\n')
                                    g.write('D=M-D\n')
                                    g.write('A=D\n')
                                    g.write('D=M\n')
                                    g.write('@ARG\n')
                                    g.write('M=D\n')
                                    # reposition lcl
                                    g.write('@4\n')
                                    g.write('D=A\n')
                                    g.write('@endFrame\n')
                                    g.write('D=M-D\n')
                                    g.write('A=D\n')
                                    g.write('D=M\n')
                                    g.write('@LCL\n')
                                    g.write('M=D\n')
                                    #goto return address
                                    g.write('@retAddr\n')
                                    g.write('A=M\n')
                                    g.write('0;JMP\n')
























