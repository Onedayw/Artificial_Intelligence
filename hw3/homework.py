import copy, Queue

kb, queries, clauses, varCount = None, [], [], 0

'''STDIN & STDOUT'''

#Read file
def readFile(fname):
    f = open(fname, "r")
    global kb, queries, clauses
    nq = int(f.readline().strip('\r\n'))
    queries = [Node(f.readline().strip('\r\n')) for i in range(nq)]
    nc = int(f.readline().strip('\r\n'))
    clauses = [f.readline().strip('\r\n') for i in range(nc)]
    f.close()
    kb = KnowledgeBase()
    for c in clauses:
        kb.add_clauses(to_cnfs(c))

'''PARSE INPUTS'''

def expand(exp):
    if isinstance(exp, Node):
        return exp.negate()
    elif exp[0] == 'not':
        return exp[1]
    elif exp[0] == 'and':
        exp[0], exp[1], exp[2] = 'or', expand(exp[1]), expand(exp[2])
    elif exp[0] == 'or':
        exp[0], exp[1], exp[2] = 'and', expand(exp[1]), expand(exp[2])
    return exp

def distribute(exp):
    res = []
    if isinstance(exp, Node):
        res.append([exp])
    elif exp[0] == 'and':
        res.extend(distribute(exp[1]))
        res.extend(distribute(exp[2]))
    elif exp[0] == 'or':
        left, right = distribute(exp[1]), distribute(exp[2])
        for o1 in left:
            for o2 in right:
                list = []
                list.extend(o1)
                list.extend(o2)
                res.append(list)
    return res

def to_cnfs(s):
    s = s.replace(' ', '')
    return [Clause(c).factorize() for c in distribute(parse(s))]

def fetch(sentence):
    if 'A' <= sentence[0] <= 'Z':
        return '', [sentence]
    npar, i, operator, operands, start = 0, 0, '', [], -1
    while i < len(sentence):
        if sentence[i] == '(':
            npar += 1
            if npar == 1:
                start = i + 1
        elif sentence[i] == ')':
            npar -= 1
            if npar == 0:
                operands.append(sentence[start: i].strip())
        elif npar == 1: 
            if sentence[i] == '&' or sentence[i] == '|':
                operands.append(sentence[start: i].strip())
                operator, start = sentence[i], i + 1
            elif sentence[i] == '=':
                operands.append(sentence[start: i].strip())
                i += 1
                operator, start = '=>', i + 1
            elif npar == 1 and sentence[i] == '~':
                operator, start = '~', i + 1
        i += 1
    return operator, operands

def parse(sentence):
    operator, operands = fetch(sentence)
    if operator == '&':
        o1, o2 = parse(operands[0]), parse(operands[1])
        return ['and', o1, o2]
    elif operator == '|':
        o1, o2 = parse(operands[0]), parse(operands[1])
        return ['or', o1, o2]
    elif operator == '~':
        o = parse(operands[0])
        if isinstance(o, Node):
            return o.negate()
        else:
            return expand(o)
    elif operator == '=>':
        o1, o2 = parse(operands[0]), parse(operands[1])
        return ['or', parse('(~' + operands[0] + ')'), o2]
    elif operator == '':
        return Node(operands[0])
    
'''CLASSES'''    

#Atomic literal
class Node(object):
    __slots__ = '__sign', '__predicate', '__arguments'
    
    def __init__(self, s):
        s = s.replace(' ', '')
        if s[0] == '~':
            self.__sign, s = False, s[1:]
        elif s[1] == '~':
            self.__sign, s = False, s[2:-1]
        else:
            self.__sign = True
        self.__predicate = s[0: s.find('(')]
        self.__arguments = s[s.find('(') + 1: s.find(')')].split(',')
    
    def negate(self):
        self.__sign = not self.__sign
        return self
    
    def complements_to(self, node2):
        if self.__predicate != node2.predicate() or self.__sign == node2.sign():
            return False
        for i in range(len(self.__arguments)):
            if self.__arguments[i] != node2.arguments()[i]:
                return False
        return True
    
    def set_indices(self, count):
        for i in range(len(self.__arguments)):
            if is_variable(self.__arguments[i]):
                self.__arguments[i] = self.__arguments[i][0] + str(count)
                
    def set_variables(self, dict):
        for i in range(len(self.__arguments)):
            if self.__arguments[i] in dict:
                self.__arguments[i] = dict[self.__arguments[i]]
    
    def sign(self): return self.__sign
    def predicate(self): return self.__predicate
    def arguments(self): return self.__arguments
        
    def __eq__(self, node2):
        if self.__sign != node2.sign() or self.__predicate != node2.predicate():
            return False
        for i in range(len(self.__arguments)):
            if is_variable(self.__arguments[i]):
                if not is_variable(node2.arguments()[i]):
                    return False
            else:
                return self.__arguments[i] == node2.arguments()[i]
        return True
    
    def __hash__(self):
        return hash(self.to_string())
        
    def __str__(self):
        string = str()
        string += self.__predicate + '(' + ','.join(self.__arguments) + ')'
        if not self.__sign:
            string = '(~' + string + ')'
        return string
    
    def to_string(self):
        string = str(self.__sign) + self.__predicate
        for argument in self.__arguments:
            if is_variable(argument):
                string += 'x'
            else:
                string += argument
        return string

