import plistlib
import psutil
import tkinter as tk
from tkinter import filedialog, messagebox

def bytes_to_hex_string(b):
    return ' '.join(f'{byte:02X}' for byte in b)

def check_amd_vanilla_patches(plist_path):
    try: 
        with open(plist_path, 'rb') as f:
            plist = plistlib.load(f)

        core_count = psutil.cpu_count(logical=False)

        expected_replace_values = [
            b'\xB8' + core_count.to_bytes(1, 'little') + b'\x00\x00\x00\x00',    # 1st patch (0)
            b'\xBA' + core_count.to_bytes(1, 'little') + b'\x00\x00\x00\x00',    # 2nd (1)
            b'\xBA' + core_count.to_bytes(1, 'little') + b'\x00\x00\x00\x90',    # 3rd (2)
            b'\xBA' + core_count.to_bytes(1, 'little') + b'\x00\x00\x00',        # 4th (3)
        ]

        kernel_patches = plist.get('Kernel', {}).get('Patch', [])

        correct_patches = True
        for i, patch in enumerate(kernel_patches[:4]):
            replace_value = patch.get('Replace')
            expected_value = expected_replace_values[i]

            if replace_value != expected_value:
                print(f"Patch {i} has an incorrect Replace value: {bytes_to_hex_string(replace_value)}. Expected: {bytes_to_hex_string(expected_value)}")
                correct_patches = False
            else:
                print(f"Patch {i} has the correct Replace value.")

        if correct_patches:
            messagebox.showinfo("Result", "All patches have the correct Replace values.")
        else:
            messagebox.showerror("Result", "Some patches have incorrect Replace values.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def open_file_dialog():
    root = tk.Tk()
    root.withdraw() 
    file_path = filedialog.askopenfilename(
        title="Select config.plist file",
        filetypes=(("Plist files", "*.plist"), ("All files", "*.*"))
    )
    if file_path:
        check_amd_vanilla_patches(file_path)

if __name__ == "__main__":
    open_file_dialog()
