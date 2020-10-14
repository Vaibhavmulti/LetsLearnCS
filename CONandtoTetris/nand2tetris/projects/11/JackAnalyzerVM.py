import sys
import os
import re
"""
Gets a file/ directory from the command line argument and generates VM file for the corresponding 
jack file(s) by first passing the jack file to Tokenizer(class) which generates the tokens 
which are then passed to CompilationEngine(class)
which finally generates the Vm code according to the recursive method calls with the help of
Symbol Table(for variables) and VMWriter which does the actual writing. 
"""


# Breaks the HighLevelLanguage into tokens providing input to the parser.
class Tokenizer:
    """opens the file for tokenizing.
       removes whitespaces,comments and flats the file for individual tokens"""

    def __init__(self, jack_file):
        # flat list of file => jack
        self.jack = []
        self.current_token = ''
        self.cur_token_type = ''
        self.KEYWORDS = ['class', 'constructor', 'function', 'method', 'field'
            , 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false'
            , 'null', 'let', 'do', 'this', 'while', 'return', 'if', 'else']

        self.SYMBOLS = ['{', '}', '(', ')', '[', ']', ',', ';', '+',
                        '-', '*', '/', '<', '>', '=', '.', '&', '|', '~']
        multiline_comment = 0
        with open(jack_file) as f:
            with open('temp.jack', 'w') as g:
                for lines in f:
                    if len(lines.split()) == 0:  # skip empty lines
                        continue
                    printed_thisline = 0
                    for word in lines.split():
                        if len(word) >= 2 and word[0] == '/' and word[1] == '/':
                            break
                        if len(word) >= 2 and word[0] == '/' and word[1] == '*':
                            multiline_comment = 1
                            continue
                        if len(word) >= 2 and word[-2] == '*' and word[-1] == '/':
                            multiline_comment = 0
                            continue
                        if multiline_comment == 0:
                            g.write(word + ' ')
                            printed_thisline = 1
                    if printed_thisline == 1:
                        g.write('\n')  # print newline only when something is printed
        # flatten the processed temp(no whitespaces/comments) file now
        with open('temp.jack') as f:
            for lines in f:
                for word in lines.split():
                    self.jack.append(word)
        os.remove('temp.jack')

    # are there more tokens left?
    def hasMoreTokens(self):
        return True if len(self.jack) != 0 else False

    # processes the next token
    def advance(self):
        try_token = self.jack[0]
        pattern_words = re.compile("^[a-zA-Z_][a-zA-Z0-9_]*")
        pattern_digits = re.compile("[0-9]+")
        # if found match (entire string matches pattern)
        if pattern_words.fullmatch(try_token) is not None:
            self.current_token = try_token
            if try_token in self.KEYWORDS:
                self.cur_token_type = 'KEYWORD'
            else:
                self.cur_token_type = 'IDENTIFIER'
            self.jack.pop(0)
        elif pattern_digits.fullmatch(try_token) is not None:
            self.current_token = try_token
            self.cur_token_type = 'INT_CONST'
            self.jack.pop(0)
        else:  # symbol remains or combination of words/letters and symbols
            if len(try_token) == 1 and try_token[0] in self.SYMBOLS:
                self.current_token = try_token
                self.cur_token_type = 'SYMBOL'
                self.jack.pop(0)
            else:
                words_numbers_wrapped = ''
                recur_call = 0
                for w in try_token:
                    if w in self.SYMBOLS and words_numbers_wrapped != '':
                        self.jack[0] = self.jack[0].replace(words_numbers_wrapped, '', 1)
                        self.jack.insert(0, words_numbers_wrapped)
                        recur_call = 1
                        break
                    elif w in self.SYMBOLS and words_numbers_wrapped == '':
                        self.jack[0] = self.jack[0].replace(w, '', 1)
                        self.jack.insert(0, w)
                        recur_call = 1
                        break
                    elif w != '"':
                        words_numbers_wrapped += w
                        continue
                    else:  # begin string constant
                        tp_str = ''
                        ans_str = ''
                        try_allfront = try_token[1:]
                        while tp_str != '"':
                            cur_str = ''
                            for ww in try_allfront:
                                if ww != '"':
                                    ans_str += ww
                                    cur_str += ww
                                elif ww == '"':
                                    cur_str += '"'
                                    tp_str='"'
                                    self.jack[0] = self.jack[0].replace(cur_str, '')
                                    self.current_token=ans_str
                                    self.cur_token_type='STRING_CONST'
                            if tp_str!='"':
                                self.jack.pop(0)
                                try_allfront=self.jack[0]
                                ans_str+=' '
                if recur_call == 1:
                    self.advance()

    def tokenType(self):
        return self.cur_token_type

    # Following method return the token value of respective token types
    def tokenValue(self):
        return self.current_token



