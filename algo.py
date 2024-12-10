import re
import string

fin = open('main.py', 'r') # sys.argv[1]
file = fin.readlines()
fin.close()


def filter(data: str) -> str:
    ans = ''
    for symb in data:
        if ((symb in string.ascii_lowercase) or (symb in string.ascii_uppercase)
                or (symb in string.digits) or symb == ' '):
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
    def __init__(self, buf, num, var, val):
        self.buf, self.num, self.stack = buf, num, []
        self.allowed_ops = ["+", "-", "*", "/", "%", "==", "!=", "and", "or", "<", ">", "<=", ">="]
        self.logical_ops = ["if", "elif", "else"]
        self.comments = ['#', "\"\"\""]
        self.special_tags = ["def", "class"]
        self.path = ((num % 2) == 0)
        self.var, self.val = var, val

    def parse(self, data: list[str]):
        if data[0] == 'if' or data[0] == 'def':
            for part in data:
                if ((self.allowed_ops.count(part) > 0 or self.logical_ops.count(part) == 0)
                        and self.comments.count(part) == 0):
                    self.stack.append(part)
        self.stack.clear()

    def stop(self) -> tuple[str, ...]:
        return self.var, self.val


class WalkerMaster:
    def __init__(self):
        self.slaves = []  # those are giving the result
        self.variables = {}  # name - list of WalkerSlaves which is handling only one parameter

    def add_slave(self, val, var):
        self.slaves.append(WalkerSlave('', len(self.slaves) - 1, var, val))

    def add_tracing_var(self, var_name: str, var_val: int | str | list | tuple | dict) -> None:
        self.variables[var_name] = var_val

    def parse_tracing(self, data: list[str]) -> None:
        big_comment = False
        for _string in data:
            if "\"\"\"" in _string:
                big_comment = not big_comment
            if "input()" in _string and not big_comment and _string.count('#') == 0:
                self.add_tracing_var(_string.split()[0], _string.split()[2])
            if "def" in _string and not big_comment and _string.count('#') == 0:
                args, func_name = sep_func(_string.split()[1])
                for arg in args.split(', '):
                    self.add_tracing_var(arg, '')
            if "=" in _string and not big_comment and _string.count('#') == 0 and "if" != _string.split()[0]:
                self.add_tracing_var(_string.split()[0], filter(' '.join(_string.split()[2:])))


def aka_eval(data, walkerslave: WalkerSlave):
    if walkerslave.var not in walkerslave.stack:  # case when evaluating variable not in expression
        return None
    walkerslave.parse(data)
    walkerslave.stack[1] = walkerslave.stack[1].replace('=', '')
    walkerslave.val = eval('walkerslave.val' + ' '.join(walkerslave.stack[1:]))
    print(walkerslave.val)


wm = WalkerMaster()
wm.parse_tracing(file)

ws = WalkerSlave('', 0, 'data', '')

for i in range(len(file)):
    if len(file[i].split()) > 1 and (file[i].split()[0] == 'if' or file[i].split()[0] == "def"
                                     or file[i].split()[1] == "def"):
        wm.add_slave('', sep(file[i].split()[1]))
    aka_eval(file[i].split(), ws)
    # aka_eval(file[i].split(), wm.slaves[-1])
print(wm.variables)
# for i in wm.slaves:
#     print(i.var, i.val)
