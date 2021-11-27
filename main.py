import shutil
import sys
from shutil import copyfile
from pathlib import Path


sites_to_block = {
    'www.facebook.com', 'facebook.com',
    'www.twitter.com', 'twitter.com'
}
local_host = "127.0.0.1"

def get_os_host_path() -> str:
    Linux_host = '/etc/hosts'
    Mac_host = 'private/etc/hosts'
    Windows_host = r"C:\Windows\System32\drivers\etc\hosts"

    op_sys = sys.platform
    if op_sys == 'win32':
        return Windows_host
    elif op_sys == 'darwin':
        return Mac_host
    elif op_sys == 'linux':
        return Linux_host
    else:
        return 'Error'


def swap_host_file() -> None:
    host_path = get_os_host_path()
    path = Path(host_path)
    print(path)
    try:
        # Check if a backup already exists, will replace the current with the
        # back up if it exists. The other file is deleted
        if Path.is_file(path.parent / "original_hosts"):
            print('exists')
            shutil.move(path.parent / "original_hosts", path.parent / "hosts")
        else:  # Copies the host file as a backup to add block sites
            copyfile(path, path.parent / "original_hosts")

            # Opens the new host file to edit in blocked sites
            f = open(path.parent / "hosts", "a")
            f.write("\n")

            for site in sites_to_block:
                f.write(local_host + "       " + site + "\n")
            f.close()
    except PermissionError:
        print("You do not have permission to modify the hosts file. This program require admin permissions.")
    except FileNotFoundError:
        print("Wrong file or file path")

if __name__ == '__main__':
    swap_host_file()
