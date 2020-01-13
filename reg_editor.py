import os
import re
from winreg import *
import subprocess

'''
Get all the keys from registry HKCR
"Get-ChildItem -Path Registry::HKCR -Recurse | Select-Object Name | Select -ExpandProperty Name"
'''

def pscommand(cmd, get_output=False):
    if get_output:
        # return subprocess.run(["powershell", cmd], subprocess.STDOUT, shell=True).decode('utf-8')
        output = subprocess.run(["powershell", cmd], capture_output=True, text=True).stdout
        return output

    else:
        subprocess.Popen(["powershell", cmd], subprocess.PIPE)

def string_to_raw_string(string):
    rstring = "%r"%string
    return rstring[1:-1]

def get_regpath(regpath):
    return "Registry::" + regpath.split("::")[-1]

def save_reg_keys(regpath, save_path=None):
    '''
    Examples:
    for HKEY_CLASSES_ROOT use   HKCR or HKEY_CLASSES_ROOT
    for HKEY_CURRENT_USER use   HKCU or HKEY_CURRENT_USER
    for HKEY_LOCAL_MACHINE use  HKLM or HKEY_LOCAL_MACHINE
    for HKEY_USERS use          HKU or HKEY_USERS
    for HKEY_CURRENT_CONFIG use HKCC or HKEY_CURRENT_CONFIG
    '''
    saveFileName = regpath.replace("\\","_")
    saveFileName = saveFileName.split("::")[-1] + "_key.txt"
    if save_path is None:
        saveFileName = os.path.join(os.getcwd(), saveFileName)
    else:
        save_path = os.path.abspath(save_path)
        saveFileName = os.path.join(save_path, saveFileName)
    if os.path.exists(saveFileName):
        # print("Path: " + saveFileName)
        # print("Already exists.")
        return saveFileName
    regpath = get_regpath(regpath)
    cmd = f"Get-ChildItem -Path {regpath} -Recurse | Select-Object Name | Select -ExpandProperty Name > '{saveFileName}'"
    pscommand(cmd)
    return saveFileName

def save_and_get_all_reg_keys(save_path=None):
    '''
    Saves all the keys in the registry in the given path.
    if path not specified files will be saved in directory
    from where the script is executed.
    '''
    HKCR = save_reg_keys("HKCR", save_path=save_path)
    HKCU = save_reg_keys("HKCU", save_path=save_path)
    HKLM = save_reg_keys("HKLM", save_path=save_path)
    HKU = save_reg_keys("HKU", save_path=save_path)
    HKCC = save_reg_keys("HKCC", save_path=save_path)

    return HKCR, HKCU, HKLM, HKU, HKCC


def get_keys_list(keys_file):
    try:
        with open(keys_file, 'r', encoding='UTF-16 LE') as f:
            lines = f.readlines()
            lines = [i.encode(encoding='utf-8').decode(encoding='utf-8')[:-1] for i in lines]
            lines[0] = lines[0][1:]
            return lines
    except:
        print(f"Cannot open file {keys_file}")
        return []