"""Creates two symbol tables one for class fields and one for the current subroutine"""


class SymbolTable:
    def __init__(self):     # Initialize symbol tables
        self.class_st = {}
        self.subroutine_st = {}
        self.static, self.field, self.arg, self.var = (0, 0, 0, 0)

    def start_subroutine(self):  # Clears the subroutine symbol table
        self.subroutine_st.clear()
        self.arg, self.var = (0, 0)

    def define(self, name, typ, kind):  # Adds a tuple of type, kind, number to the table
        if kind == 'STATIC':
            self.class_st[name] = (typ, kind, self.static)
            self.static += 1
        elif kind == 'FIELD':
            self.class_st[name] = (typ, kind, self.field)
            self.field += 1
        elif kind == 'VAR':
            self.subroutine_st[name] = (typ, kind, self.var)
            self.var += 1
        elif kind == 'ARG':
            self.subroutine_st[name] = (typ, kind, self.arg)
            self.arg += 1

    def var_count(self, kind):
        if kind == 'STATIC':
            return self.static
        elif kind == 'FIELD':
            return self.field
        elif kind == 'ARG':
            return self.arg
        else:
            return self.var

    def kind_of(self, name):
        return self.subroutine_st.get(name)[1] if self.subroutine_st.get(name) is not None \
            else self.class_st.get(name)[1]

    def type_of(self, name):
        return self.subroutine_st.get(name)[0] if self.subroutine_st.get(name) is not None \
            else self.class_st.get(name)[0]

    def index_of(self, name):
        return self.subroutine_st.get(name)[2] if self.subroutine_st.get(name) is not None \
            else self.class_st.get(name)[2]



"""Writes suitable VM commands to the output file"""


class VMWriter:
    def __init__(self, file_name):
        self.vm = open(file_name, "w")

    def write_push(self, segment, index):       # seg:{local,arg,this,static..} index:int
        self.vm.write('push ' + str(segment) + ' ' + str(index) + '\n')

    def write_pop(self, segment, index):
        self.vm.write('pop ' + str(segment) + ' ' + str(index) + '\n')

    def write_arithmetic(self, command):
        self.vm.write(str(command) + '\n')

    def write_label(self, label):
        self.vm.write('label ' + label + '\n')

    def write_goto(self, label):
        self.vm.write('goto ' + label + '\n')

    def write_if(self, label):
        self.vm.write('if-goto ' + label + '\n')

    def write_call(self, name, nargs):  # nargs : number of args pushed on top of the stack
        self.vm.write('call ' + name + ' ' + str(nargs) + '\n')

    def write_function(self, name, num_local):  # num_local : number of local var in function
        self.vm.write('function ' + name + ' ' + str(num_local) + '\n')

    def write_return(self):
        self.vm.write('return' + '\n')

    def close(self):
        self.vm.close()



"""Takes input from tokenizer and writes output in XML file format
    according to the method calls(statements in the class)"""


