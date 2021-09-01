# Python program to rename all file
# names in your directory 
#cd /home/computadormaxim/図書館/ModelingCoding/PracticalProgrammes/Doc_knowledge
#python3 rename_files.py 
# -d /home/computadormaxim/図 書館/BuildStructureMaterials
# -d /home/computadormaxim/図書館/HydroGeologicFlows 
# -d /home/computadormaxim/図書館/BioMedicine 
# -d /home/computadormaxim/図書館/BioMedicine/MartialArts
# -d /home/computadormaxim/図書館/ModelingCoding/ModelAutodeskAnsys
# -d /home/computadormaxim/図書館/Languages
# -d /home/computadormaxim/図書館/PreciseMatika Structures/MechNumerical
# -d /home/computadormaxim/図書館/PreciseMatika Structures/PlasmaCosmos
# -d /home/computadormaxim/図書館/PreciseMatika Structures/MathStructures
import os, sys, re
from site import addsitedir
import numpy as np
from time import time
import multiprocessing as mp
from pprint import pprint
from pathlib import Path
#from pconst import const
from collections import namedtuple, defaultdict
from itertools import chain 
import argparse
from collections import Counter
import subprocess
#import importlib
#import PyInit_fast_traverse_url.double
#moduleName = input('Enter module name:')
#importlib.import_module(moduleName)

#from numba import jit, njit
"""from julia.api import Julia
jl = Julia(compiled_modules=False)
from julia import Main
Main.include("txt_process.ipynb")"""
start_programm_time = time()

import re

prog_loc = r"/home/computadormaxim/図書館/ModelingCoding/PracticalProgrammes/rename_files.py"

def jupyterNotebookOrQtConsole():
    env = 'Unknow'
    cmd = 'ps -ef'
    try:
        with os.popen(cmd) as stream:
            if not py2:
                stream = stream._stream
            s = stream.read()
        pid = os.getpid()
        ls = list(filter(lambda l:'jupyter' in l and str(pid) in l.split(' '), s.split('\n')))
        if len(ls) == 1:
            l = ls[0]
            pa = re.compile(r'kernel-([-a-z0-9]*)\.json')
            rs = pa.findall(l)
            if len(rs):
                r = rs[0]
                if len(r)<14:
                    env = 'qtipython'
                else :
                    env = 'jn'
        return env
    except:
        return env
    
pyv = sys.version_info.major
py3 = (pyv == 3)
py2 = (pyv == 2)
class pyi():
    '''
    python info
    
    plt : Bool
        mean plt avaliable
    env :
        belong [cmd, cmdipython, qtipython, spyder, jn]
    '''
    pid = os.getpid()
    gui = 'ipykernel' in sys.modules
    cmdipython = 'IPython' in sys.modules and not gui
    ipython = cmdipython or gui
    spyder = 'spyder' in sys.modules
    if gui:
        env = 'spyder' if spyder else jupyterNotebookOrQtConsole()
    else:
        env = 'cmdipython' if ipython else 'cmd'
    
    cmd = not ipython
    qtipython = env == 'qtipython'
    jn = env == 'jn'
    
    plt = gui or 'DISPLAY' in os.environ 

script_directory = os.path.dirname(__file__)
module_directory = os.path.join(script_directory,"src")
addsitedir(module_directory)
from Walk_load_files import main_rename_print_details,\
    load_path, det_pool_size, fill_stats
from apply_regex_search import remove_libname, before_ext_lib, after_ext, regex_exclude

def Constants(Name, *Args, **Kwargs):
    t = namedtuple(Name, chain(Args, Kwargs.keys()))
    return  t(*chain(Args, Kwargs.values()))

# define dictionary
NAME_INFO = Constants('books_InfoAdd', 
                        my_comp = True, #Default True
                        ditem_path = False, 
                        dstat_info = False,
                        in_rust = True, #Default True
                        counting = True,#Default True
                        additional_output_names = False,
                        renaming = False,
                        apply_regex = True,
                        test = False)
DELETE_PATHS = Constants('DeletablePatterns', 
    zero = 0,
    lib= 1,
    z= 2)
#print(DEL_PATS.lib)
#@njit
def default_char():
    return DELETE_PATHS.zero

