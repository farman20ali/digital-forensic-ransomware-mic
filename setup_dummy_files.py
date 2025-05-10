#!/usr/bin/env python3
import os
import argparse
import random
import string
from pathlib import Path

def random_text(size=1024):
    return ''.join(random.choices(string.ascii_letters + string.digits + ' \n', k=size))

def create_text_file(path, size_kb=1):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(random_text(size_kb * 1024))

def create_binary_file(path, size_kb=10):
    with open(path, 'wb') as f:
        f.write(os.urandom(size_kb * 1024))

def main():
    parser = argparse.ArgumentParser(
        description="Generate a variety of dummy files for ransomware testing"
    )
    parser.add_argument(
        '--target', '-t',
        default='test_files',
        help='Directory to create files in (will be made if missing)'
    )
    parser.add_argument(
        '--count', '-c',
        type=int,
        default=50,
        help='Total number of files to generate'
    )
    args = parser.parse_args()

    target_dir = Path(args.target)
    target_dir.mkdir(parents=True, exist_ok=True)

    extensions = {
        '.txt': lambda p: create_text_file(p, size_kb=random.randint(1, 5)),
        '.csv': lambda p: create_text_file(p, size_kb=random.randint(1, 5)),
        '.pdf': lambda p: create_binary_file(p, size_kb=random.randint(5, 20)),
        '.zip': lambda p: create_binary_file(p, size_kb=random.randint(1, 10)),
        '.jpg': lambda p: create_binary_file(p, size_kb=random.randint(10, 50)),
    }
    honeypots = ['NTUSER.DAT', 'bootmgr', 'important.sys', 'runme.bat']

    print(f"\n[*] Creating {args.count} random files in '{target_dir}/'...\n")
    for i in range(1, args.count + 1):
        ext = random.choice(list(extensions.keys()))
        fname = f"file_{i:03d}{ext}"
        path = target_dir / fname
        extensions[ext](path)
        print(f"  [+] {fname}")

    print("\n[*] Adding honeypot files (zero-byte)...\n")
    for name in honeypots:
        path = target_dir / name
        path.write_bytes(b'')
        print(f"  [!] Honeypot: {name}")

    print("\n✅ Done! Your test folder is ready.")

if __name__ == '__main__':
    main()
