import os
import sys

#Author : Todoroki Sasha Namasaki
#Github : https://github.com/LAPUS12l/
#Content : Programming language from python

#Open a file using args and open
code = open(sys.argv[1], "r").readlines()
c = []
for i in code:
    c.append(i.replace("\n", ""))
code = c

#Error
def error(valueError, line): #We first declare our error function because it will use to everything
    print(f"""
An Error occured:

    ValueError  : {valueError}
    Line        : {line}
    Destination : {os.getcwd()}

exit code 1""")
    exit()

class IF_NODE:
    def __init__(self, assignment):
        self.Assign = assignment
    def make(self):
        return Assigner(self.Assign).Make_assignment()
class FUNC_NODE:
    def __init__(self, assignment):
        self.Assign = assignment
    def make(self):
        return Assigner(self.Assign).Make_assignment()
#Assigning method
class Assigner:
    def __init__(self, code):
        self.code = code
        self.assignment = []
        self.keys = ["PRINT", "DEF"]
        self.error_part = ""
        self.line = 1
        self.operators = ["+", "-", "/", "*"]
        self.arg_operators = ["==", "!=", "@=", "#="] #EQ_EQ, NOT_EQ, IN, NOT_IN
        self.in_if = False
        self.if_arg = []
        self.arry = []
        self.if_assign = []
        self.in_func = False
        self.func_name = ""
        self.func_idents =[]
        self.func_assign = []
        self.identaa = []
    def Make_assignment(self):
        for i in self.code:
            if self.in_if is False and self.in_func is False:
                if i[0:5]  == "PRINT":
                    i = i.replace("PRINT", "", 1)
                    i = i.lstrip()
                    self.assignment.append({"PRINT":i})
                elif i.lstrip().rstrip() == "":
                    continue
                elif i[0:3] == "DEF":
                    i = i.replace("DEF", "", 1)
                    i = i.lstrip()
                    self.name = ""
                    self.value = ""
                    self.id = "name"
                    for i in i:
                        if i != "=" and self.id == "name":
                            self.name += i
                        elif i == "=" and self.id == "name":
                            self.name = self.name.lstrip()
                            self.name = self.name.rstrip()
                            self.id = "value"
                        elif self.id == "value":
                            self.value += i
                        
                    self.value = self.value.lstrip()
                    self.value = self.value.rstrip()
                    if self.value == "":
                        error("Can't create value with an ''", self.line)
                    else:
                        self.assignment.append({"DEF":[self.name, self.value]})
                elif i[0:5] == "INPUT":
                    i = i.replace("INPUT", "", 1)
                    self.holder = ""
                    self.storing_var = ""
                    self.id = "var"
                    for i in i:
                        if i != "<" and self.id == "var":
                            self.storing_var += i
                        elif i == "<" and self.id == "var":
                            self.storing_var = self.storing_var.lstrip()
                            self.storing_var = self.storing_var.rstrip()
                            self.id = "hold"
                        elif self.id == "hold":
                            self.holder += i
                    self.assignment.append({"INPUT":[self.storing_var, self.holder]})
                elif i[0:2] == "IF":
                    i = i.replace("IF", "", 1)
                    self.id = ""
                    self.tmp = ""
                    self.st = 0
                    for i in i:
                        self.tmp += i
                        if i == "|" and self.st == 0:
                            self.if_arg.append(self.tmp)
                            self.st = 1
                            self.tmp = ""
                        elif i == "|" and self.st == 1:
                            self.tmp = self.tmp[0:len(self.tmp)-1]
                            self.tmp = self.tmp.lstrip()
                            self.tmp = self.tmp.rstrip()
                            if self.tmp in self.arg_operators:
                                self.if_arg.append(self.tmp)
                                self.tmp = ""
                                self.st = 2 
                            else:
                                error("Invalid argument operator '"+self.tmp+"'", self.line)
                        elif i == "{" and self.st == 2:
                            self.if_arg.append(self.tmp)
                            self.tmp = ""
                    
                    if len(self.if_arg) < 3:
                        error("No last argument", self.line)
                    self.in_if = True
                elif i[0:4] == "FUNC":
                    i = i.replace("FUNC", "", 1)
                    self.id = "name"
                    self.name = ""
                    self.idents = []
                    self.tmp = ""
                    self.count_index = 0
                    for loc in i:
                        self.count_index += 1
                        if loc != "(" and self.id == "name":
                            self.tmp += loc
                        if loc == "(" and self.id == "name":
                            self.name = self.tmp
                            self.tmp = ""
                            self.id = "iden"
                        if loc != ")" and self.id == "iden" or loc != "," and self.id == "iden":
                            self.tmp += loc
                        if self.id == "iden" and loc == ",":
                            self.idents.append(self.tmp.replace("(", "", 1)[0:len(self.name)-2].lstrip())
                            self.tmp = ""
                        if self.id == "iden" and loc == ")":
                            if self.tmp.lstrip().rstrip() == "":
                                pass
                            else:
                                self.idents.append(self.tmp[0:len(self.tmp)-1].lstrip().rstrip())
                                break
                    self.name = self.name.lstrip().rstrip()
                    if i[self.count_index:len(i)].lstrip().rstrip() == "{":
                        self.in_func = True
                        self.func_name = self.name
                        self.identaa = self.idents
                        self.idents = []
                    else:
                        error("Expected end block '{'", self.line)
                elif i[0:1] == "#":
                    i = i.replace("#", '', 1)
                    self.id = "name"
                    self.name = ""
                    self.idents = []
                    self.tmp = ""
                    self.count_index = 0
                    for loc in i:
                        self.count_index += 1
                        if loc != "(" and self.id == "name":
                            self.tmp += loc
                        if loc == "(" and self.id == "name":
                            self.name = self.tmp
                            self.tmp = ""
                            self.id = "iden"
                        if loc != ")" and self.id == "iden" or loc != "," and self.id == "iden":
                            self.tmp += loc
                        if self.id == "iden" and loc == ",":
                            self.idents.append(self.tmp.replace("(", "", 1)[0:len(self.name)].lstrip())
                            self.tmp = ""
                        if self.id == "iden" and loc == ")":
                            if self.tmp.lstrip().rstrip() == "":
                                pass
                            else:
                                self.idents.append(self.tmp[0:len(self.tmp)-1].lstrip().rstrip())
                                break
                    self.name = self.name.lstrip().rstrip()
                    self.assignment.append({"CALL_F_PROTO":[self.name, self.idents]})
                    self.idents= []
                    self.tmp = ""
                    self.name = ""
                #Module feature
                elif i[0:6] == "MODULE":
                    i = i.replace("MODULE", "", 1)
                    i = i.lstrip().rstrip()
                    self.assignment.append({"MODULE":i})
                else:
                    if ' ' in i:
                        i = i[0:i.index(' ')]
                    else:
                        pass
                    error("Keyword Error '"+i+"'", self.line)
                self.line += 1
            elif self.in_if is True:
                if i != "}":
                    if i.lstrip().rstrip() == "":
                        continue
                    elif i[0] == "\t":
                        i = i.replace("\t", "", 1)
                        self.arry.append(i)
                    else:
                        error("Indent error expected '\t'", self.line)
                elif i == "}":
                    self.if_assign = IF_NODE(self.arry).make()
                    self.assignment.append({"IF":[self.if_arg, self.if_assign]})
                    self.in_if = False
                    self.if_arg = []
                    self.arry = []
                    self.if_assign = []
            elif self.in_func is True:
                if i != "}":
                    if i.lstrip().rstrip() == "":
                        continue
                    if i[0] == "\t":
                        i = i.replace("\t", "", 1)
                        self.arry.append(i)
                    else:
                        error("Indent error expected '\t'", self.line)
                elif i == "}":
                   
                    self.func_assign = FUNC_NODE(self.arry).make()
                    self.arry = []
                    self.in_func = False
                    self.assignment.append({"FUNC":[[self.func_name, self.identaa], self.func_assign]})
                    self.func_name = ""
                    self.func_assign = []
                    self.identaa = []
                    self.in_func = False
                    self.func_name = ""
                    self.func_idents =[]
                    self.func_assign = []
                    self.identaa = []
                    
        return self.assignment

