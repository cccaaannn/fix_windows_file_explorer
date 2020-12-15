import argparse
import winreg
import json

def edit_reg(keys, key_paths, operation="delete", architecture=64):
    """creates or deletes registry values"""

    if(architecture == 32):
        other_view_flag = winreg.KEY_WOW64_32KEY
    elif(architecture == 64):
        other_view_flag = winreg.KEY_WOW64_64KEY
    else:
        print("unsupported architecture")
        return

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


def main():
    parser = argparse.ArgumentParser(prog = "fix win file explorer")
    parser.add_argument("-o", '--operation', dest='operation', type=str, help='pass create or delete', choices=['create', 'delete'], required=True)
    parser.add_argument("-c", '--cfg_path', dest='cfg_path', type=str, help='config file path', required=False, default="keys.cfg")
    parser.add_argument("-a", '--architecture', dest='architecture', type=int, help='system architecture', required=False, default=64)
    args = parser.parse_args()
    operation = args.operation

    cfg_dict = read_cfg_file(args.cfg_path)

    if(not cfg_dict):
        print("cfg file is broken")
        return
        
    
    keys = cfg_dict["keys"]
    key_paths = cfg_dict["key_paths"]

    # run reg editor
    edit_reg(keys, key_paths, operation=operation, architecture=args.architecture)



if __name__ == "__main__":
    main()