rename_parser = argparse.ArgumentParser(description='Short sample rename',
                    fromfile_prefix_chars=r"@")
#So -mc to take my path(or someone who will rename it without use of -d key): prog_loc
#-d is the directory in which to rename files 
#-i print additional info
#-r recursion to the end of nested directories 
#-p rename only pdf files 
#-y choose your formats to rename
rename_parser.add_argument('-s', action='store',
    dest='say_smth',
    help= 'Store smth you want to say')
rename_parser.add_argument('-mc', action='store_true',
                    default= False,
                    dest='my_computer',
                    help='Set a switch to true')
rename_parser.add_argument('-rg', "--apply_regex", action='store_true',
                    default= False,
                    dest='apply_regex',
                    help='Set a switch to true')
rename_parser.add_argument('-i', "--add_info", action='store_true',
                    default= False,
                    dest='additional_info',
                    help='Set a switch to recurse nested directories')
rename_parser.add_argument('-r',"--recursion", action='store_true',
                    default= False,
                    dest='recursion',
                    help='Set a switch to true')
rename_parser.add_argument('-p', action='store_true',
                    default= False,
                    dest='only_pdf',
                    help='Set a switch to true')
rename_parser.add_argument('-d', action='append',
                    dest='name_directories',
                    default= [],
                    type= str,
                    help='Add directories you wish to rename to a list')
text_process = argparse.ArgumentParser(parents=[rename_parser],
                                        add_help= False,
                                        prog= 'text_process',
                                        description="All info will be saved in txt format  "
                                            "to be processed"
                                            "and save some possible names in case "
                                            "of default not corresponding ones")

rename_args , unknown = rename_parser.parse_known_args() 
say = rename_args.say_smth
print("Passed arguments are: ",)
pprint(rename_args)
print("Say: ", end = "\t")
pprint(say)
only_pdf = rename_args.only_pdf
recursion = rename_args.recursion
rename_dirs = rename_args.name_directories
my_comp = True if rename_args.my_computer else NAME_INFO.my_comp
info_stat = True if rename_args.additional_info else NAME_INFO.dstat_info
info_path = True if rename_args.additional_info else NAME_INFO.ditem_path
info_count = True if rename_args.additional_info else NAME_INFO.counting
info_output_names = True if rename_args.additional_info else NAME_INFO.additional_output_names
in_rust = NAME_INFO.in_rust 
testing = NAME_INFO.test
renaming = NAME_INFO.renaming
rust_from_python = True
apply_regex = True if rename_args.apply_regex else NAME_INFO.apply_regex
#all_rename_dirs = parser[name_directories]
is_notebook = (pyi.env == "jn" or pyi.env == "Unknow")
files_path = []

if info_path:
    print("Now using envirenment: ", pyi.env)
if is_notebook and in_rust and my_comp:
    process_direc =  Path(prog_loc).resolve(strict=True).parent.parent.parent
elif is_notebook and my_comp:
    process_direc =  Path(prog_loc).resolve(strict=True).parent.parent
else:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print("Python programm is located in: \n", dir_path)
    if in_rust:
        process_direc = Path(dir_path).parent.parent
    else:
        process_direc = Path(dir_path).parent
    #temp_file = os.path.join(dir_path, "hyplinks.txt")

try:
    if len(rename_dirs)!= 0 and my_comp:
        rename_dirs.append(str(process_direc))
        files_path = rename_dirs
    elif len(rename_dirs)!= 0:
        files_path = rename_dirs
    elif my_comp:
        files_path = [str(process_direc)]
        print(Path(__file__).resolve().parent.parent, " = ? ", process_direc)
    else:
        pprint("You need to indicate path to your book store!")
        exit()
except FileNotFoundError:
    pass


if info_path:
    load_path(is_notebook)
#files_path= [str(files_path)] if my_comp else files_path
if info_path:
    print('Python Envronment is %s' % pyi.env)
    print("Passed directories that will be processed: ")
    pprint(files_path)


print("Path at terminal when executing this file")
print(os.getcwd() + "\n")

if info_path:
    dirsn = len(files_path)
    print("Passed directories amount: ", dirsn)


