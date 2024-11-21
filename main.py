import yara
import os
import magic

report = []


def get_callback(data):
    global report
    report.append(data)
    return yara.CALLBACK_CONTINUE


filenames = os.getcwd() + '/rules/'
path = input("Enter path to analyze: ")

if not os.access(path, os.F_OK):
    print("No such file or directory")
    exit(0)

if not os.access(path, os.R_OK):
    print("Check the permissions and try again")
    exit(0)

if os.path.isdir(path):
    print("Directory in uncheckable format!")
    exit(0)


functions = {}

if magic.from_file(path, mime=True).count('text') > 0:
    filenames += 'sources/'
else:
    filenames += 'binaries/'

for i in os.listdir(filenames):
    functions[i] = filenames + i

rules = yara.compile(filepaths=functions)
detected = rules.match(path, callback=get_callback, which_callbacks=yara.CALLBACK_MATCHES)

if len(detected) == 0:
    print("Congrats! No rules matched.")
else:
    print(*report)