def update_key_data(full_key_path, dtype, value_name, value):
    '''
    Updates the value of given key
    '''
    full_path_list = full_key_path.split('\\')
    root_key = string_to_raw_string(full_path_list[0])
    sub_key = "\\".join(full_path_list[1:])

    if root_key == 'HKEY_CLASSES_ROOT':
        sub_key = string_to_raw_string(sub_key)
        try:
            key = OpenKey(HKEY_CLASSES_ROOT, sub_key, 0, KEY_ALL_ACCESS)
        except:
            print(f'Cannot open Key: {full_key_path}')
            return
        
        SetValueEx(key, value_name, 0, dtype, value)
        CloseKey(key)
        return

    elif root_key == 'HKEY_CURRENT_USER':
        sub_key = string_to_raw_string(sub_key)
        try:
            key = OpenKey(HKEY_CURRENT_USER, sub_key, 0, KEY_ALL_ACCESS)
        except:
            print(f'Cannot open Key: {full_key_path}')
            return

        SetValueEx(key, value_name, 0, dtype, value)
        CloseKey(key)
        return

    elif root_key == 'HKEY_LOCAL_MACHINE':
        sub_key = string_to_raw_string(sub_key)
        try:
            key = OpenKey(HKEY_LOCAL_MACHINE, sub_key, 0, KEY_ALL_ACCESS)
        except:
            print(f'Cannot open Key: {full_key_path}')
            return

        SetValueEx(key, value_name, 0, dtype, value)
        CloseKey(key)
        return

    elif root_key == 'HKEY_USERS':
        sub_key = string_to_raw_string(sub_key)
        try:
            key = OpenKey(HKEY_USERS, sub_key, 0, KEY_ALL_ACCESS)
        except:
            print(f'Cannot open Key: {full_key_path}')
            return
        
        SetValueEx(key, value_name, 0, dtype, value)
        CloseKey(key)
        return

    elif root_key == 'HKEY_CURRENT_CONFIG':
        sub_key = string_to_raw_string(sub_key)
        try:
            key = OpenKey(HKEY_CURRENT_CONFIG, sub_key, 0, KEY_ALL_ACCESS)
        except:
            print(f'Cannot open Key: {full_key_path}')
            return
        
        SetValueEx(key, value_name, 0, dtype, value)
        CloseKey(key)
        return

    else:
        print(f"Path: {full_key_path} not found.")


def get_key_data(full_key_path):
    '''
    Generator functionn which yeilds name, value, type of a given key
    in the order.
    full_key_path ex: 'HKEY_CURRENT_CONFIG\System\CurrentControlSet\Control' type str
    '''
    full_path_list = full_key_path.split('\\')
    root_key = string_to_raw_string(full_path_list[0])
    sub_key = "\\".join(full_path_list[1:])

    if root_key == 'HKEY_CLASSES_ROOT':
        sub_key = string_to_raw_string(sub_key)
        try:
            key = OpenKey(HKEY_CLASSES_ROOT, sub_key, 0, KEY_READ)
        except:
            return

        i=0
        while True:
            try:
                n,v,t = EnumValue(key, i)
                yield n,v,t
                i+=1
            except WindowsError as e:
                break
        CloseKey(key)

    elif root_key == 'HKEY_CURRENT_USER':
        sub_key = string_to_raw_string(sub_key)
        try:
            key = OpenKey(HKEY_CURRENT_USER, sub_key, 0, KEY_READ)
        except:
            return

        i=0
        while True:
            try:
                n,v,t = EnumValue(key, i)
                yield n,v,t
                i+=1
            except WindowsError as e:
                break
        CloseKey(key)

    elif root_key == 'HKEY_LOCAL_MACHINE':
        sub_key = string_to_raw_string(sub_key)
        try:
            key = OpenKey(HKEY_LOCAL_MACHINE, sub_key, 0, KEY_READ)
        except:
            return

        i=0
        while True:
            try:
                n,v,t = EnumValue(key, i)
                yield n,v,t
                i+=1
            except WindowsError as e:
                break
        CloseKey(key)

    elif root_key == 'HKEY_USERS':
        sub_key = string_to_raw_string(sub_key)
        try:
            key = OpenKey(HKEY_USERS, sub_key, 0, KEY_READ)
        except:
            return
        i=0
        while True:
            try:
                n,v,t = EnumValue(key, i)
                yield n,v,t
                i+=1
            except WindowsError as e:
                break
        CloseKey(key)

    elif root_key == 'HKEY_CURRENT_CONFIG':
        sub_key = string_to_raw_string(sub_key)
        try:
            key = OpenKey(HKEY_CURRENT_CONFIG, sub_key, 0, KEY_READ)
        except:
            return
        
        i=0
        while True:
            try:
                n,v,t = EnumValue(key, i)
                yield n,v,t
                i+=1
            except WindowsError as e:
                break
        CloseKey(key)

    else:
        print(f"Path: {full_key_path} not found.")

if __name__ == "__main__":
    pass
