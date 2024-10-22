import os
import argparse
import re
from datetime import datetime

def expand_wildcards(filename_pattern):
    """
    Expands wildcards like {1...5}.txt to a list of filenames [1.txt, 2.txt, ..., 5.txt].
    Supports ranges in the format {start...end}.
    """
    match = re.search(r'{(\d+)\.\.\.(\d+)}', filename_pattern)
    if match:
        start, end = int(match.group(1)), int(match.group(2))
        return [re.sub(r'{\d+\.\.\.\d+}', str(i), filename_pattern) for i in range(start, end + 1)]
    return [filename_pattern]  # No expansion needed

def set_time(path, access_time=None, modification_time=None):
    """Set custom access and modification times for a file."""
    os.utime(path, (access_time, modification_time))

def touch(path, no_create=False, access_only=False, mod_only=False, custom_time=None, verbose=False):
    """
    Mimics the Linux 'touch' command with additional features.
    :param path: Path of the file to create or update.
    :param no_create: Do not create file if it doesn't exist.
    :param access_only: Modify access time only.
    :param mod_only: Modify modification time only.
    :param custom_time: Custom time for access and modification in the format YYYYMMDDHHMM.
    :param verbose: Display detailed information about actions.
    """
    if not os.path.exists(path):
        if no_create:
            if verbose:
                print(f"File {path} does not exist, and --no-create is set. Skipping file.")
            return
        with open(path, 'a'):
            os.utime(path, None)
        if verbose:
            print(f"Created new file: {path}")
    
    current_time = datetime.now().timestamp()
    
    if custom_time:
        custom_time = datetime.strptime(custom_time, "%Y%m%d%H%M").timestamp()
    
    if access_only:
        if verbose:
            print(f"Updating access time of {path}")
        set_time(path, access_time=custom_time or current_time, modification_time=None)
    elif mod_only:
        if verbose:
            print(f"Updating modification time of {path}")
        set_time(path, access_time=None, modification_time=custom_time or current_time)
    else:
        if verbose:
            print(f"Updating access and modification times of {path}")
        set_time(path, access_time=custom_time or current_time, modification_time=custom_time or current_time)

def main():
    parser = argparse.ArgumentParser(description="Enhanced 'touch' command for Windows with support for wildcards and additional options.")
    
    # Adding arguments
    parser.add_argument("filenames", type=str, nargs='+', help="Name(s) of the file(s) to create or update. Supports ranges like {1...5}.txt")
    parser.add_argument("-a", "--access-time", action="store_true", help="Only update the access time")
    parser.add_argument("-m", "--modification-time", action="store_true", help="Only update the modification time")
    parser.add_argument("-c", "--no-create", action="store_true", help="Do not create files if they do not exist")
    parser.add_argument("-t", "--time", type=str, help="Set a custom time for access and modification in the format YYYYMMDDHHMM")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode, display detailed info about actions")
    
    args = parser.parse_args()

    for filename_pattern in args.filenames:
        filenames = expand_wildcards(filename_pattern)
        for filename in filenames:
            touch(filename, no_create=args.no_create, access_only=args.access_time, 
                  mod_only=args.modification_time, custom_time=args.time, verbose=args.verbose)

if __name__ == "__main__":
    main()