#completed = subprocess.run(['ls', '-1'])
#print('returned code:', completed.returncode)
#completed = subprocess.run('echo $HOME', shell=True)
#print('returned code:', completed.returncode )
#@jit(int32, int32)
#from copy import deepcopy
from asyncio import get_event_loop, all_tasks, gather, run as run_asyncio
loop = get_event_loop()

import pathlib
import linecache
#linecache.getline(filename, 5)

reg_coincidence = pathlib.Path('regular_coincidence.txt')

def fill_dirs_with_dictfiles(reg_coincidence, regex_exclude, files_path = [], info_item = False, apply_regex = False):
    #x = np.zeros((max(2, ),2), dtype=[('Number_of_files_and_directories', np.int32)])
    fn_num = {}
    fd_num = {}
    Books = {}
    New_book_with_stat = {}
    Path_and_new_names = {}
    Stat_info = dict()
    exts = Counter()
    #print(os.scandir(Path(files_path[0])))
    for ind_fp, fp in enumerate(files_path):
        print(str(fp), "will be", ind_fp + 1, "th directory\n")
        with os.scandir(fp) as fi:
            if info_path:
                print("Directory: ", fp)
            if rust_from_python:
                print("Execute rust from python.")

            processed_fn = 0
            processed_dn = 0
            processed_sl = 0
            processed_unk = 0
            for entry in fi:
                if info_item:
                    print("File: ", entry, "  ", Path(entry).is_file())
                if entry.is_dir():
                    typ = "dir"
                    processed_dn += 1
                elif entry.is_file():
                    typ = 'file'
                    processed_fn += 1
                elif entry.is_symlink():
                    typ = "link"
                    processed_sl += 1
                else:
                    typ = "’unknown’"
                    processed_unk += 1
            print(processed_fn, "+", processed_dn, "=? ", eval("processed_fn + processed_dn"))
            fn_num.update({str(fp)+"_files": processed_fn})
            fd_num.update({str(fp)+"_directories": processed_dn})

    for ind_fp, dir_traverse in enumerate(files_path):
        print("Traversing directory?: ", Path(dir_traverse).is_dir())
        #num_files = fn_num[ind_fp]
        loop = get_event_loop()
        pool_size = det_pool_size(fn_num, processed_fn = processed_fn, info_count = info_count)
        with os.scandir(dir_traverse) as dt:
            with reg_coincidence.open('w', encoding='utf-8') as handle:
                task_with_details = loop.create_task(
                    main_rename_print_details(dt, dir_traverse, files_path, Books, New_book_with_stat, exts,
                        reg_file = reg_coincidence, regex_exclude = regex_exclude, apply_regex = apply_regex))
            loop.run_until_complete(task_with_details)
        Path_and_new_names[dir_traverse] = New_book_with_stat
        task_stats = loop.create_task(
            fill_stats(dir_traverse, Books, New_book_with_stat, Stat_info, exts,
            info_path = info_path, info_stat = info_stat, renaming = renaming))
        loop.run_until_complete(task_stats)
        pending = all_tasks(loop=loop)#Tasks return
        for task in pending:
            task.cancel()
        group = gather(*pending, return_exceptions=True)
        loop.run_until_complete(group)
        loop.close()
        #if info_count:
        #    print("Processed files: ", new_count)
        new_count = len(fn_num.values())
#________________________________________________________________
    if info_path:
        print("Return directories for renaming: ", files_path)
    try:
        book_items = Books.items()
        stat_len = len(Stat_info.items())
        #New_book_with_stat = dict((Stat_info[key], value) for (key, value) in book_items)#if int(Stat_info[value]) < min(len(book_items), stat_len))
        New_book_with_stat = rekey(New_book_with_stat, Stat_info)
    except KeyError as err:
        print("{}th the last file, continue ... {} ^ {}".format(err, len(book_items), stat_len))
    if info_output_names:
        print("New fresh dictionary: ")
        pprint(New_book_with_stat)
    return Path_and_new_names
##################################################################
def rekey(inp_dict, keys_replace):
        return {v : keys_replace.get(k, k) for k, v in inp_dict.items()}