class CompilationEngine:

    def __init__(self, tokens,file_name):
        self.tokens = tokens  # Tokenizer object
        self.file_name = file_name
        self.return_type = ''
        self.function_type = ''
        self.while_counter = 0
        self.if_counter = 0
        self.methods = {}
        self.symbol_table = SymbolTable()
        self.vm_writer = VMWriter(file_name + '.vm')
        self.compile_class()

    def compile_class(self):
        print_depth = 1
        self.tokens.advance() if self.tokens.hasMoreTokens() else print("No more tokens")
        self.tokens.advance()  # advances the keyword 'class'
        self.tokens.advance()  # advances the class name
        self.tokens.advance()  # advances the symbol {
        while self.tokens.tokenType() == 'KEYWORD' and self.tokens.tokenValue() in ('static', 'field'):
            self.compile_classvardec(print_depth+1)
            # self.tokens.advance()
        while self.tokens.tokenType() == 'KEYWORD' and self.tokens.tokenValue() in ('constructor', 'function', 'method'):
            self.compile_subroutineDec(print_depth + 1)

    def compile_classvardec(self, print_depth):
        class_var_kind = self.tokens.tokenValue()
        self.tokens.advance()  # advances the class var kind (static, field)
        class_var_type = self.tokens.tokenValue()
        self.tokens.advance()  # advances the class var type
        class_var_name = self.tokens.tokenValue()
        self.tokens.advance()  # advances the class var name
        if class_var_kind == 'static':
            self.symbol_table.define(class_var_name, class_var_type, 'STATIC')  # filling the symbol table
        else:
            self.symbol_table.define(class_var_name, class_var_type, 'FIELD')  # filling the symbol table
            if class_var_type not in ('int', 'char', 'boolean'):
                self.methods[class_var_name] = class_var_type
        while self.tokens.tokenValue() == ',':
            self.tokens.advance()  # advances the symbol ','
            class_var_name = self.tokens.tokenValue()
            self.tokens.advance()  # advances the class var name
            if class_var_kind == 'static':
                self.symbol_table.define(class_var_name, class_var_type, 'STATIC')  # filling the symbol table
            else:
                self.symbol_table.define(class_var_name, class_var_type, 'FIELD')  # filling the symbol table
                if class_var_type not in ('int', 'char', 'boolean'):
                    self.methods[class_var_name] = class_var_type
        self.tokens.advance()  # advances the symbol ';'


    def compile_subroutineDec(self, print_depth):
        self.symbol_table.start_subroutine()
        self.function_type = self.tokens.tokenValue()
        self.tokens.advance()  # advanced from the type of function (constructor,method,function)
        self.return_type = self.tokens.tokenValue()
        self.tokens.advance()  # advances the return type
        function_name = self.file_name + '.' + self.tokens.tokenValue()
        self.tokens.advance()  # advances the function name
        if self.function_type == 'method':
            self.symbol_table.define('this', self.file_name, 'ARG')  # first argument is always the object
        self.tokens.advance()  # advances symbol '('
        self.compile_parameterList(print_depth+1)
        self.tokens.advance()  # advances symbol ')'
        self.compile_subroutineBody(print_depth + 1, function_name, self.function_type)

    def symboltable_local_ARG(self):  # fills arg variable in the subroutine symbol table
        var_type = self.tokens.tokenValue()
        self.tokens.advance()  # advances the type of the var
        var_name = self.tokens.tokenValue()
        self.tokens.advance()  # advances the var name
        self.symbol_table.define(var_name, var_type, 'ARG')  # filling the symbol table
        if var_type not in ('int', 'char', 'boolean'):
            self.methods[var_name] = var_type



    def compile_parameterList(self, print_depth):
        while self.tokens.tokenValue() != ')':
            self.symboltable_local_ARG()
            while self.tokens.tokenValue() == ',':
                self.tokens.advance()  # advances the symbol ','
                self.symboltable_local_ARG()

    def compile_subroutineBody(self, print_depth, function_name, function_type):
        self.tokens.advance()  # advances the symbol {
        while self.tokens.tokenValue() == 'var':
            self.compile_varDec(print_depth+1)
        self.vm_writer.write_function(function_name, self.symbol_table.var_count('VAR'))
        if function_type == 'method':
            self.vm_writer.write_push('argument', '0')
            self.vm_writer.write_pop('pointer', '0')
        elif function_type == 'constructor':
            self.vm_writer.write_push('constant', self.symbol_table.var_count('FIELD'))
            self.vm_writer.write_call('Memory.alloc', '1')
            self.vm_writer.write_pop('pointer', '0')

        self.compile_statements(print_depth+1)
        self.tokens.advance()  # advances the symbol }

    def compile_varDec(self, print_depth):
        self.tokens.advance()  # advances the keyword var
        var_type = self.tokens.tokenValue()
        self.tokens.advance()  # advances the type of the variable
        var_name = self.tokens.tokenValue()
        self.tokens.advance()  # advances the var name
        self.symbol_table.define(var_name, var_type, 'VAR')  # filling the symbol table
        if var_type not in ('int', 'char', 'boolean'):
            self.methods[var_name] = var_type

        while self.tokens.tokenValue() == ',':
            self.tokens.advance()  # advances the symbol ,
            var_name = self.tokens.tokenValue()
            self.tokens.advance()  # advances the var name
            self.symbol_table.define(var_name, var_type, 'VAR')  # filling the symbol table
            if var_type not in ('int', 'char', 'boolean'):
                self.methods[var_name] = var_type
        self.tokens.advance()  # advances the symbol ;

    def compile_statements(self, print_depth):
        while self.tokens.tokenValue() in ('let', 'if', 'while', 'do', 'return'):
            if self.tokens.tokenValue() == 'let':
                self.compile_letstatement(print_depth+1)
            elif self.tokens.tokenValue() == 'if':
                self.compile_ifstatement(print_depth+1)
            elif self.tokens.tokenValue() == 'while':
                self.compile_whilestatement(print_depth + 1)
            elif self.tokens.tokenValue() == 'do':
                self.compile_dostatement(print_depth + 1)
            elif self.tokens.tokenValue() == 'return':
                self.compile_returnstatement(print_depth + 1)

    def compile_letstatement(self, print_depth):
        self.tokens.advance()  # advances the keyword let
        var_name = self.tokens.tokenValue()
        array_flag = 0
        self.tokens.advance()  # advances the variable name
        if self.tokens.tokenValue() == '[':
            array_flag = 1
            self.tokens.advance()  # advances the symbol '['
            self.compile_expression(print_depth+1)
            self.push_var(var_name)
            self.tokens.advance()  # advances the symbol ']'
            self.vm_writer.write_arithmetic('add')
        self.tokens.advance()  # advances the symbol '='
        self.compile_expression(print_depth + 1)
        if array_flag == 1:
            self.vm_writer.write_pop('temp', '0')
            self.vm_writer.write_pop('pointer', '1')
            self.vm_writer.write_push('temp', '0')
            self.vm_writer.write_pop('that', '0')
        else:
            if self.symbol_table.kind_of(var_name) == 'VAR':
                self.vm_writer.write_pop('local', self.symbol_table.index_of(var_name))
            elif self.symbol_table.kind_of(var_name) == 'ARG':
                self.vm_writer.write_pop('argument', self.symbol_table.index_of(var_name))
            elif self.symbol_table.kind_of(var_name) == 'STATIC':
                self.vm_writer.write_pop('static', self.symbol_table.index_of(var_name))
            else:
                self.vm_writer.write_pop('this', self.symbol_table.index_of(var_name))
        self.tokens.advance()  # advances the symbol ';'

    def compile_ifstatement(self, print_depth):
        self.tokens.advance()  # advances the keyword 'if'
        self.tokens.advance()  # advances the symbol '('
        self.compile_expression(print_depth + 1)
        num_if = self.if_counter
        self.if_counter += 1
        self.vm_writer.write_if(self.file_name + 'if_true' + str(num_if))
        self.vm_writer.write_goto(self.file_name + 'if_false' + str(num_if))
        self.tokens.advance()  # advances the symbol ')'
        self.tokens.advance()  # advances the symbol '{'
        self.vm_writer.write_label(self.file_name + 'if_true' + str(num_if))
        self.compile_statements(print_depth+1)
        self.vm_writer.write_goto(self.file_name + 'if_end' + str(num_if))
        self.tokens.advance()  # advances the symbol '}'
        self.vm_writer.write_label(self.file_name + 'if_false' + str(num_if))
        if self.tokens.tokenValue() == 'else':
            self.tokens.advance()  # advances the keyword 'else'
            self.tokens.advance()  # advances the symbol '{'
            self.compile_statements(print_depth + 1)
            self.tokens.advance()  # advances the symbol '}'
        self.vm_writer.write_label(self.file_name + 'if_end' + str(num_if))

    def compile_whilestatement(self, print_depth):
        self.tokens.advance()  # advances keyword 'while'
        self.tokens.advance()  # advances symbol '('
        num_while = self.while_counter
        self.vm_writer.write_label(self.file_name + '_while_start' + str(num_while))
        self.while_counter += 1
        self.compile_expression(print_depth + 1)
        self.vm_writer.write_arithmetic('not')
        self.vm_writer.write_if(self.file_name + '_while_end' + str(num_while))
        self.tokens.advance()  # advances the symbol ')'
        self.tokens.advance()  # advances the symbol '{'
        self.compile_statements(print_depth + 1)
        self.vm_writer.write_goto(self.file_name + '_while_start' + str(num_while))
        self.tokens.advance()  # advances the symbol '}'
        self.vm_writer.write_label(self.file_name + '_while_end' + str(num_while))

    def compile_dostatement(self, print_depth):
        self.tokens.advance()  # advances the keyword 'do'
        self.compile_subroutineCall(print_depth + 1, 0, '')
        self.vm_writer.write_pop('temp', 0)
        self.tokens.advance()  # advances the symbol ;

    def compile_returnstatement(self, print_depth):
        self.tokens.advance()  # advances the keyword 'return'
        if self.tokens.tokenValue() != ';':
            self.compile_expression(print_depth + 1)
        if self.return_type == 'void':
            self.vm_writer.write_push('constant', '0')
        #if self.function_type == 'constructor':
            #self.vm_writer.write_push('pointer', '0')
        self.vm_writer.write_return()
        self.tokens.advance()  # advances the symbol ;

    def compile_expression(self, print_depth):
        self.compile_term(print_depth + 1)
        while self.tokens.tokenValue() in ('+', '-', '*', '/', '&', '|', '<' , '>', '='):
            operation = self.tokens.tokenValue()
            self.tokens.advance()  # advances the symbol ('+', '-', '*', '/', '&', '|', '<' , '>', '=')
            self.compile_term(print_depth + 1)
            if operation == '+':
                self.vm_writer.write_arithmetic('add')
            elif operation == '-':
                self.vm_writer.write_arithmetic('sub')
            elif operation == '&':
                self.vm_writer.write_arithmetic('and')
            elif operation == '|':
                self.vm_writer.write_arithmetic('or')
            elif operation == '<':
                self.vm_writer.write_arithmetic('lt')
            elif operation == '>':
                self.vm_writer.write_arithmetic('gt')
            elif operation == '=':
                self.vm_writer.write_arithmetic('eq')
            elif operation == '*':
                self.vm_writer.write_call('Math.multiply', 2)
            elif operation == '/':
                self.vm_writer.write_call('Math.divide', 2)

    def compile_subroutineCall(self, print_depth, skip, var_name):
        function_name = ''
        vr_name = var_name
        flag_method_call = 0
        plain_method_call = 0
        if skip == 0:
            function_name += self.tokens.tokenValue()
            vr_name = self.tokens.tokenValue()
            self.tokens.advance()  # advances the variable name
        if self.tokens.tokenValue() == '.':
            self.tokens.advance()  # advances the symbol '.'
            function_name += var_name + '.' + self.tokens.tokenValue()
            if self.methods.get(vr_name) is not None:
                self.push_var(vr_name)
                flag_method_call = 1
            self.tokens.advance()  # advances the function_name
        else:
            plain_method_call = 1
        self.tokens.advance()  # advances the symbol (
        if plain_method_call == 1:
            self.vm_writer.write_push('pointer', '0')
        nargs = 0
        if self.tokens.tokenValue() != ')':
            nargs = self.compile_expressionList(print_depth + 1)
        self.tokens.advance()  # advances the symbol )
        if flag_method_call == 1:
            self.vm_writer.write_call(self.methods.get(vr_name) + '.' + function_name.split('.')[1], nargs + 1)
        elif plain_method_call == 1:
            self.vm_writer.write_call(self.file_name + '.' + function_name, nargs + 1)
        else:
            self.vm_writer.write_call(function_name, nargs)

    def compile_expressionList(self, print_depth):
        nargs = 1
        self.compile_expression(print_depth + 1)
        while self.tokens.tokenValue() == ',':
            self.tokens.advance()  # advances the symbol ','
            nargs += 1
            self.compile_expression(print_depth + 1)
        return nargs

    def compile_term(self, print_depth):
        if self.tokens.tokenValue() in ('-', '~'):
            unary_operator = self.tokens.tokenValue()
            self.tokens.advance()  # advances the symbol '-' or '~'
            self.compile_term(print_depth + 1)
            if unary_operator == '-':
                self.vm_writer.write_arithmetic('neg')
            else:
                self.vm_writer.write_arithmetic('not')

        elif self.tokens.tokenValue() == '(':
            self.tokens.advance()  # advances the symbol (
            self.compile_expression(print_depth + 1)
            self.tokens.advance()  # advances the symbol )
        else:
            if self.tokens.tokenType() == 'INT_CONST':
                self.vm_writer.write_push('constant', self.tokens.tokenValue())
                self.tokens.advance()  # advances the integer constant
            elif self.tokens.tokenType() == 'STRING_CONST':
                string = str(self.tokens.tokenValue())
                self.vm_writer.write_push('constant', str(len(string)))
                self.vm_writer.write_call('String.new', '1')
                for s in string:
                    self.vm_writer.write_push('constant', str(ord(s)))
                    self.vm_writer.write_call('String.appendChar', '2')
                self.tokens.advance()  # advances the string constant
            elif self.tokens.tokenValue() in ('true', 'false', 'null', 'this'):
                if self.tokens.tokenValue() == 'true':
                    self.vm_writer.write_push('constant', '0')
                    self.vm_writer.write_arithmetic('not')
                elif self.tokens.tokenValue() in ('false', 'null'):
                    self.vm_writer.write_push('constant', '0')
                elif self.tokens.tokenValue() == 'this':
                    self.vm_writer.write_push('pointer', '0')
                self.tokens.advance()
            else:
                var_name = self.tokens.tokenValue()
                self.tokens.advance()  # advances the variable name
                if self.tokens.tokenValue() == '[':
                    self.tokens.advance()  # advances the symbol '['
                    self.compile_expression(print_depth + 1)
                    self.push_var(var_name)
                    self.vm_writer.write_arithmetic('add')
                    self.vm_writer.write_pop('pointer', '1')
                    self.vm_writer.write_push('that', '0')
                    self.tokens.advance()  # advances the symbol ']'
                elif self.tokens.tokenValue() in ('(' , '.'):
                    self.compile_subroutineCall(print_depth, 1, var_name)
                else:
                    self.push_var(var_name)

    def push_var(self, var_name):
        if self.symbol_table.kind_of(var_name) == 'VAR':
            self.vm_writer.write_push('local', self.symbol_table.index_of(var_name))
        elif self.symbol_table.kind_of(var_name) == 'ARG':
            self.vm_writer.write_push('argument', self.symbol_table.index_of(var_name))
        elif self.symbol_table.kind_of(var_name) == 'STATIC':
            self.vm_writer.write_push('static', self.symbol_table.index_of(var_name))
        else:
            self.vm_writer.write_push('this', self.symbol_table.index_of(var_name))


for (root, dirs, files) in os.walk(sys.argv[1], topdown=True):
    for file in files:
        if file.split('.')[1] == 'jack':
            #print(root+'\\'+file)
            token = Tokenizer(root+'\\'+file)
            parser = CompilationEngine(token, file.split('.')[0])

