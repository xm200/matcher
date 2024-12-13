import re
import string

fin = open('main.py', 'r') # sys.argv[1]
file = fin.readlines()
fin.close()


def filter(data: str) -> str:
    ans = ''
    for symb in data:
        if ((symb in string.ascii_lowercase) or (symb in string.ascii_uppercase)
                or (symb in string.digits) or symb == ' ') or symb in '\'\"':
            ans += symb
    return ans


def sep_func(data: str) -> tuple[str, str]:
    func_name, var_name = '', ''
    for symb in data:
        if symb == '(':
            var_name, func_name = func_name, var_name
            func_name += symb
        if symb == ')':
            func_name += symb
        var_name += symb
    return filter(var_name), filter(func_name)


def sep_method(data: str) -> tuple[str, ...]:
    return tuple(data.split('.'))


def sep(data: str) -> tuple[str, str]:
    _type = re.search(r'^\D+[(]\D+[)]$', data)  # func(name) - True Class.method() - False
    return sep_func(data) if (_type is not None) else sep_method(data)


class WalkerSlave:
    def __init__(self, num, var, val, type: str):
        self.num, self.stack = num, []
        self.allowed_ops = ["+", "-", "*", "/", "%", "==", "!=", "and", "or", "<", ">", "<=", ">="]
        self.logical_ops = ["if", "elif", "else"]
        self.comments = ['#', "\"\"\""]
        self.path = ((num % 2) == 0)
        self.var, self.val, self.val_type = var, val, type

    def gen(self, condition):
        value1 = condition[0]
        operator = condition[1]
        value2 = condition[2]
        if condition[2] != 'self.val':
            value2 = filter(condition[2])
        if operator in ['<=', '>=']:
            return [value1, value2] if value2 is not None else [value1]
        elif operator in ['>', '<']:
            return [value2 - 1, value2 + 1] if eval(f"{value1} {operator} {value2}") and operator == '>' else \
                [min(value1, value2 + 1), max(value1, value2 + 1)]
        elif operator in ['!=', 'is not', '==', 'is']:
            if not eval(f"{value1} {operator} {value2}"):
                return [eval(i) for i in [value1, value2]]
            else:
                if type(value2) is int or type(value2) is float or self.val_type != 'str':
                    return [int(eval(value1)) + 1, eval(value2)]
                elif type(value2) is str:
                    return [str(eval(value1)) + 'A', eval(value2)]
        else:
            raise ValueError(f"Неизвестный оператор: {operator}")

    def aka_eval(self, data: str):
        if self.var not in data:  # case when evaluating variable not in expression
            return None
        self.stack = data.replace(f'{self.var}', f'{self.val}')
        self.stack = self.stack.split()
        if self.stack[1] not in ['==', '>=', '<=', '!=', '=']:  # nuh-uh it`s if!
            self.stack[1] = self.stack[1].replace('=', '')
        if self.stack[1] == '=':
            self.val = self.stack[2]
            self.stack.clear()
            return
        self.val = eval(' '.join(self.stack[:]))
        self.stack.clear()

    def discover(self, data):
        for i in data:
            if i.split()[0] in ['if', 'elif']:
                i = i.replace(f'{self.var}', 'self.val')
                print(self.gen(i.split()[1:]))
                continue
            self.aka_eval(i)  # todo: make code discovering;use dfs idea,
        # get some useful discovering information from WM, store it and start voyage

    def stop(self) -> tuple[str, ...]:
        return self.var, self.val


class WalkerMaster:
    def __init__(self):
        self.slaves = []  # those are giving the result
        self.variables = set()  # name - list of WalkerSlaves which is handling only one parameter

    def add_slave(self, var, val, _type: str):
        self.slaves.append(WalkerSlave(len(self.slaves), var, val, _type))

    def add_tracing_var(self, var_name: str) -> None:
        self.variables.add(var_name)

    def parse_tracing(self, data: list[str]) -> None:
        big_comment = False
        for _string in data:
            if "\"\"\"" in _string:
                big_comment = not big_comment
            if "input()" in _string and not big_comment and _string.count('#') == 0:
                self.add_tracing_var(_string.split()[0])
            if "def" in _string and not big_comment and _string.count('#') == 0:
                args, func_name = sep_func(_string.split()[1])
                for arg in args.split(', '):
                    self.add_tracing_var(arg)
            if "=" in _string and not big_comment and _string.count('#') == 0:
                if _string.split()[0] not in ['elif', 'if']:
                    self.add_tracing_var(_string.split()[0])
                else:
                    self.add_tracing_var(_string.split()[1])

    def start(self):
        global file
        self.parse_tracing(file)
        print(self.variables)
        self.variables = list(self.variables)
        for i in file:
            self.add_slave(self.variables[0], '', '')


# ws = WalkerSlave(0, '.discover', 7999989888, "int")
# ws.discover(['.discover += 234','.discover = 1', '.discover /= 0.1922112'])
# print(ws.val)

wm = WalkerMaster()
wm.start()

