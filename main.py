import yara
import os
import magic

filenames = os.listdir(os.getcwd() + '/rules/sources/')
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

if magic.from_file(path, mime=True).count('text') > 0:
    filenames = os.listdir(os.getcwd() + '/rules/sources/')
    functions = {}
    for i in filenames:
        if '_b' not in i:
            functions[i[:-4]] = os.getcwd() + '/rules/sources/' + i
else:
    functions = {}
    for i in filenames:
        if '_b' in i:
            functions[i] = os.getcwd() + '/rules/sources/' + i

rules = yara.compile(filepaths=functions)
detected = rules.match(path, which_callbacks=yara.CALLBACK_ALL)

if len(detected) == 0:
    print("Congrats! No rules matched.")
else:
    for function in detected:
        print(f"Found: {str(function)[:-5]}\nCallback: {function.tags}\nSecure version of this function: {bgdb[function.meta['name']]}")
        found = bgdb[function.meta['name']].split(', ')
        for i in found:
            print(f"Usage of {i}: {links_of_secure[i]}")
