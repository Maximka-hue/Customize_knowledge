import re
from pprint import pprint
#python3 src/FPython/apply_regex_search.py

ext_lib = ["z_lib", "org",
        "github", "_PDFDrive"]
def lib_del(matchobj, libname):
    for exl in ext_lib:
        if (matchobj.group(libname).find("{exl}".format(exl = exl)) == 1):
            return ''
        else: return '_'

z_lib = "Advanced_Raspberry_Pi_Raspbian_Linux_and_GPIO_Integration_by_Warren_Gay_(z_lib.org).pdf"
pdf_drive = "Handbook_of_Statistical_Analysis_and_Data_Mining_Applications_(_PDFDrive_).pdf"
defice = "The_OpenCL_™_C++_.pdf"
excess = "C#，。net.pdf"

files = [z_lib, pdf_drive, defice, excess]

NAME_DEF = "(?:\w+[-_,#]*?)+?"
INCLUDED_IN_NAME = "(?:\w+[-_,#]+?[a-zA-Z0-9]+)"
before_ext_lib = re.compile(r"""^(?P<simple_name> {main_name})[-_, #]*?          #Any name of book
            (  \(  )(?P<library_name>[w_,-~`\#]*?)(?(2)\)|\.?)(.\w+?$)    #all that will begin with parentheses                  """.format(main_name = NAME_DEF), #            #(   \[  )(?:[w_,-~`\#]*?)  (?(3)\]|\.\w+?$)            | 
                                                    #(   \{  )(?:[w_,-~`\#]*?)  (?(4)\}|\.\w+?$)               
            flags = re.MULTILINE | re.VERBOSE)#(?P<simple_name>\w+)+(.?lib.*?\.)(?P<date_published>\d{3:8})*
#after_ext = re.compile("(?P<name>.+?)(?P<sgn>(?<=[-\_,#]))(?P<ext>\.\w+)$")
after_ext = re.compile("(?P<name>{main_name}+?)(?P<sgn>[_.,|`'!+=]*)(?P<ext>\.\w+)$".format(main_name = INCLUDED_IN_NAME))
add_dot = re.compile("(?P<name>.*?)\.+?[-#,.~]*(?<=[-\_,])(?P<ext>\.\w+)$")
name_library = "(?P<name>{})[_ ](?P<brackets>(?=\(.*?\)))(?P<Library_name>.*?lib.*?)(?(brackets)(?P<end>\))|\w*?)".format(NAME_DEF)
pz = "(\.\W+)?([ A.]?z-[A.]*?\.)"
defice = re.compile("__+")
regex_exclude = ["dokumen", "pub", "net", 
    "™", "PDFDrive", "org", "z_lib", "Password_Removed",
    add_dot, plib, pz, defice]
#print("MM", fnmatch.filter(files, plib))

for i, file in enumerate(files):
        for reg in regex_exclude:
            reg_sgn = re.compile(reg)
            if reg_sgn.search(file):
                print("{:<10}".format(str(reg)), "   ", "{:<14}".format(repr(reg_sgn.search(file))), " : ",  "{:<18} : Before".format(file))
                print("After", reg_sgn.sub(r'', file))

def remove_libname(files, before_ext_lib = before_ext_lib, after_ext = after_ext):
    for fn in files:
        m = re.search(before_ext_lib, fn)
        if m == None:
            print("book ", end = "\t")
            pprint(fn)
            continue
        else:
            print("Name of file: ", m.group('simple_name').replace("_", " "), "", sep='')
            print("Will remove: ", m.group(2),  m.group("library_name"), ")", sep='')
            new_fn = "{}{}".format(m.group('simple_name'), m.group(4))
            print(new_fn)
            mm = re.search(after_ext, new_fn)
            if mm == None:
                pass
            else: 
                print("Additional excessive symbol before extension: ", mm.group("sgn"), "\n", sep='')
            fn = "{}L{}{}".format(mm.group("name"), 
                mm.end("ext") + 1 + len(str(mm.end("ext"))), mm.group("ext"))
            print("So new name will be: ", fn, "\n")
#remove_libname(files, before_ext_lib = before_ext_lib, after_ext = after_ext)
