from pathlib import Path
import os
current_path = Path(__file__)
def get_ouput_audio():
    c_path = current_path
    x_path = os.path.join(str(c_path), 'output', 'audio')
    my_file = Path(x_path)
    con = 0
    while not my_file.exists():
        if con > 3:
            break
        c_path = c_path.parent
        x_path = os.path.join(str(c_path), 'output', 'audio')
        my_file = Path(x_path)
        con += 1
    return str(my_file)