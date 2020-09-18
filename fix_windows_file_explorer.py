import argparse
import platform
import winreg
import json

def edit_reg(keys, key_paths, operation="delete"):
    """creates or deletes registry values"""
    # get system info
    bitness = platform.architecture()[0]
    if(bitness == '32bit'):
        other_view_flag = winreg.KEY_WOW64_64KEY
    elif(bitness == '64bit'):
        other_view_flag = winreg.KEY_WOW64_32KEY

    for key in keys:
        for index, key_path in enumerate(key_paths):
            try:
                opened_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, access = (winreg.KEY_READ | other_view_flag))
                if(operation == "delete"):
                    winreg.DeleteKey(opened_key, keys[key])
                elif(operation == "create"):
                    winreg.CreateKey(opened_key, keys[key])
                else:
                    print("operation {0} is not supported available operations create, delete".format(operation))
                    return
                print("key: {0} - {1} \t found -> {2}".format(key, index+1, operation))
            except FileNotFoundError:
                print("key: {0} - {1} \t not found".format(key, index+1))

def read_cfg_file(path):
    try:
        with open(path,"r") as file:
            d = json.load(file)
        return d
    except:
        return 0


def main(cfg_path = "keys.cfg"):
    parser = argparse.ArgumentParser(prog = "fix win file explorer")
    parser.add_argument("-o", '--operation', dest='operation', type=str, help='pass create or delete', choices=['create', 'delete'], required=True)
    parser.add_argument("-c", '--cfg_path', dest='cfg_path', type=str, help='config file path', required=False)
    args = parser.parse_args()
    operation = args.operation

    if(args.cfg_path):
        cfg_path = args.cfg_path
    cfg_dict = read_cfg_file(cfg_path)

    if(not cfg_dict):
        print("cfg file is broken")
        return
        
    keys = cfg_dict["keys"]
    key_paths = cfg_dict["key_paths"]

    # run reg editor
    edit_reg(keys, key_paths, operation=operation)



if __name__ == "__main__":
    main()