#Execution
class Executor:
    def __init__(self):
        self.assignment = []
        self.varriables = {"Name":"John"}
        self.back_up_varriables = {}
        self.line = 1
        self.functions = []
        self.fn_names = []
        self.identss = []
    def make_val(self, regex='""'):
        self.id = ""
        self.tmp = ""
        self.value = ""
        self.operators = ["+", "-", "/", "*"] #add, minus, devide, multiply
        self.int = ['1','2','3','4','5','6','7','8','9','0']
        self.do = ""
        for i in regex:
            self.tmp += i
            if i == '"' and self.id == "" or i =="'" and self.id == "":
                self.id = "char"
            elif i == '"' and self.id == "char" or i == "'" and self.id == "char":
                self.value += self.tmp
                self.tmp = ""
                self.id = ""
            elif self.id == "char":
                pass
            elif i == " " and self.id == "":
                self.tmp = ""
            elif i == "{" and self.id == "":
                self.id = "varname"
            elif self.id == "varname" and i != "}":
                pass
            elif self.id == "" and i == "s":
                self.id = "string-e"
                self.tmp = ""
            elif i == "(" and self.id == "string-e":
                self.tmp = ""
                self.id = "start-string-e"
            elif self.id == "start-string-e" and i != ")":
                self.do += i
                self.tmp = ""
            elif self.id == "start-string-e" and i == ")":
                self.value += "str("+self.make_val(regex=self.do)+")"
                self.id = ''
                self.tmp = ''
            elif i != "(" and self.id == "string-e":
                error("Illegal Syntax '"+i+"'", self.line)
            elif i == "}" and self.id == "varname":
                try:
                    self.value += self.varriables[self.tmp[1:len(self.tmp)-1]]
                    self.tmp = ""
                    self.id = ""
                except:
                    error("Varriable name '"+self.tmp+"' not found", self.line)
            elif i in self.operators and self.id == "":
                self.value += i
                self.tmp = ""
            elif i in self.int and self.id == "":
                self.value += i
            else:
                error("Illegal Syntax '"+i+"'", self.line)
        try:
            eval(self.value)
        except:
            error("String int combination '"+self.value+"' or operator is invalid", self.line)
        return self.value
                    
    def Execute(self, code):
        self.assignment = code
        for i in self.assignment:
            for l in i:
                if l == "PRINT":
                    self.value = self.make_val(regex=i[l])
                    print(eval(self.value))
                elif l == "DEF":
                    self.all = i[l]
                    self.name = self.all[0]
                    self.value = self.all[1]
                    self.make_val(regex=self.value) #Check if there is an error or nothing
                    if '"' in self.name:
                        error("Illegal name part '\"'", self.line)
                    elif "+" in self.name or "-" in self.name or "*" in self.name or "/" in self.name:
                        error("Illegal name part operator", self.line)
                    elif  "'" in self.name:
                        error("Illegal name part \"'\"", self.line)
                    elif " " in self.name:
                        error("Illegal name part ' '", self.line)
                    self.varriables[self.name] = self.value
                elif l == "INPUT":
                    self.name = i[l][0]
                    self.hold = i[l][1]
                    self.name_checker(self.name)
                    self.make_val(self.hold)
                    self.varriables[self.name] = '"'+input(eval(self.make_val(self.hold)))+'"'
                elif l == "IF":
                    self.all_args = i[l][0]
                    self.all_args[0] = self.all_args[0][0:len(self.all_args[0])-1].lstrip().rstrip()
                    self.all_args[2] = self.all_args[2][0:len(self.all_args[2])-1].lstrip().rstrip()
                    if self.all_args[1] == "@=":
                        self.all_args[1] = "in"
                    elif self.all_args[1] == "#=":
                        self.all_args[1] = "#="
                    self.arg = ""
                    self.count = 0
                    for n in self.all_args:
                        if self.count == 0: #First arg
                            self.arg += self.make_val(self.all_args[0])
                            self.count = 1
                        elif self.count == 1: # This is the oprerator So we will not gonna do any changes (Just to add some spaces)
                            self.arg += " "+self.all_args[1]+" "
                            self.count =2
                        elif self.count == 2:
                            self.arg += self.make_val(self.all_args[2])
                    if eval(self.arg):
                       self.reparse(i[l][1])
                elif l == "FUNC":
                    self.fn_names.append(i[l][0][0])
                    self.functions.append({i[l][0][0]:i[l][1]})
                    self.idents = i[l][0][1]
                    self.identss.append({i[l][0][0]:self.idents})
                elif l == "CALL_F_PROTO":
                    self.name = i[l][0]
                    self.idents = i[l][1]
                    if self.name in self.fn_names:
                        pass
                    else:error("No Function '"+self.name+"' Found", self.line)
                    self.back_up_varriables = self.varriables
                    self.varriables = {}
                    self.func_args = self.functions
                    self.identsss  = None
                    self.ass = []
                    self.ok = ""
                    for i in self.identss:
                        for pr in i:
                            self.ok = pr.replace("(", "", 1).lstrip().rstrip()
                            break
                        break
                    self.identss[0] = self.ok
                    print(self.identss)
                    for n in self.identss:
                        for nn in n:
                            if nn == self.name:
                                self.identsss = n[nn]
                    self.count = 0
                    for i in self.idents:
                        self.varriables[self.identsss[self.count]] = self.idents[self.count]
                        self.count += 1
                    for i in self.functions:
                        for n in i:
                            if n == self.name:
                                self.ass = i[n]
                    
                    for i in self.varriables:
                        self.i_val = self.varriables[i]
                    print(self.varriables)
                    self.reparse(self.ass)
                elif l == "MODULE":
                    self.name = i[l]
                    self.array = []
                    try:
                        open(self.name, "r")
                    except:
                        error("No module name '"+self.name+"' found at the directory '"+os.getcwd()+"'", self.line)
                    self.array = open(self.name, "r").readlines()
                    self.array= Assigner(self.array).Make_assignment()
                    self.reparse(self.array)
                    
                        
            self.line += 1
    def name_checker(self, name):
        self.name = name
        if '"' in self.name:
            error("Illegal name part '\"'", self.line)
        elif "+" in self.name or "-" in self.name or "*" in self.name or "/" in self.name:
            error("Illegal name part operator", self.line)
        elif  "'" in self.name:
            error("Illegal name part \"'\"", self.line)
        elif " " in self.name:
            error("Illegal name part ' '", self.line)
    def reparse(self, s):
        self.Execute(s)

Assignment = Assigner(code).Make_assignment()
if len(sys.argv) > 2:
    if sys.argv[2] == "--showt":
        print(Assignment)
    else:
        error("Option error '"+sys.argv[2]+"'", 0)
#Exexution
Executor().Execute(Assignment)
