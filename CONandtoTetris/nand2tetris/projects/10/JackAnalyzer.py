import sys
import os
import re
"""
Gets a file/ directory from the command line argument and generates xml file for the corresponding 
jack file(s) by first passing the jack file to Tokenizer(class) which generates the tokens 
which are then passed to CompilationEngine(class)
which finally generates the xml according to the recursive method calls. 
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
                        self.jack[0] = self.jack[0].replace(words_numbers_wrapped, '')
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
        self.xml.write(' ' * (print_depth - 1) * 2 + '<classVarDec>\n')
        self.type(print_depth)
        self.type(print_depth)
        self.varName(print_depth)
        while self.tokens.tokenValue() == ',':
            self.xml.write(' ' * print_depth * 2 + '<symbol> , </symbol>\n')
            self.tokens.advance()
            self.varName(print_depth)
        self.xml.write(' ' * print_depth * 2 + '<symbol> ; </symbol>\n')
        self.tokens.advance()
        self.xml.write(' ' * (print_depth - 1) * 2 + '</classVarDec>\n')


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
            elif self.tokens.tokenValue() in ('true', 'false', 'null', 'this'):
                self.xml.write(' ' * print_depth * 2 + '<keyword> ' + self.tokens.tokenValue() + ' </keyword>\n')
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


for (root, dirs, files) in os.walk(sys.argv[1], topdown=True):
    for file in files:
        if file.split('.')[1] == 'jack':
            #print(root+'\\'+file)
            token = Tokenizer(root+'\\'+file)
            parser = CompilationEngine(token, file.split('.')[0] + '.xml')

