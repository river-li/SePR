#!/usr/bin/env python

import os
import re
import argparse
import multiprocessing
import numpy as np
import pandas as pd
from util.pretty_print import log, success, error


def parse_data(input_path, output_path=None):
    # output_path is a optional value
    # if called by other python files, the function would simply return a DataFrame.
    # the function will generate a  "csv" file if specified the output_path

    input_path = os.path.abspath(input_path)
    dirs = os.listdir(input_path)
    # pool = multiprocessing.Pool()
    # pool.map(parse_commit, dirs)

    feature = []

    for commit in dirs:
        feature.append(parse_commit(os.path.join(input_path, commit)))

    columns = ['files changed',
               'lines added',
               'lines removed',
               'loops added',
               'loops removed',
               'ifs added',
               'ifs removed',
               'boolean_op added',
               'boolean_op removed',
               'pairs added',
               'pairs removed',
               'function calls added',
               'function calls removed',
               'assignment added',
               'assignment removed',
               'sizeof added',
               'sizeof removed',
               'continue added',
               'continue removed',
               'break added',
               'break removed',
               'goto added',
               'goto removed',
               'return added',
               'return removed',
               'numerical added',
               'numerical removed',
               'compare added',
               'compare removed',
               'error added',
               'error removed',
               'char changed',
               ]

    df = pd.DataFrame(feature, columns=columns, dtype=np.int)
    success('Successfully Got DataFrame')

    if output_path:
        output_path = os.path.abspath(output_path)

        if os.path.isdir(output_path):
            feature_path = os.path.join(output_path, 'feature.csv')
            df.to_csv(feature_path)
            log("[+] Write CSV File to " + feature_path, "PURPLE")
        else:
            df.to_csv(output_path)
            log("[+] Write CSV File to " + output_path, "PURPLE")

    else:
        log("[-] Not Specified output_path, returning...", "PURPLE")

    return df


def extract_features(adds, decs):
    vec = np.zeros(32)
    # vec is a column vector with 10 dims
    #  0: files changed in a commit
    #  1: lines added
    #  2: lines removed
    #  3: loops added
    #  4: loops removed
    #  5: ifs added
    #  6: ifs removed
    #  7: boolean operators added
    #  8: boolean operators removed            log("[+] Write CSV File to "+output_path, "PURPLE")
    #  9: (){}[] added
    # 10: (){}[] removed
    # 11: function calls added
    # 12: function calls removed
    # 13: assignment added
    # 14: assignment removed
    # 15: sizeof added
    # 16: sizeof removed
    # 17: continue added
    # 18: continue removed
    # 19: break added
    # 20: break removed
    # 21: goto added
    # 22: goto removed
    # 23: return added
    # 24: return removed
    # 25: numerical operator (+-*/ >> << & |) added
    # 26: numerical operator (+-*/ >> << & |) removed
    # 27: compare operator (== >= <= < > !=) added
    # 28: compare operator removed
    # 29: error added
    # 30: error removed
    # 31: total char added/removed (added chars - removed chars)
    #     may be a negative value

    loop_op = re.compile('while |for ')
    if_op = re.compile('if ')
    bool_op = re.compile('\|\||\&\&|\!')
    pair_op = re.compile('\(')

    function_op = re.compile('[a-zA-Z0-9]\(')
    assignment_op = re.compile(' = ')
    sizeof = re.compile('sizeof\(')
    continue_op = re.compile('continue;')
    break_op = re.compile('break;')
    goto_op = re.compile('go ')
    return_op = re.compile('return[ |;]')
    # this may involve some "return" in comments

    numerical_op = re.compile('\+|-|>>|<<| \| | & ')
    # start (*) may be the pointer operator

    compare_op = re.compile('<=| < | > |==|>=|!=')
    # the space in the string is meaningful

    err_op = re.compile('err')

    addlines = ""
    for line in adds:
        addlines = addlines + line

    declines = ""
    for line in decs:
        declines = declines + line

    vec[1] = len(adds)
    vec[2] = len(decs)

    vec[3] = len(re.findall(loop_op, addlines))
    vec[4] = len(re.findall(loop_op, declines))

    vec[5] = len(re.findall(if_op, addlines))
    vec[6] = len(re.findall(if_op, declines))

    vec[7] = len(re.findall(bool_op, addlines))
    vec[8] = len(re.findall(bool_op, declines))

    vec[9] = len(re.findall(pair_op, addlines))
    vec[10] = len(re.findall(pair_op, declines))

    vec[11] = len(re.findall(function_op, addlines))
    vec[12] = len(re.findall(function_op, declines))

    vec[13] = len(re.findall(assignment_op, addlines))
    vec[14] = len(re.findall(assignment_op, declines))

    vec[15] = len(re.findall(sizeof, addlines))
    vec[16] = len(re.findall(sizeof, declines))

    vec[17] = len(re.findall(continue_op, addlines))
    vec[18] = len(re.findall(continue_op, declines))

    vec[19] = len(re.findall(break_op, addlines))
    vec[20] = len(re.findall(break_op, declines))

    vec[21] = len(re.findall(goto_op, addlines))
    vec[22] = len(re.findall(goto_op, declines))

    vec[23] = len(re.findall(return_op, addlines))
    vec[24] = len(re.findall(return_op, declines))

    vec[25] = len(re.findall(numerical_op, addlines))
    vec[26] = len(re.findall(numerical_op, declines))

    vec[27] = len(re.findall(compare_op, addlines))
    vec[28] = len(re.findall(compare_op, declines))

    vec[29] = len(re.findall(err_op, addlines))
    vec[30] = len(re.findall(err_op, declines))

    vec[31] = len(addlines) - len(declines)

    return vec


