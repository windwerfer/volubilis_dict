
# import pdb
from ast import arg
import os
import sys
import regex

# to create a direcory if not exits
from pathlib import Path


from pprint import pp    # type: ignore  # noqa


def readfile(file, limit=-1):
    # file_out = 'tmp/' + regex.sub('^.*/', '', file)
    f = open(file + '.txt','r')
    lines = 100
    l = ' '
    end = False
    i = 0
    while True:
        if limit > 0 and i > limit:
            break

        li = []
        for x in range(0, lines):
            l = f.readline();
            if l == '':
                end = True
                break
            # for the first cycle check if there is a title
            if i == 0 and l[0:2] == '##':
                filter_title(l, file)
            else:
                li.append(l)

        # pp(li)
        la = process_to_txtMdx(li)
        a = False if i == 0 else True
        save_to(file + '_mdx.txt', la, append=a)
        i += 1
        if end:
            break

def filter_title(line, file):
    tmp = line.split('\t')
    if tmp[0] == '##description':
        save_to(file + '_description.html',[tmp[1]],append=False)
    if tmp[0] == '##title' or tmp[0] == '##name':
        save_to(file + '_title.html',[tmp[1]],append=False)


def process_to_txtMdx(li):
    r = []
    for l in li:
        tmp = l.split('\t')
        #ignore invalid entries
        if len(tmp) != 2 or len(tmp[0]) == 0 or len(tmp[1]) == 0:
            continue
        # tmp[1] already has a \n at the end

        #check for synonyms
        syn = tmp[0].split('|')
        if len(syn) > 1:
            tmp[0] = syn[0]
            # starting with syn[1]: referrence all words to the first one
            for s in range(1,len(syn)):
                x = syn[s] + '\n@@@LINK=' + syn[0] + '\n</>\n'
                r.append(x)
        #remove newline at the end of the string
        tmp[1] = regex.sub(r'\\n', '', tmp[1])

        x = tmp[0] + '\n' + tmp[1] + '</>\n'
        r.append(x)
    return r


def save_to(file, li, append=True):
    if append:
        mode = 'a'
    else:
        mode = 'w'
    f = open(file, mode)
    for l in li:
        f.write(l)


if __name__ == "__main__":
    usage = 'python convert_ta..mdxTxt.py <file> <limit> \n <file> needs to be a .txt file \n(<limit> is optional)'
    if len(sys.argv) <= 1 or sys.argv[1] == '-h':
        print (usage)
        exit()
    argv1 = sys.argv[1]
    if argv1[-4:] != '.txt':
        print("<file> must be a .txt file")
        exit()
    else:
        argv1 = argv1[:-4]
    argv2 = -1
    limit = ''
    if len(sys.argv) == 3:
        argv2 = int(sys.argv[2])
        limit = f' (limiting to {str(argv2)} lines)'

    # -p -> no error if exists
    # os.system('mkdir -p tmp')
    readfile(argv1, limit=argv2)
    pp(f"file '{argv1}' prepared for mdx. {limit}")