#DNF of Nodes
class Clause(object):
    __slots__ = '__nodes'
    
    def __init__(self, nodes):
        self.__nodes = nodes
    
    def set_indices(self):
        global varCount
        for node in self.__nodes:
            node.set_indices(varCount)
        varCount += 1
        
    def set_variables(self, dict):
        for node in self.__nodes:
            node.set_variables(dict)
            
    def can_factorize(self, i, j):
        if i == j:
            return False
        node1, node2 = self.__nodes[i], self.__nodes[j]
        if node1.predicate() != node2.predicate() or node1.sign() != node2.sign():
            return False
        if len(node1.arguments()) != len(node2.arguments()):
            return False
        for k in range(len(node1.arguments())):
            arg1, arg2 = node1.arguments()[k], node2.arguments()[k]
            if arg1 == arg2:
                continue
            if not is_variable(arg1) or not is_variable(arg2):
                return False
            for l in range(len(self.__nodes)):
                node3 = self.__nodes[l]
                if arg1 in node3.arguments() and arg2 in node3.arguments():
                    return False
        return True
    
    def factorize(self):    
        i = 0
        while i < len(self.__nodes):
            j = 0
            while j < len(self.__nodes):
                if self.can_factorize(i, j):
                    self.__nodes.pop(j)
                    if i > j:
                        i -= 1
                    j -= 1
                j += 1
            i += 1
        return self
    
    def is_useless(self):
        i = len(self.__nodes) - 1
        while i >= 0:
            for j in range(i):
                if self.__nodes[i].complements_to(self.__nodes[j]):
                    return True
            i -= 1
        return False
    
    def nodes(self): return self.__nodes
    
    def __eq__(self, clause2):
        dict = {}
        for node in self.__nodes:
            if node in dict:
                dict[node] = dict[node] + 1
            else:
                dict[node] = 1
        for node in clause2.nodes():
            if node in dict:
                dict[node] = dict[node] - 1
            else:
                return False
        for node in dict:
            if dict[node] != 0:
                return False
        return True
    
    def __hash__(self):
        res = 0
        for node in self.__nodes:
            res += hash(node.to_string())
        return res

    def __str__(self):
        return '[' + ' | '.join([str(node) for node in self.__nodes]) + ']'
    
#CNF of Clauses
class KnowledgeBase(object):
    __slots__ = '__clauses'
    
    def __init__(self):
        self.__clauses = []
        
    def add_clause(self, clause):
        clause.set_indices()
        self.__clauses.append(clause)
        
    def add_clauses(self, clauses):
        for clause in clauses:
            clause.set_indices()
            self.add_clause(clause)
    
    def clauses(self): return self.__clauses
    
    def __str__(self):
        strs = [str(c) for c in self.__clauses]
        return '\n'.join(strs)
    
'''FUNCTIONS'''
    
# Return true if x is a variable
def is_variable(x):
    if x == '' or isinstance(x, list): 
        return False
    else:
        return (97 <= ord(x[0]) <= 122)    

# Unify two nodes
def unify(node1, node2, dict={}):
    if node1.predicate() == node2.predicate() and node1.sign() != node2.sign():
        args1, args2 = node1.arguments(), node2.arguments()
        temp = {}
        for i in range(len(args1)):
            arg1, arg2 = args1[i], args2[i]
            while arg1 in temp:
                arg1 = temp[arg1]
            while arg2 in temp:
                arg2 = temp[arg2]
            if is_variable(arg1):
                temp[arg1] = arg2
            else:
                if is_variable(arg2):
                    temp[arg2] = arg1
                else:
                    if arg1 != arg2:
                        return None
        res = dict.copy()
        res.update(temp)
        return res
    else:
        return None

# 
def combine(clause1, clause2):
    res = []
    res.extend(clause1.nodes())
    res.extend(clause2.nodes())
    res = Clause(res)
    res.set_indices()
    if res.is_useless():
        return None
    return res.factorize()

# Resolution
def resolve(clause1, clause2):
    res, flag = [], True
    for node1 in clause1.nodes():
        for node2 in clause2.nodes():
            if node1.predicate() == node2.predicate() and node1.sign() != node2.sign():
                dict = unify(node1, node2)
                if dict is not None:
                    c1, c2, flag = copy.deepcopy(clause1), copy.deepcopy(clause2), False
                    c1.nodes().remove(node1)
                    c2.nodes().remove(node2)
                    c1.set_variables(dict)
                    c2.set_variables(dict)
                    c3 = combine(c1, c2)
                    if c3 is not None:
                        res.append(c3)
    if flag: return None
    return res

# Run process
def run(kb, query):
    query, queue, visited = Clause([query.negate()]), Queue.Queue(), set()
    queue.put(query)
    visited.add(query)
    while not queue.empty():
        c = queue.get()
        cs = resolve(query, c)
        if cs is not None:
            for c2 in cs:
                if len(c2.nodes()) == 0:
                    return True
        for clause in kb.clauses():
            if min(len(c.nodes()), len(clause.nodes())) < 3:
                cs = resolve(c, clause)
                if cs is not None:
                    for c2 in cs:
                        if len(c2.nodes()) == 0:
                            return True
                        elif c2 not in visited:
                                queue.put(c2)
                                visited.add(c2)
    return False
    
'''MAIN'''

def main():
    readFile("./input.txt")
    f = open("./output.txt", 'w')
    f.write('\n'.join([str(run(kb, q)).upper() for q in queries]) + '\n')
    f.close()

if __name__ == "__main__": 
    main()