"""                          
def editbook(request, book_id):
    log.debug("test....")
    author = Author.objects.filter(author_id= author_info.author_id)
    books=Book.objects.filter(book_id=book_id)
    if request.POST:
        book_name =request.POST['book_name']
        publisher_name =request.POST['publisher_name']
        books=Book.objects.filter(book_id=book_id).update(book_name=book_name, publisher_name=publisher_name)
        first_name = request.POST('first_name')
        last_name = request.POST('last_name')
        email = request.POST('email')
        age = request.POST('age')

        author_info = Author.objects.latest('author_id')
        log.debug("test:%s",author_info.author_id)
        author = Author.objects.filter(author_id=author_info.author_id).update(first_name = first_name,last_name = last_name,email=email,age=age)
        return redirect('/index/')
    else:
        books = Book.objects.get(pk=book_id)
        return render_to_response('editbook.html',{'books':books},{'author':author},context_instance=RequestContext(request))
time_to_convert = time()
            fn_num = np.array(fn_num)
            fd_num = np.array(fd_num)
            end_time_to_convert = time()
            if info_count:
            print("Convert to ndarray in: ",
            end_time_to_convert - time_to_convert)
if info_output_names:
                        print("{name} {typ}".format(
                        name=entry.name,
                        typ=typ,
                        file = "out_names.txt"))
        fill_dirs_with_dictfiles(files_path, info_item)
        #for books in all_dirs:
            #remove_libname(files = books, before_ext_lib= before_ext_lib, after_ext= after_ext)
    for word, count in various_exts.most_common():
            print(word, count)
    return (all_dirs, new_count)"""
    
#%timeit dirs = fill_dirs_with_dictfiles(files_path, info_item)
#if not os.path.exists(fn):
#    os.makedirs(fn)
#if __ name__ == '__ main__' :
Book_collection = {}
Paths_to_current_names = {}
if testing:
    import profile
    Book_collection = profile.run("fill_dirs_with_dictfiles(files_path, info_item = info_stat) ")
else:
    """    jobs = []
    p = mp.Process(
                            name = "wrap_file_walk",
                            target= walk_through_files, 
                            args=())
                            #max_workers= pool_size
    p.start()
    jobs.append(p)
    for j in jobs:
        j.join()
    """
    Book_collection = fill_dirs_with_dictfiles(reg_coincidence, regex_exclude, files_path, info_item = info_stat, apply_regex = apply_regex)
    #pprint(directories)
"""    for ind_fp, book_name, book_statistic in enumerate(Book_collection):
        print(book_name)
        
        os.rename(item_path, item_path
            .replace(" ", "_"))
            #.replace("---","-")
                #.replace("--","-")
                #.replace(",","")
                #.replace("__","_")
                #.replace("___","_"))"""
"""
            #if not_at_the_end .replace(".","_")
                if info_list:
                    ("After \n", item_path)
                for regex, i in regexes_remove.items():
                    regex = re.compile(regex)
                if regex.search(item_path):
                    pprint("The File: {:30s} match pattern {:d} \n" 
                        .format(item_path, regex.value))"""

end_programm_time = time()
print(end_programm_time - start_programm_time)



#fast_traverse_url.double(9)
"""from time import sleep
from concurrent import futures
import threading
ti = time()
def task(n):
    print("{}: sleeping {}".format(
    threading.current_thread().name,
        n)
)
    sleep(n / 10)
    print('{}: done with {}'.format(
    threading.current_thread().name,
        n)
)
    return n / 10

ex = futures.ThreadPoolExecutor(max_workers=8)
print('main: starting')
f = ex.submit(task, 5)
print("main: unprocessed results {}".format(f))
print("main: waiting for real results")
result = f.result()
print("main: results: {}".format(result))
te = time()
print(te - ti)"""

def change_dictionary_key_name(dict_object, old_name, new_name):
    '''
    [PARAMETERS]: 
        dict_object (dict): The object of the dictionary to perform the change
        old_name (string): The original name of the key to be changed
        new_name (string): The new name of the key
    [RETURNS]:
        final_obj: The dictionary with the updated key names
    Take the dictionary and convert its keys to a list.
    Update the list with the new value and then convert the list of the new keys to 
    a new dictionary
    '''
    keys_list = list(dict_object.keys())
    for i in range(len(keys_list)):
        if (keys_list[i] == old_name):
            keys_list[i] = new_name

    final_obj = dict(zip(keys_list, list(dict_object.values()))) 
    return final_obj
os.system('date; (sleep 3; date)&')