import sys

fin = open(sys.argv[1], 'r')
file = fin.readlines()

print("Analysis started")

class Walker:
    def __init__(self, buf, num):
        self.buf, self.num = buf, num


    def modify_true(self, data):
        if data[0] == 'if':
            self.parsed = data
            print(self.parsed)


    def modify_false(self, data):
        if data[0] == 'if':
            self.parsed = data
            print(self.parsed)


    def stop(self):
        pass

walkers = []
for i in range(len(file)):
    if file[i].split()[0] == 'if':
        walkers.append(Walker('', len(walkers) - 1))
        walkers.append(Walker('', len(walkers) - 1))
        walkers[-2].modify_true(file[i].split())
        walkers[-1].modify_false(file[i].split())
        # print(file[i])
        # print("if statement found! {} on str {}".format(file[i].split(), i))


fin.close()
