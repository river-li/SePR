import os
import argparse
import numpy as np
import pandas as pd
from model.preprocessing import parse_patch
from util.pretty_print import error, log

def parse_commit(csv_path, flag=True):
    csv_path = os.path.abspath(csv_path)

    df = pd.read_csv(csv_path)

    if flag:
        del (df['Unnamed: 0'])

    nsep = df.loc[df['vulnerability'] == 0]
    sep = df.loc[df['vulnerability'] == 1]

    sep_commit = sep['commit_msf']
    nsep_commit = nsep['commit_msf']

    return sep_commit, nsep_commit

def parse_csv(csv_path,flag=True):
    # qemu.csv need to delete a line
    # while ffmpeg.csv doesn't need to do this
    csv_path = os.path.abspath(csv_path)

    df = pd.read_csv(csv_path)

    if flag:
        del (df['Unnamed: 0'])

    nsep = df.loc[df['vulnerability'] == 0]
    sep = df.loc[df['vulnerability'] == 1]

    sep_vec = []
    nsep_vec = []

    sep_diff = sep['patch']
    nsep_diff = nsep['patch']

    for cnt in sep_diff:
        sep_vec.append(parse_patch(cnt))

    for cnt in nsep_diff:
        if type(cnt)!=str:
            continue
        nsep_vec.append(parse_patch(cnt))
    # there is a bad data in qemu.csv:
    #
    # print(df.loc[2179]['commit_msg']
    # Standard project directories initialized by cvs2svn. git-svn-id: svn://svn.savannah.nongnu.org/qemu/trunk@1c046a42c-6fe2-441c-8c8c-71466251a162&&&&
    #
    # print(df.loc[2179]['patch']
    # nan

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

    sep_df = pd.DataFrame(sep_vec, columns=columns, dtype=np.int)
    nsep_df = pd.DataFrame(nsep_vec, columns=columns, dtype=np.int)

    return sep_df, nsep_df


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="script to extract features from samples given by SPI")
    parser.add_argument('-i', '--input', help="given csv file path")
    parser.add_argument('-o', '--ouput', help="specify the target directory to save parsed features")

    args = parser.parse_args()

    if not args.input:
        error("No input file")
        exit(-1)

    output = os.path.abspath(args.output)
    if not os.path.isdir(os.path.join(os.getcwd(), args.output)):
        output = os.getcwd()
        log("[-] Output directory Not Valid, use current directory temporarily", "PURPLE")

    sep, nsep = parse_csv(args.input)
    sep.to_csv(os.path.join(output, 'sep.csv'))
    nsep.to_csv(os.path.join(output, 'nsep.csv'))

    log("[+] Successfully saved file: " + os.path.join(output, 'sep.csv'), "PURPLE")
    log("[+] Successfully saved file: " + os.path.join(output, 'nsep.csv'), "PURPLE")
