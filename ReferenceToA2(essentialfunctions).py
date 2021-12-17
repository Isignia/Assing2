def parse_command_args():
    """
    feature: (x) required ( ) additional
    Description: parse_command_args sets the configuration of argarse module.
    the function configure and parses the following arguments: length, human-readable, max-depth, target. More information can be found in README.md
    the funcion returns an argument object
    """
    parser = argparse.ArgumentParser(description="DU Improved -- See Disk Usage Report with bar charts",epilog="Copyright 2021")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    # add argument for "human-readable". USE -H, don't use -h! -h is reserved for --help which is created automatically.
    # check the docs for an argparse option to store this as a boolean.
    parser.add_argument("-H", "--human-readable", action='store_true', default=False, help="Specify human-readable format")
    # max-depth defines the depth level of du
    parser.add_argument("-d","--max-depth", type=int, nargs=1, help='Specify the depth')
    # add argument for "target". set number of args to 1.
    parser.add_argument("target",nargs='?', type=checker, default=os.path.expanduser('~'), help='Specify a target path')
    args = parser.parse_args()
    return args
    

def percent_to_graph(percent, total_chars):
    '''
    feature: (x) required ( ) additional
    Description: take an percentage and a number of chars and returns a string with bar graph
    '''
    "returns a string: eg. '##  ' for 50 if total_chars == 4"
    yout=int(round(percent/100*total_chars))
    chars='='*yout + ' '*(total_chars-yout)

    return chars

def call_du_sub(location):
    '''
    feature: (x) required ( ) additional
    Description: takes a location argument as a path and returns a list of paths and dir sizes
    '''
    raw = str(subprocess.Popen(["du", "-d", "1", location],stdout=subprocess.PIPE).communicate()[0])
    "use subprocess to call `du -d 1 + location`, rtrn raw list"
    #if debug == True: print(raw)
    list = raw.replace("b'", "",1)
    list = list.replace("'", "",1)
    list = list.replace("\\t","\t")
    list = list.split("\\n")
    if list[-1] ==  '': list.pop()
    return list

def create_dir_dict(raw_dat):
    '''
    feature: (x) required ( ) additional
    Description: "takes the raw list from du_sub and returns a dict {'directory': 0} where 0 is size"
    '''
    dict = {}
    list = raw_dat
    #removes the last element (empty new line)
    for item in list:
        size = [int(n) for n in item.split('\t') if n.isdigit()][0]
        path = [str(n) for n in item.split('\t') if n.isdigit() == False][0]
        dict[path] = size
    
    return dict
