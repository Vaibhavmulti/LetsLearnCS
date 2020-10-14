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
