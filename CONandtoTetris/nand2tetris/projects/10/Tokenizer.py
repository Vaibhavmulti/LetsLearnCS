import os
import re


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


