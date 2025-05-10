 # Python Ransomware Simulation & Windows Integrity Level Protection Demo

🛡️ This repository shows how to simulate a simple Python-based “ransomware” attack and how Windows Mandatory Integrity Control (MIC) can block untrusted processes from modifying protected files when the folder’s integrity level is set to High (or Medium). All steps are performed inside a Windows 10 VM for safe, repeatable testing.

🎥 Watch the full video walkthrough here: [Windows Integrity Level Ransomware Demo](https://www.youtube.com/watch?v=dQw4w9WgXcQ)

---

## 📆 Software & Tools Used

| Tool                              | Version / Notes                 |
| --------------------------------- | ------------------------------- |
| Windows 10 VM                     | 21H2                            |
| Python                            | 3.8+                            |
| cryptography, watchdog, psutil    | Latest via `pip install`        |
| PyInstaller                       | Latest (optional, for bundling) |
| Windows built-in `icacls` utility | For setting integrity levels    |
| Hypervisor                        | Hyper-V / VMware (optional)     |

---

## 🧪 Project Structure

```
IntegrityLevelDemo/
├── setup_dummy_files.py        # Generates dummy files in a target folder
├── trojan.py                   # “Ransomware” script that encrypts files
├── mandatory_control_level.mp4 # "vidoes" for demo
├── defence_monitor_mic_high.py # Script to apply/revert folder integrity level
├── requirements.txt            # Python dependencies
├── .gitignore                  # .gitignore files that should not be part of repo are mentioned
├── LICENSE                     # MIT LICENSE
└── README.md                   # This file
```

---

## 🚀 How to Use

> ⚠️ **Warning:**
> Always run this demo in a secure, isolated VM. This simulation is for educational/testing purposes only.

### 🔧 Prerequisites

1. **Windows 10 VM** (21H2 or later)
2. **Python 3.8+**
3. Internet access (to install Python packages)
4. (Optional) **PyInstaller** for bundling scripts into `.exe`
5. Familiarity with elevated (Administrator) command prompt

### 📅 Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/farman20ali/digital-forensic-ransomware-mic.git
   cd digital-forensic-ransomware-mic
   ```

2. **Create & activate a virtual environment**

   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   *Contents of `requirements.txt`:*

   ```
   cryptography
   watchdog
   psutil
   ```

4. **(Optional) Bundle scripts**

   ```bash
   pip install pyinstaller
   pyinstaller --onefile --windowed trojan.py
   pyinstaller --onefile --windowed defence_monitor_mic_high.py
   ```

   * Outputs appear in dist/ as trojan.exe and defence_monitor_mic_high.exe.

---

## 🗂️ Prepare the Test Directory

1. **Generate dummy files**

   ```bash
   python setup_dummy_files.py --target test_files --count 30
   ```

2. **Set folder integrity level to High**

   ```bash
   # Run as Administrator:
   python defence_monitor_mic_high.py apply test_files
   ```

   * This applies **High** MIC to the folder and its children.
   * To revert back to Medium (default):

     ```bash
     python defence_monitor_mic_high.py revert test_files
     ```

---

## 🔒 Run the Simulation

1. **Ensure** `test_files` is at **High** integrity.

2. **Launch the trojan using command or double click** to mimic untrusted code:

   ```powershell
     'trojan.py --path 'test_files'
   ```

3. **Observe:**

   * The trojan script attempts to encrypt files in `test_files`.
   * MIC blocks Medium-integrity processes, so write/rename operations fail, preserving your files.

4. **Revert folder integrity** (if needed):

   ```bash
   python defence_monitor_mic_high.py revert test_files
   ```

---

## 📺 Video Demo Highlights

* 🔧 Setting and reverting integrity levels with `defence_monitor_mic_high.py`
* 💣 Running the ransomware at Medium integrity
* 🚫 Blocked write attempts and protected files
* 🔍 Reviewing Windows security event logs for denied access

Watch it here: [https://www.youtube.com/watch?v=dQw4w9WgXcQ](https://www.youtube.com/watch?v=dQw4w9WgXcQ)

> ⚠️ **Disclaimer:**
> This project is strictly for controlled, educational environments. Never run ransomware simulations on production systems or without explicit authorization.

---

## 🙌 Contributions

Pull requests are welcome for improvements, new defense integrations, or enhanced documentation.

##📄 License
This project is licensed under the MIT License.
