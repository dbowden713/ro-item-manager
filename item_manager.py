import copy, os
# -------------------------------------
#  Working databases
# -------------------------------------
item_mod = {}
item_base = {}

os.system("title Item Manager")
os.system("cls")

# -------------------------------------
#  Item contains all information about an item.
# -------------------------------------
class Item():
    """
        Holds information about an item.
        
        id_num - the raw ID as read from the data files
        id_str - only the id number, without delimiters
        desc   - the item description, read from data
        name   - the actual item name, read from data
        res    - the resource name for the item sprite
    """
    id_num = ""
    id_str = ""
    desc = ""
    name = ""
    res = ""
    def __init__(self, id_num, description, item_name, resource):
        self.id_num = id_num
        self.desc = desc
        self.name = item_name
        self.res = resource
        self.id_str = self.id_num.replace("#\n", "")
    
    def __str__(self):
        return self.id_str + "\t" + self.name
        
    def __repr__(self):
        return self.__str__()
        
    def view(self):
        """
            Display all of an item's stored information.
        """
        print self.id_str + '\t' + self.name.replace('_', ' ') + '\t' + self.res, '\n'
        desclines = self.desc.split('\n')
        for i in range(len(desclines)):
            if len(str(i)) == 1: space = "   "
            else: space = "  "
            if not desclines[i] in ("", "#", '\n'): 
                if len(desclines[i]) > 75:
                    print str(i) + space + desclines[i][:75].strip() + '\n' + space + " " + desclines[i][75:].strip()
                else: print str(i) + space + desclines[i].strip()
        print ''
        
    def edit(self, flag):
        """
            Add information to the item's description.
            
            /f - "Cooking Ingredient for: LVL10 DEX (5)"
            /s - "SQI Ingredient for: Evangelist (5)
            /u - "Upgrade Ingredient for: Evangelist (800)"
        """
        print "EDITING", 
        self.view()
        if flag == "/f":
            print "Stat: ",
            stat = raw_input().upper()
            if not stat in ("STR", "AGI", "VIT", "DEX", "INT", "LUK"):
                print "Not a vaild stat.  Please try again.\n"
                return False
            print "Level: ",
            level = raw_input()
            if not level in str(range(1, 11)):
                print "Not a valid level. Please try again.\n"
                return False
            print "Amount: ",
            amount = raw_input()
            if not amount.isdigit():
                print "Not a valid amount. Please try again.\n"
                return False
            entry = "^000088Cooking Ingredient for: LVL" + level + " " + stat + " (" + amount + ")" + "^000000"
        if flag == "/s":
            print "SQI: ",
            sqi = raw_input().capitalize()
            print "Amount: ",
            amount = raw_input()
            if not amount.isdigit():
                print "Not a valid amount. Please try again.\n"
                return False
            entry = "^008800SQI Ingredient for: " + sqi + " (" + amount + ")" + "^000000"
        if flag == "/u":
            print "SQI: ",
            sqi = raw_input().capitalize()
            print "Amount: ",
            amount = raw_input()
            if not amount.isdigit():
                print "Not a valid amount. Please try again.\n"
                return False
            entry = "^880088Upgrade Ingredient for: " + sqi + " (" + amount + ")" + "^000000"
        print '\n' + entry + '\n'
        print "Accept? ",
        if not raw_input().lower() in ('y', 'yes'): return False
        
        desclines = self.desc.split('\n')
        
        print "Insert after line: ",
        line = raw_input()
        
        if not line.isdigit() or line not in str(range(len(desclines)-2)):
            print "\nInvalid line number. Please try again.\n"
            return False
            
        self.desc = ""
        for i in range(len(desclines)):
            if str(i-1) == line: self.desc = self.desc + entry + '\n'
            self.desc = self.desc + desclines[i] + '\n'
            
        print '\n' + "DONE" + '\n'
        
        return True

# -------------------------------------
#  Open files for reading/writing
# -------------------------------------
try:
    desc_in = open("idnum2itemdesctable.txt", 'r')
    desc_out = open("idnum2itemdesctable_new.txt", 'w')

    name_in = open("idnum2itemdisplaynametable.txt", 'r')
    name_out = open("idnum2itemdisplaynametable_new.txt", 'w')

    res_in = open("idnum2itemresnametable.txt", 'r')
    res_out = open("idnum2itemresnametable_new.txt", 'w')
except IOError:
    print "Data files missing or incomplete.  Please try again."
    os.system("exit")

# -------------------------------------
#  Read files and populate databases
# -------------------------------------

# Read IDs & descriptions first (most complete list)
file_end = False 
while not file_end:
    desc = ""
    skip = False
    
    desc_end = False
    
    id_num = desc_in.readline()
    if "//" in id_num or not "#" in id_num: skip = True
    if not '\n' in id_num or id_num == "": file_end = True
    
    while not (desc_end or file_end or skip):
        line = desc_in.readline()
        desc += line
        if "#" in line: desc_end = True
        
    if not skip and not file_end:
        if item_base.has_key(id_num.replace("#\n", "")): file_end = True
        if not file_end: item_base[id_num.replace("#\n", "")] = Item(id_num, desc, "NAMEHERE", "RESHERE")
        
# Read item names (2nd most complete)
file_end = False 
while not file_end:
    name = ""
    skip = False
    
    name = name_in.readline()
    if "//" in name or not "#" in name: skip = True
    if not '\n' in name: file_end = True
    
    if not (file_end or skip):
        line = name.split("#")
        name = line[1]
        
    if not skip and not file_end:
        try: item_base[line[0]].name = name
        except KeyError: item_base[line[0]] = Item(line[0], "", name, "RESHERE")
        
