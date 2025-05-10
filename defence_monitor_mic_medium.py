import os
import sys
import subprocess
import argparse


def is_admin():
    """
    Returns True if the script is running with administrative privileges.
    """
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def apply_mic(folder_path):
    """
    Set Mandatory Integrity Control to High on the folder and its descendants.
    """
    print(f"[-] Applying High integrity level to '{folder_path}' (and children)")
    cmd = [
        'icacls',
        folder_path,
        '/setintegritylevel',
        'H',
        '/T'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"[+] Integrity level set to High on: {folder_path}")
    else:
        print(f"[!] Failed to set integrity level. Error:\n{result.stderr.strip()}")


def revert_mic(folder_path):
    """
    Reset Mandatory Integrity Control to Medium (default) on the folder and its descendants.
    """
    print(f"[-] Reverting integrity level to Medium on '{folder_path}' (and children)")
    cmd = [
        'icacls',
        folder_path,
        '/setintegritylevel',
        'M',
        '/T'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"[+] Integrity level reset to Medium on: {folder_path}")
    else:
        print(f"[!] Failed to revert integrity level. Error:\n{result.stderr.strip()}")


def main():
    parser = argparse.ArgumentParser(
        description='Apply or revert Mandatory Integrity Control (MIC) on a folder.'
    )
    parser.add_argument('action', choices=['apply', 'revert'], help='"apply" sets High IL; "revert" resets to Medium IL')
    parser.add_argument('folder', help='Path to target folder')
    args = parser.parse_args()

    folder = args.folder
    if not os.path.isdir(folder):
        print(f"Error: folder not found: {folder}")
        sys.exit(1)

    if not is_admin():
        print("Error: you must run this script as Administrator.")
        sys.exit(1)

    if args.action == 'apply':
        apply_mic(folder)
    else:
        revert_mic(folder)


if __name__ == '__main__':
    main()
