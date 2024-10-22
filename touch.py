import os
import argparse
from datetime import datetime

def touch(path, update_only=False):
    """
    Mimics the Linux 'touch' command.
    :param path: Path of the file to create or update.
    :param update_only: If True, only update the file timestamp.
    """
    if os.path.exists(path):
        # Update the file's modified time
        os.utime(path, None)
        print(f"Updated the timestamp of: {path}")
    elif not update_only:
        # Create an empty file
        with open(path, 'a'):
            os.utime(path, None)
        print(f"Created new file: {path}")
    else:
        print(f"File {path} does not exist and `update_only` is set to True.")

def main():
    parser = argparse.ArgumentParser(description="Touch command for Windows")
    parser.add_argument("filename", type=str, help="Name of the file to create or update")
    parser.add_argument("-u", "--update-only", action="store_true", help="Only update the timestamp of the file")
    
    args = parser.parse_args()
    touch(args.filename, args.update_only)

if __name__ == "__main__":
    main()
