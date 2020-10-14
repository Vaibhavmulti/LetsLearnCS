"""Takes input from tokenizer and writes output in XML file format
    according to the method calls(statements in the class)"""

from Compiler.SymbolTable import SymbolTable
from Compiler.VMWriter import VMWriter
from Compiler.Tokenizer import Tokenizer
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


tokens = Tokenizer('Main.jack')
parser = CompilationEngine(tokens, 'Main')