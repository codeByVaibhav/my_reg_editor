import re
from tqdm import tqdm
from winreg import *
from reg_editor import *

HKCR, HKCU, HKLM, HKU, HKCC = save_and_get_all_reg_keys()

ALL_KEYS = (get_keys_list(HKCR), get_keys_list(HKCU), get_keys_list(HKLM), get_keys_list(HKU), get_keys_list(HKCC))

search_string = 'text_to_replace'

for KEYS in ALL_KEYS:
    for key in tqdm(KEYS):

        for name, value, dtype in get_key_data(key):

            if dtype in (REG_SZ, REG_EXPAND_SZ):

                if re.search(search_string, value):
                    updated_value = value.replace('text_to_replace', 'updated_text')
                    update_key_data(key, dtype, name, updated_value)
                    print(f"Befor Value: {value}")
                    print(f"After Value: {updated_value}")
                    

            
