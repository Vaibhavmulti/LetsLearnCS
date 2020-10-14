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
