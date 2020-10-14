"""Takes input from tokenizer and writes output in XML file format
    according to the method calls(statements in the class)"""


class CompilationEngine:

    def __init__(self, tokens,file_name):
        self.tokens = tokens  # Tokenizer object
        self.xml = open(file_name, "w")
        self.compile_class()

    def __del__(self):
        self.xml.close()  # Closing the file

    def compile_class(self):
        print_depth = 1
        self.xml.write(' ' * (print_depth - 1) * 2 + '<class>\n')
        self.tokens.advance() if self.tokens.hasMoreTokens() else print("No more tokens")
        if self.tokens.tokenType() == 'KEYWORD' and self.tokens.tokenValue() == 'class':
            self.xml.write(' ' * print_depth * 2 + '<keyword> class </keyword>\n')
        self.tokens.advance()
        if self.tokens.tokenType() == 'IDENTIFIER':
            self.xml.write(' ' * print_depth * 2 + '<identifier> ' + str(self.tokens.tokenValue())+' </identifier>\n')
        self.tokens.advance()
        if self.tokens.tokenType() == 'SYMBOL' and self.tokens.tokenValue() == '{':
            self.xml.write(' ' * print_depth * 2 + '<symbol> { </symbol>\n')
        self.tokens.advance()
        while self.tokens.tokenType() == 'KEYWORD' and self.tokens.tokenValue() in ('static', 'field'):
            self.compile_classvardec(print_depth+1)
            self.tokens.advance()
        while self.tokens.tokenType() == 'KEYWORD' and self.tokens.tokenValue() in ('constructor', 'function', 'method'):
            self.compile_subroutineDec(print_depth + 1)
            self.tokens.advance()
        self.xml.write(' ' * print_depth * 2 + '<symbol> } </symbol>\n')
        self.xml.write(' ' * (print_depth - 1) * 2 + '</class>\n')

    def type(self, print_depth):
        self.xml.write(' ' * print_depth * 2 + '<' + str(self.tokens.tokenType()).lower() +
                       '> ' + self.tokens.tokenValue() + ' </' + str(self.tokens.tokenType()).lower() + '>\n')
        self.tokens.advance()

    def varName(self, print_depth):
        self.xml.write(' ' * print_depth * 2 + '<identifier> ' + self.tokens.tokenValue() + ' </identifier>\n')
        self.tokens.advance()

    def compile_classvardec(self, print_depth):
        print(print_depth)

    def compile_subroutineDec(self, print_depth):
        self.xml.write(' ' * (print_depth - 1) * 2 + '<subroutineDec>\n')
        self.xml.write(' ' * print_depth * 2 + '<keyword> ' + self.tokens.tokenValue() + ' </keyword>\n')
        self.tokens.advance()
        self.type(print_depth)
        self.varName(print_depth)
        self.xml.write(' ' * print_depth * 2 + '<symbol> ( </symbol>\n')
        self.tokens.advance()

        self.compile_parameterList(print_depth+1)
        self.xml.write(' ' * print_depth * 2 + '<symbol> ) </symbol>\n')
        self.tokens.advance()

        self.compile_subroutineBody(print_depth + 1)
        self.xml.write(' ' * (print_depth - 1) * 2 + '</subroutineDec>\n')

    def compile_parameterList(self, print_depth):
        self.xml.write(' ' * (print_depth - 1) * 2 + '<parameterList>\n')
        while self.tokens.tokenValue() != ')':
            self.type(print_depth)
            self.varName(print_depth)
            while self.tokens.tokenValue() == ',':
                self.xml.write(' ' * print_depth * 2 + '<symbol> , </symbol>\n')
                self.tokens.advance()
                self.type(print_depth)
                self.varName(print_depth)
        self.xml.write(' ' * (print_depth - 1) * 2 + '</parameterList>\n')

    def compile_subroutineBody(self, print_depth):
        self.xml.write(' ' * (print_depth - 1) * 2 + '<subroutineBody>\n')
        self.xml.write(' ' * print_depth * 2 + '<symbol> { </symbol>\n')
        self.tokens.advance()
        while self.tokens.tokenValue() == 'var':
            self.compile_varDec(print_depth+1)
        self.compile_statements(print_depth+1)
        self.xml.write(' ' * print_depth * 2 + '<symbol> } </symbol>\n')
        self.tokens.advance()
        self.xml.write(' ' * (print_depth - 1) * 2 + '</subroutineBody>\n')

    def compile_varDec(self, print_depth):
        self.xml.write(' ' * (print_depth - 1) * 2 + '<varDec>\n')
        self.xml.write(' ' * print_depth * 2 + '<keyword> var </keyword>\n')
        self.tokens.advance()
        self.type(print_depth)
        self.varName(print_depth)
        while self.tokens.tokenValue() == ',':
            self.xml.write(' ' * print_depth * 2 + '<symbol> , </symbol>\n')
            self.tokens.advance()
            self.varName(print_depth)
        self.xml.write(' ' * print_depth * 2 + '<symbol> ; </symbol>\n')
        self.tokens.advance()
        self.xml.write(' ' * (print_depth - 1) * 2 + '</varDec>\n')

    def compile_statements(self, print_depth):
        self.xml.write(' ' * (print_depth - 1) * 2 + '<statements>\n')
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

        self.xml.write(' ' * (print_depth - 1) * 2 + '</statements>\n')

    def compile_letstatement(self, print_depth):
        self.xml.write(' ' * (print_depth - 1) * 2 + '<letStatement>\n')
        self.xml.write(' ' * print_depth * 2 + '<keyword> let </keyword>\n')
        self.tokens.advance()
        self.varName(print_depth)
        if self.tokens.tokenValue() == '[':
            self.xml.write(' ' * print_depth * 2 + '<symbol> [ </symbol>\n')
            self.tokens.advance()
            self.compile_expression(print_depth+1)
            self.xml.write(' ' * print_depth * 2 + '<symbol> ] </symbol>\n')
            self.tokens.advance()
        self.xml.write(' ' * print_depth * 2 + '<symbol> = </symbol>\n')
        self.tokens.advance()
        self.compile_expression(print_depth + 1)
        self.xml.write(' ' * print_depth * 2 + '<symbol> ; </symbol>\n')
        self.tokens.advance()
        self.xml.write(' ' * (print_depth - 1) * 2 + '</letStatement>\n')

    def compile_ifstatement(self, print_depth):
        self.xml.write(' ' * (print_depth - 1) * 2 + '<ifStatement>\n')
        self.xml.write(' ' * print_depth * 2 + '<keyword> if </keyword>\n')
        self.tokens.advance()
        self.xml.write(' ' * print_depth * 2 + '<symbol> ( </symbol>\n')
        self.tokens.advance()
        self.compile_expression(print_depth + 1)
        self.xml.write(' ' * print_depth * 2 + '<symbol> ) </symbol>\n')
        self.tokens.advance()
        self.xml.write(' ' * print_depth * 2 + '<symbol> { </symbol>\n')
        self.tokens.advance()
        self.compile_statements(print_depth+1)
        self.xml.write(' ' * print_depth * 2 + '<symbol> } </symbol>\n')
        self.tokens.advance()
        if self.tokens.tokenValue() == 'else':
            self.xml.write(' ' * print_depth * 2 + '<keyword> else </keyword>\n')
            self.tokens.advance()
            self.xml.write(' ' * print_depth * 2 + '<symbol> { </symbol>\n')
            self.tokens.advance()
            self.compile_statements(print_depth + 1)
            self.xml.write(' ' * print_depth * 2 + '<symbol> } </symbol>\n')
            self.tokens.advance()
        self.xml.write(' ' * (print_depth - 1) * 2 + '</ifStatement>\n')

    def compile_whilestatement(self, print_depth):
        self.xml.write(' ' * (print_depth - 1) * 2 + '<whileStatement>\n')
        self.xml.write(' ' * print_depth * 2 + '<keyword> while </keyword>\n')
        self.tokens.advance()
        self.xml.write(' ' * print_depth * 2 + '<symbol> ( </symbol>\n')
        self.tokens.advance()
        self.compile_expression(print_depth + 1)
        self.xml.write(' ' * print_depth * 2 + '<symbol> ) </symbol>\n')
        self.tokens.advance()
        self.xml.write(' ' * print_depth * 2 + '<symbol> { </symbol>\n')
        self.tokens.advance()
        self.compile_statements(print_depth + 1)
        self.xml.write(' ' * print_depth * 2 + '<symbol> } </symbol>\n')
        self.tokens.advance()
        self.xml.write(' ' * (print_depth - 1) * 2 + '</whileStatement>\n')

    def compile_dostatement(self, print_depth):
        self.xml.write(' ' * (print_depth - 1) * 2 + '<doStatement>\n')
        self.xml.write(' ' * print_depth * 2 + '<keyword> do </keyword>\n')
        self.tokens.advance()
        self.compile_subroutineCall(print_depth + 1, 0)
        self.xml.write(' ' * print_depth * 2 + '<symbol> ; </symbol>\n')
        self.tokens.advance()
        self.xml.write(' ' * (print_depth - 1) * 2 + '</doStatement>\n')

    def compile_returnstatement(self, print_depth):
        self.xml.write(' ' * (print_depth - 1) * 2 + '<returnStatement>\n')
        self.xml.write(' ' * print_depth * 2 + '<keyword> return </keyword>\n')
        self.tokens.advance()
        if self.tokens.tokenValue() != ';':
            self.compile_expression(print_depth + 1)
        self.xml.write(' ' * print_depth * 2 + '<symbol> ; </symbol>\n')
        self.xml.write(' ' * (print_depth - 1) * 2 + '</returnStatement>\n')

    def compile_expression(self, print_depth):
        self.xml.write(' ' * (print_depth - 1) * 2 + '<expression>\n')
        self.compile_term(print_depth + 1)
        while self.tokens.tokenValue() in ('+', '-', '*', '/', '&', '|', '<' , '>', '='):
            if self.tokens.tokenValue() == '<':
                self.xml.write(' ' * print_depth * 2 + '<symbol> &lt; </symbol>\n')
            elif self.tokens.tokenValue() == '>':
                self.xml.write(' ' * print_depth * 2 + '<symbol> &gt; </symbol>\n')
            elif self.tokens.tokenValue() == '&':
                self.xml.write(' ' * print_depth * 2 + '<symbol> &amp; </symbol>\n')
            else:
                self.xml.write(' ' * print_depth * 2 + '<symbol> ' + self.tokens.tokenValue() + ' </symbol>\n')
            self.tokens.advance()
            self.compile_term(print_depth + 1)
        self.xml.write(' ' * (print_depth - 1) * 2 + '</expression>\n')

    def compile_subroutineCall(self, print_depth, skip):
        if skip == 0:
            self.varName(print_depth)
        if self.tokens.tokenValue() == '.':
            self.xml.write(' ' * print_depth * 2 + '<symbol> . </symbol>\n')
            self.tokens.advance()
            self.varName(print_depth)
        self.xml.write(' ' * print_depth * 2 + '<symbol> ( </symbol>\n')
        self.tokens.advance()
        if self.tokens.tokenValue() != ')':
            self.compile_expressionList(print_depth + 1)
        else:
            self.xml.write(' ' * print_depth * 2 + '<expressionList>\n')
            self.xml.write(' ' * print_depth * 2 + '</expressionList>\n')
        self.xml.write(' ' * print_depth * 2 + '<symbol> ) </symbol>\n')
        self.tokens.advance()

    def compile_expressionList(self, print_depth):
        self.xml.write(' ' * (print_depth - 1) * 2 + '<expressionList>\n')
        self.compile_expression(print_depth + 1)
        while self.tokens.tokenValue() == ',':
            self.xml.write(' ' * print_depth * 2 + '<symbol> , </symbol>\n')
            self.tokens.advance()
            self.compile_expression(print_depth + 1)
        self.xml.write(' ' * (print_depth - 1) * 2 + '</expressionList>\n')

    def compile_term(self, print_depth):
        self.xml.write(' ' * (print_depth - 1) * 2 + '<term>\n')
        if self.tokens.tokenValue() in ('-', '~'):
            self.xml.write(' ' * print_depth * 2 + '<symbol >' + self.tokens.tokenValue() + '< /symbol>\n')
            self.tokens.advance()
            self.compile_term(print_depth + 1)
        elif self.tokens.tokenValue() == '(':
            self.xml.write(' ' * print_depth * 2 + '<symbol> ( </symbol>\n')
            self.tokens.advance()
            self.compile_expression(print_depth + 1)
            self.xml.write(' ' * print_depth * 2 + '<symbol> ) </symbol>\n')
            self.tokens.advance()
        else:
            if self.tokens.tokenType() == 'INT_CONST':
                self.xml.write(' ' * print_depth * 2 + '<integerConstant> ' + self.tokens.tokenValue() + ' </integerConstant>\n')
                self.tokens.advance()
            elif self.tokens.tokenType() == 'STRING_CONST':
                self.xml.write(' ' * print_depth * 2 + '<stringConstant> ' + self.tokens.tokenValue() + ' </stringConstant>\n')
                self.tokens.advance()
            elif self.tokens.tokenType() in ('true', 'false', 'null', 'this'):
                self.xml.write(' ' * print_depth * 2 + '<keywordConstant> ' + self.tokens.tokenValue() + ' </keywordConstant>\n')
                self.tokens.advance()
            else:
                self.varName(print_depth + 1)
                if self.tokens.tokenValue() == '[':
                    self.xml.write(' ' * print_depth * 2 + '<symbol> [ </symbol>\n')
                    self.tokens.advance()
                    self.compile_expression(print_depth + 1)
                    self.xml.write(' ' * print_depth * 2 + '<symbol> ] </symbol>\n')
                    self.tokens.advance()
                elif self.tokens.tokenValue() in ('(' , '.'):
                    self.compile_subroutineCall(print_depth, 1)
        self.xml.write(' ' * (print_depth - 1) * 2 + '</term>\n')


