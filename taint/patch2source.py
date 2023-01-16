import os
import re
from model.preprocessing import separate_diff_file


def parse_data(input_path):
    input_path = os.path.abspath(input_path)
    dirs = os.listdir(input_path)

    for commit in dirs:
        parse_commit(os.path.join(input_path, commit))


def parse_commit(commit_dir_path):
    patch_path = os.path.join(commit_dir_path, 'patch')
    with open(patch_path, 'r') as f:
        patch = f.read()
        sep_cnt = separate_diff_file(patch)

        for diff_cnt in sep_cnt:
            # diff_cnt is a paragraph in the patch file
            # only contains one file's diff result
            filename = diff_cnt.split('\n')[0].split(' ')[-1][2:].replace('/', '_')
            with open(os.path.join(commit_dir_path, 'before', filename), 'r') as bf:
                before_filecnt = bf.read()
            with open(os.path.join(commit_dir_path, 'patched', filename), 'r') as pf:
                patched_filecnt = pf.read()

            before_func = extract_function(before_filecnt)
            patched_func = extract_function(patched_filecnt)

            adds, decs = extract_patchline(diff_cnt)

            before_file_dependency = control_dependency_analysis(decs, before_filecnt,before_func)
            patched_file_dependency = control_dependency_analysis(adds, patched_filecnt, patched_func)

            """
            for line in decs:
                before_file_dependency += control_dependency_analysis(line, before_filecnt)
            for line in adds:
                patched_file_dependency += control_dependency_analysis(line, patched_filecnt)
            """
            cross_var, source_var, = extract_var(adds, decs)
            # these vars may be the security constrains

def extract_function(filecnt):
    func_list = []
    left = []
    right = []

    func_list.append([])
    func_list.append([])

    temp_pointer = 0
    while filecnt.index('{',temp_pointer)!=-1:
        left.append(filecnt.index('{',temp_pointer))

    temp_pointer = 0
    while filecnt.index('}',temp_pointer)!=-1:
        right.append(filecnt.index('}',temp_pointer))

    target = left.pop(0)
    while left!=[] and right!=[]:
        if left == [] and right!=[]:
            r = right.pop(0)
            func_list[0].append(target)
            func_list[1].append(r)
            break
        l = left.pop(0)
        r = right.pop(0)
        if l<r:
            # l matches r
            continue
        else:
            func_list[0].append(target)
            func_list[1].append(r)
            target = l

    return func_list

def control_dependency_analysis(patchlines, filecnt, funclist):
    # Input:
    # patchlines lines have been modified
    # filecnt    original file content
    # funclist   functions that extracted from the foriginal file,
    #             a list of tuple that each tuple indicats the
    #             left brace's and the right brace's position
    # Return:
    # dependency a subset of the funclist

    dependency = []
    for line in patchlines:
        ptr = filecnt.index(line)

        if check_dependency(dependency,ptr):
            continue

        leftptr=0
        while funclist[0][leftptr] < ptr:
            leftptr+=1
        leftptr=leftptr-1
        dependency.append((funclist[0][leftptr],funclist[1][leftptr]))

    return dependency


def check_dependency(dep_list,ptr):
    if dep_list==[]:
        return False
    for dep in dep_list:
        if ptr<dep[1] and ptr>ptr[0]:
            return True
    return False

"""
def control_dependency_analysis(patchline, filecnt):
    # patchline is a separate line in the patch file changes
    # filecnt is a str type original file content
    prev_content = []
    lines = filecnt.splitlines()
    linenum = lines.index(patchline)
    prev_content.append(linenum)
    idx = filecnt.find(patchline)

    right_brace = filecnt.rfind('}',0,idx)
    left_brace = filecnt.rfind('{',0,idx)

    while right_brace<left_brace:


    if left_brace>right_brace:
        # which means filecnt[left:] is a block contains the patchline
        # add all this block to line
        close_brace = filecnt.find('}',left_brace)
        cnt = filecnt[left_brace:close_brace].splitlines()
        for line in cnt:
            prev_content.append(lines.index(line))
        recognize_expression(left_brace,filecnt)

        # "else" doesn't mean that the patch line doesn't in a block
        # it may be a structure like:
        #
        # int func()
        # {
        #   { xxxx }
        #   path line <------
        # }
        #
        # so we have to recurrently call above comparision

    return prev_content
"""
def recognize_expression(left, filecnt):
    # left is the left brace's index
    # filecnt is the original file's content
    # This function aims to recognize what expression(if? while? for? function...) the following brace in
    right_bracket = filecnt.rfind(')',left)
    left_bracket = filecnt.rfind('(',left)

    if left - right_bracket < 3:
        expression = filecnt[left_bracket:right_bracket]
        return expression

def taint_var(var,filecnt):
    pattern_str = '^[=|!|>|<]=[ |\t|\n]*'+var
    propagation_list = []
    pattern = re.compile(pattern_str)
    filecnt.search(pattern,filecnt)


def extract_patchline(content):
    # This function scan the patch paragraph and only extract lines changed
    content = content.rstrip().split('\n')
    adds = []
    decs = []
    for line in content[4:]:
        if line[0] == '+':
            adds.append(line[1:])
        elif line[0] == '-':
            decs.append(line[1:])
    return adds, decs


def extract_var(addlines, declines):
    var_pattern = re.compile('[a-zA-Z][a-zA-Z_0-9]*')
    addvar = re.findall(var_pattern, addlines)
    decvar = re.findall(var_pattern, declines)

    stop_word = ['while', 'if', 'do', 'case', 'switch', 'else', 'break', 'continue', 'goto', 'return', 'for', 'typedef',
                 'NULL', 'const', 'struct', 'int', 'float', 'string', 'void', 'unsigned', 'long',
                 'sizeof', 'printf', 'malloc', 'free', 'ssize_t', 'size_t', 'define']

    for v in addvar:
        if v in stop_word:
            addvar.remove(v)

    for v in decvar:
        if v in stop_word:
            decvar.remove(v)

    union_var = set(addvar).union(set(decvar))
    cross_var = set(addvar).difference(set(decvar))
    # source_var is variables in addline while not in decline
    # which means it may be a variable in checking expression

    return cross_var, union_var