def parse_commit(commit_path):
    log('[+] Started parsing ' + commit_path, 'CYAN')
    with open(os.path.join(commit_path, 'patch'), 'r') as pf:
        cnt = pf.read()
        # diff_str = 'diff --git a(/[a-zA-Z0-9_]+)+\.c b(/[a-zA-Z0-9_]+)+\.c'
        # diff_pattern = re.compile(diff_str)

        diff_str = 'diff --git'
        separator = [cnt.index(diff_str)]
        # separator is where "diff --git xxxxx xxxx" separate each file log

        sep = 0
        flag = True
        while flag:
            if cnt.index(diff_str, sep) != cnt.rindex(diff_str):
                sep = cnt.index(diff_str, sep + 1)
                separator.append(sep)
            else:
                if cnt.rindex(diff_str) in separator:
                    flag = False
                else:
                    separator.append(cnt.rindex(diff_str))

        changed_files = len(separator)
        last = separator.pop()
        commit_size = len(cnt)

        diff = cnt[last:commit_size]
        lines = diff.rstrip().split('\n')
        adds = []
        decs = []

        # The first four lines look like:
        # 
        # diff --git a/fs/stat.c b/fs/stat.c
        # index 29c5fe4f8b6..d712a0dfb50f 100644
        # --- a/fs/stat.c
        # +++ b/fs/stat.c
        # 
        # we just start from the fifth line
        for line in lines[4:]:
            if line[0] == '+':
                adds.append(line[1:])
            elif line[0] == '-':
                decs.append(line[1:])

        vec = extract_features(adds, decs)
        vec[0] = changed_files

        success('extract vector from ' + commit_path + ' done!')
        return vec


if __name__ == '__main__':

    def print_help():
        print("This script is used to extract features")
        print("If you have not run extract_cve_patch.py before, run it first.")
        print("OPTIONS:")
        print("  -i/--input <value> Specify the directory of the patches")
        print("  -o/--output <value> Specify the location to write the csv file")
        print("EXAMPLE:\n  $ python extract_cve_patch.py -i ./data/linux/SeP -o ./feature.csv")


    parser = argparse.ArgumentParser(description="script to extract features")
    parser.add_argument('-i', '--input', help="specify the data directory")
    parser.add_argument('-o', '--output', help="specify the output directory to save the csv file")

    args = parser.parse_args()
    if not args.input:
        print_help()
        error('Input dir not specified!')
        exit(-1)
    if not os.path.isdir(os.path.join(os.getcwd(), args.input)):
        print_help()
        exit(-1)

    parse_data(args.input, args.output)
