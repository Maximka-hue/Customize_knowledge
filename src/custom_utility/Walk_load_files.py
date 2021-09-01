import os, site
from time import ctime
from sys import path
import multiprocessing as mp
from pprint import pprint


print('Loaded {} from {}'
     .format(__name__ , __file__ [len(os.getcwd()) + 1:]))

def det_pool_size(fn_num, info_count = False, processed_fn = 0, det_process = 100000):
     pool_size = mp.cpu_count()
     while pool_size > 4:
          print("Processed files: ", processed_fn, " & some digit", det_process)
          if processed_fn > det_process:
               break
          elif processed_fn > det_process / 2:
               pool_size -= 1
               det_process = det_process/10
          else:
               pool_size -= 2
               det_process = det_process/100
     if info_count:
          print("Number of processes will be used for ", fn_num, end = "\t")
          print(pool_size)
     return pool_size

def stat_info(item, info_full = True):
     stat_info = os.stat(item)
     if info_full:
          print(' Size:', stat_info.st_size)
          print(' Permissions:', oct(stat_info.st_mode))
          print(' Owner:', stat_info.st_uid)
          print(' Device:', stat_info.st_dev)
          print(" Created"
               " :", ctime(stat_info.st_ctime))
          print(' Last modified:', ctime(stat_info.st_mtime))
          print(' Last accessed:', ctime(stat_info.st_atime))
     else:
          pprint("The File: {:30s} The Size: {:d} Bytes \n".format(item, stat_info.st_size))
          pprint("Located in: ")

def walk_through_files(file_traverse, queue_for_books, queue_for_directories, 
     various_exts, info_output_names = False, 
     only_pdf = False):
     next_name = file_traverse.name
     if info_output_names:
          worker_pid = os.getpid()
          proc_name = mp.current_process().name
          print('Doing something fancy in {}, by process {}, for {}!'.format(proc_name, worker_pid, next_name))
          #if not worker_pid:
          #    print("AAAA OOOuuuOOO")
     if True:  
          is_pdf = os.path.splitext(next_name)[1] == ".pdf"
          extension = os.path.splitext(next_name)[1]
          if info_output_names:
               print("Found extension: ", extension)
          if is_pdf:
               various_exts.update(extension)
          elif only_pdf!= True:
               various_exts.update(extension.lower())
          if extension:
               queue_for_books.put(next_name)
          #elif Path(next_name).is_dir():
          #    queue_for_directories.put(next_name)
          else:
               queue_for_directories.put(next_name)
     # Ждать завершения рабочего процесса
     #queue_for_books.close()
     #queue_for_books.join_thread()

async def main_rename_print_details(dt, dir_traverse, files_path, Books, New_book_with_stat, exts, reg_file, regex_exclude,
     recursion = False, info_output_names = False, renaming = False, apply_regex = False):
     import re
     manager = mp.Manager()
     memorizedPaths = manager.dict()
     queue_for_directories = manager.Queue()
     queue_for_books = manager.Queue()
     jobs = []
     for fn, entry in enumerate(dt):
          if os.path.isfile(entry) and not entry.name.startswith('.'):
     #jobs = np.zeros(pool_size)
     #from time import pause
               p = mp.Process(
                    name = "wrap_file_walk",
                    target= walk_through_files, 
                    args=(entry,  queue_for_books, queue_for_directories, exts, info_output_names))
               #max_workers= pool_size
               p.start()
               jobs.append(p)
               book = queue_for_books.get()
               if recursion:
                    dir_next = queue_for_directories.get()
                    if dir_next:
                         files_path.append(dir_next)
               if info_output_names:
                    print("Retrieved from book queue: " , book)
               book_key = "{}_{}".format(dir_traverse, fn)
               Books[book_key] = book
               New_book_with_stat[book_key] = book.replace(" ", "_").replace("---","-").replace("--","-").replace(",","").replace("__","_").replace("___","_")
               new_path = os.path.normpath(os.path.join(dir_traverse, New_book_with_stat[book_key]))
               old_path = os.path.normpath(os.path.join(dir_traverse, Books[book_key]))
               if renaming:
                    os.rename(old_path, new_path)
               if apply_regex:
                    for ut in regex_exclude:
                         reg_sgn = re.compile(ut)
                         print(reg_sgn, "   ", reg_sgn.search(new_path), " : ",  new_path , ": Before")
                         print("After", reg_sgn.sub(r'', new_path))
               if info_output_names:
                    print(old_path , " will be replaced by: \n \t", new_path)
                    print("Current names that was in directory: ", dir_traverse, " - ", Books[book_key])
          else:
               print("Write func in julia and insert")
     for j in jobs:
          j.join()
          #Books.update(dict_for_books)
          #print(queue_for_books.values())
     else:
          print("Launching synchronously")

def load_path(is_notebook = False):
     #As example, not nessecery at all)
     if is_notebook!= True:
          script_directory = os.path.dirname(__file__ )
          module_directory = os.path.join(script_directory,"src")
          before_len = len(path)
          site.addsitedir(module_directory)
          print('New paths:')
          for p in path[before_len:]:
               print(p.replace(os.getcwd(), '.'))
          for p in site.PREFIXES:
               print(' ', p)
          print('Base: ', site.USER_BASE)
          print('Site: ', site.USER_SITE)
          status = {
          None: 'Disabled for security',
          True: 'Enabled' ,
          False: 'Disabled by command-line option',
          }
          print('Flag: ', site.ENABLE_USER_SITE)
          print('Meaning: ', status[site.ENABLE_USER_SITE] )
import asyncio
async def fill_stats(dir_traverse, Books, New_book_with_stat, Stat_info, exts, info_path= False,info_stat = False, renaming= False):
     for bn in range(len(Books.values())): #Calculate size for all files here. 
          book_key = "{}_{}".format(dir_traverse, bn)
          try:
               if renaming:
                    print(New_book_with_stat[book_key], " : ", bn, " : " , len(New_book_with_stat.values()))
                    stats = os.stat(str(dir_traverse) + "/"+ New_book_with_stat[book_key])
               else:
                    print(Books[book_key], " : ", bn + 1, " : " , len(Books.values()))
                    stats = os.stat(str(dir_traverse) + "/"+ Books[book_key])
          except KeyError:
               print("{}th is directory.".format(book_key))
               continue
          Stat_info[book_key] = stats
          if info_path:
               print("pdf files amount: ", exts)
          if info_stat:
               print("Statistical information: ", end = "\t")
               pprint(Stat_info)
     #if info_count:
     #    print("Processed files: ", new_count)
