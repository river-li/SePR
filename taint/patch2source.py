import os

def parse_data(input_path):
    input_path = os.path.abspath(input_path)
    dirs = os.listdir(input_path)

    for commit in dirs:
        parse_commit(os.path.join(input_path, commit))

def parse_commit(commit_dir_path):
    patch_path = os.path.join(commit_dir_path, 'patch')
    with open(patch_path,'r') as f:
        patch = f.read()

        diff_str = 'diff --git'
        separator = [patch.index(diff_str)]
        # separator is where "diff --git xxxxx xxxx" separate each file log

        sep = 0
        flag = True
        while flag:
            if patch.index(diff_str, sep) != cnt.rindex(diff_str):
                sep = patch.index(diff_str, sep + 1)
                separator.append(sep)
            else:
                if patch.rindex(diff_str) in separator:
                    flag = False
                else:
                    separator.append(patch.rindex(diff_str))


def change2source(filecontent, changed):
    pass