#!/usr/bin/env python3

import subprocess, sys
import os
import argparse

def parse_command_args():
    '''
    Description: parse_command_args sets the configuration of argarse module.
    the function configure and parses the following arguments: length, human-readable, max-depth, target. More information can be found in README.md
    the funcion returns an argument object
    '''
    parser = argparse.ArgumentParser(description="DU Improved -- See Disk Usage Report with bar charts",epilog="Copyright 2021")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    parser.add_argument("-H", "--human-readable", type=bool, default=False, help="print sizes in human readable format (e.g. 1K 23M 2G)")
    parser.add_argument("target", type=str, help="The directory to scan.")
    args = parser.parse_args()
    return args

def percent_to_graph(percent, total_chars) -> str:
    '''
    Description: take an percentage and a number of chars and returns a string with bar grap
    '''
    if percent < 0 or percent > 100:
        raise ValueError("Invalid percent")
    bar_percent = (percent / 100) * total_chars
    percent_dd = total_chars - bar_percent
    bar_chars = ("=" * int(bar_percent)) + (" " * int(round(percent_dd)))
    return bar_chars

def call_du_sub(location):
    '''
    Description: takes a location argument as a path and returns a list of paths and dir sizes
    '''
    p = "du -d 1 " + location
    raw_list = subprocess.Popen(p, shell=True, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
    f = open('./list.txt', 'w+')
    f.write(raw_list)
    f.close()
    f = open('./list.txt', 'r')
    return f.read().splitlines()

def create_dir_dict(raw_dat):
    '''
    Description: "takes the raw list from du_sub and returns a dict {'directory': 0} where 0 is size"
    '''
    dict = {}
    list = raw_dat
    for item in list:
        value, path = str(item).split('t')
        dict[path] = int(value)
    return dict    


if __name__ == "__main__":
    args = parse_command_args()
    location = args.target
    usage_list = call_du_sub(location)
    usage_dict = create_dir_dict(usage_list)