# Read item sprite resources
file_end = False 
while not file_end:
    res = ""
    skip = False
    
    res = res_in.readline()
    if "//" in res or not "#" in res: skip = True
    if not '\n' in res: file_end = True
    
    if not (file_end or skip):
        line = res.split("#")
        res = line[1]
        
    if not skip and not file_end:
        try: item_base[line[0]].res = res
        except KeyError: item_base[line[0]] = Item(line[0], "", "", res)
    
# -------------------------------------
#  Main loop - command line
# -------------------------------------
command = [""]

while not command[0] == "exit":
    print ">",
    command = raw_input().lower().strip().split()
    if len(command) == 0: command = " "
    
    if command[0] == "help":
        if len(command) == 1:
            print "For more information on a specific command, type HELP command-name.\n"
            print "CLEAR \t Removes modifications made to an item."
            print "CLS \t Clears the screen."
            print "HELP \t Provides help information for item manager commands."
            print "EDIT \t Opens an item for description and resource editing."
            print "EXIT \t Closes input files and exits the program."
            print "FIND \t Searches for an item."
            print "SAVE \t Writes all changes made to the data files."
            print "MODS \t Lists all modifications in the working database."
            print "VIEW \t Displays all information on an item.\n"
        else:
            command = command[1]
            if command == "help":
                print "Provides help information for item manger commands.\n"
                print "HELP [command]\n"
                print "  command - displays help information on that command\n"
            elif command == "exit":
                print "Closes input files and exits the program.\n"
                print "EXIT\n"
            elif command == "view":
                print "Displays all information on an item."
                print "Any modifications made will be shown.\n"
                print "VIEW [id]\n"
                print "  id\tID number of item.\n"
            elif command == "edit":
                print "Opens an item for description and resource editing."
                print "NOTE: You cannot modify the base ID of an item.\n"
                print "EDIT [id] [/F] [/S] [/U]\n"
                print "  id\tID number of item."
                print "  /F\tAdd food ingredient note to description."
                print "  /S\tAdd SQI ingredient note to description."
                print "  /U\tAdd upgrade ingredient note to description.\n"
            elif command == "clear":
                print "Removes modifications made to an item.\n"
                print "CLEAR [id]\n"
                print "  id\tID number of item.\n"
            elif command == "cls":
                print "Clears the screen.\n"
                print "CLS\n"
            elif command == "mods":
                print "Lists all modifications in the working database.\n"
                print "MODS\n"
            elif command == "find":
                print "Searches for an item.\n"
                print "FIND [keyword]\n"
                print "  keyword\tTerm or terms to search by.\n"
            elif command == "save":
                print "Writes all changes made to the data files.\n"
                print "SAVE\n"
            else:
                print "Invalid command or no help listed.  Please try again.\n"
    elif command[0] == "view":
        if not len(command) == 2: print "Invalid parameters.  Please try again.\n\n"
        else:
            if item_mod.has_key(command[1]): item_mod[command[1]].view()
            elif item_base.has_key(command[1]): item_base[command[1]].view()
            else: print "Invalid key.  Please try again.\n"
    elif command[0] == "edit":
        if not len(command) == 3: print "Invalid parameters.  Please try again.\n"
        else:
            if item_base.has_key(command[1]):
                if command[2] in ("/f", "/s", "/u"): 
                    flag = command[2]
                    item_mod[command[1]] = copy.deepcopy(item_base[command[1]])
                    if not item_mod[command[1]].edit(flag): del item_mod[command[1]]
                else: print "Invalid flag. Please try again.\n"
            else: print "Invalid ID.  Please try again.\n"
    elif command[0] == "clear":
        if not len(command) == 2: print "Invalid parameters.  Please try again.\n"
        elif not item_mod.has_key(command[1]): print "Invalid ID or no mods made.  Please try again.\n"
        else: 
            del item_mod[command[1]]
            print "ID " + command[1] + " restored.\n"
    elif command[0] == "cls":
        os.system('cls')
    elif command[0] == "mods":
        if len(item_mod): 
            for x in item_mod.values(): print x
        else: print "No modifications made yet.\n"
    elif command[0] == "find":
        if len(command) < 2: print "Invalid parameters. Please try again.\n"
        results = 0
        for i in item_base.keys():
            match = True
            for j in command[1:]:
                if not j in item_base[i].name.lower(): 
                    match = False
            if match:
                print str(item_base[i]).replace('_', ' ')
                results += 1
        if results: print '\n' + str(results) + " results.\n"
        else: print "No results.\n"
    elif command[0] == "save":
        list_vals = [int(x) for x in item_base.keys()]
        for i in sorted(list_vals):
            if item_mod.has_key(str(i)):
                if not item_mod[str(i)].desc == "": desc_out.write(item_mod[str(i)].id_num + item_mod[str(i)].desc)
            else: 
                if not item_base[str(i)].desc == "":desc_out.write(item_base[str(i)].id_num + item_base[str(i)].desc)
        desc_out.write("\0")
        desc_in.close()
        desc_out.close()
        os.rename("idnum2itemdesctable.txt", "idnum2itemdesctable.old.txt")
        os.rename("idnum2itemdesctable_new.txt", "idnum2itemdesctable.txt")
        desc_in = open("idnum2itemdesctable.txt", 'r')
        desc_out = open("idnum2itemdesctable_new.txt", 'w')
    elif command[0] == "exit": pass
    else:
        print "Command not found.  Please try again.\n"

# -------------------------------------
#  Close files before exiting
# -------------------------------------
desc_in.close()
desc_out.close()

name_in.close()
name_out.close()

res_in.close()
res_out.close()

os.remove("idnum2itemdesctable_new.txt")
os.remove("idnum2itemdisplaynametable_new.txt")
os.remove("idnum2itemresnametable_new.txt")