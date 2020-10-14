#Clear the whitescapes and the comments and writes to the file target file .hack
with open("Pong.asm") as f:
    with open("Add_Rwhitespaces.hack",'w') as g:
        for line in f:
            if len(line.split())==0:
                continue
            for word in line.split():
                if word[0]=='/' and word[1]=='/':
                    break
                g.write(word)
            if line.split()[0]!="//":
                g.write('\n')

#let's initialise the symbol table with predefined values name->address
symbol_table={
"R0":0,"R1":1,"R2":2,"R3":3,"R4":4,"R5":5,"R6":6,"R7":7,"R8":8,"R9":9,"R10":10,
"R11":11,"R12":12,"R13":13,"R14":14,"R15":15,"SCREEN":16384,"KBD":24576,
"SP":0,"LCL":1,"ARG":2,"THIS":3,"THAT":4}

#let's do one pass for labels  (label) for forward reference i.e
#label is referenced before declaring

with open("Add_Rwhitespaces.hack") as f:
    with open("Add_Rlabels.hack",'w') as g:
        index=0
        for line in f:
            if line[0]=='(':
                label_name=""
                for w in line[1:]:
                    if w==')':
                        break
                    label_name+=w
                symbol_table[label_name]=index
                continue
            else:
                g.write(line)
            index+=1

print(symbol_table)
#final pass let's generate binary code
#let's encode destination,computation,jump bits in a dict first
comp_dict={
    '0':'0101010','1':'0111111','-1':'0111010','D':'0001100','A':'0110000','M':'1110000',
    '!D':'0001101','!A':'0110001','!M':'1110001','-D':'0001111','-A':'0110011','-M':'1110011',
    'D+1':'0011111','A+1':'0110111','M+1':'1110111','D-1':'0001110','A-1':'0110010',
    'M-1':'1110010','D+A':'0000010','D+M':'1000010','D-A':'0010011','D-M':'1010011',
    'A-D':'0000111','M-D':'1000111','D&A':'0000000','D&M':'1000000','D|A':'0010101',
    'D|M':'1010101'}
dest_dict={
    'NULL':'000','M':'001','D':'010','A':'100','MD':'011','AM':'101',
    'AD':'110','AMD':'111'}
jmp_dict={
    'NULL':'000','JGT':'001','JEQ':'010','JGE':'011','JLT':'100',
    'JNE':'101','JLE':'110','JMP':'111'}
index=16  #first availabe memory place for storing variables

with open("Add_Rlabels.hack") as f:
    with open("Add.hack",'w') as g:
        for line in f:
            for word in line.split():
                if word[0]=='@':        #A instruction
                    if str.isdigit(word[1]):
                        number=int(word[1:])
                    else:
                        name=word.split('@')[1]
                        if name in symbol_table:
                            number=symbol_table[name]
                        else:
                            symbol_table[name]=index
                            number=index
                            index+=1
                    g.write(str(format(number,'016b')))
                    g.write('\n')
                else:                       #C instruction
                    # seperate the dest | comp | jmp
                    if '=' in word and ';' in word:
                        dest = word.split('=')[0]
                        comp = word.split('=')[1].split(';')[0]
                        jmp = word.split('=')[1].split(';')[1]
                    elif ';' in word and '=' not in word:
                        dest = 'NULL'
                        comp = word.split(';')[0]
                        jmp = word.split(';')[1]
                    elif '=' in word and ';' not in word:
                        jmp = 'NULL'
                        dest = word.split('=')[0]
                        comp = word.split('=')[1]
                    else:
                        comp = word
                        jmp = 'NULL'
                        dest = 'NULL'

                    out_inst='111'         #C starts with 3 111 first 1 op code rest 2 1's are not used
                    out_inst+=comp_dict[comp]
                    out_inst += dest_dict[dest]
                    out_inst += jmp_dict[jmp]
                    g.write(out_inst)
                    g.write('\n')
