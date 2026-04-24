---
title: 如何使用 venv 建立 Python 虛擬環境
description: 本文詳細介紹如何使用 Python 內建的 venv 指令建立、啟動與管理虛擬環境，幫助隔離不同專案的套件依賴。
slug: how-to-use-venv
date: 2026-04-25 03:29:13+0800
categories:
    - tutorial
tags:
    - Python
    - venv
    - virtual environment
weight: 1
---

## 內容大綱

1. [什麼是虛擬環境？為何需要它？](#1-什麼是虛擬環境為何需要它)
2. [建立虛擬環境](#2-建立虛擬環境)
3. [進階參數指令 (Options)](#3-進階參數指令-options)
4. [啟動與退出虛擬環境](#4-啟動與退出虛擬環境)
5. [套件的安裝、匯出與批次移除](#5-套件的安裝匯出與批次移除)
6. [常見問題與注意事項](#6-常見問題與注意事項)

---

### 1. 什麼是虛擬環境？為何需要它？

在開發 Python 專案時，經常需要使用 `pip` 安裝各種第三方套件。如果不使用虛擬環境，所有套件都會被安裝到系統全域環境中。這樣會產生幾個嚴重問題：
- **版本衝突**：專案 A 需要 `Django 3.0`，但專案 B 卻依賴 `Django 4.0`，兩者無法共存於同一個環境。
- **環境污染**：全域環境累積過多不需要的套件，難以管理。

`**venv**` 是 Python 3.3 之後內建的虛擬環境管理工具，它能為每個專案建立一個獨立的資料夾。在這個資料夾中，擁有獨立的 Python 執行檔與獨立的套件庫，從而完美隔離各個專案。

### 2. 建立虛擬環境

建立虛擬環境主要有兩種指定路徑的方式。

**方式一：在目前目錄下建立（相對路徑）**
請先開啟終端機，並使用 `cd` 指令切換到專案資料夾，接著輸入以下指令：

```bash
# Windows / macOS / Linux 通用指令
python -m venv venv
```

- `python -m venv`：呼叫 Python 內建的 `venv` 模組。
- 最後的 `venv`：這是即將產生的虛擬環境資料夾名稱。一般約定成俗會將其命名為 `venv` 或 `.venv`。執行後，目前的專案目錄下就會多出這個資料夾。

**方式二：在指定位置建立（絕對路徑）**
如果不想將虛擬環境放在專案資料夾內，或者想統一集中管理所有虛擬環境，可以直接指定一個完整的路徑：

```bash
python -m venv /path/to/new/virtual/environment
```

**兩個指令的差別：**
- **`python -m venv venv`**：利用**相對路徑**，將虛擬環境建立在「目前終端機所在的資料夾」底下。適合讓每個專案擁有專屬、跟隨專案代碼的環境，這也是最常見的做法。
- **`python -m venv /path/to/...`**：利用**絕對路徑**（或明確指定的路徑），無論目前終端機在哪個目錄，都會將虛擬環境強制建立在指定的特定位置上。適合習慣把所有虛擬環境統一存放在同一個集中目錄（例如 `~/.virtualenvs/`）的開發情境。

不管使用哪種方式，執行後該資料夾裡面都會包含獨立的 Python 執行檔與套件庫結構。

### 3. 進階參數指令 (Options)

在建立虛擬環境時，可以在終端機加上特定的參數來客製化環境設定（可透過 `python -m venv -h` 查詢完整列表），以下介紹幾個常用的進階參數：

- **`--system-site-packages`**：預設情況下，虛擬環境是完全隔離的。加上此參數後，虛擬環境將「可以存取」系統全域 (System-wide) 所安裝的套件。
- **`--clear`**：如果指定的資料夾已經存在，加上此參數會在建立前「先清空」該資料夾裡的所有內容，相當於重新建立一個乾淨的環境。
- **`--without-pip`**：建立環境時預設會自動安裝 `pip`。若加上此參數則會跳過安裝。
- **`--prompt <PROMPT>`**：自訂啟動虛擬環境後，終端機前面顯示的「提示字元前綴」（預設為資料夾的名稱）。
- **`--upgrade-deps`**：建立環境的同時，將環境內的基礎套件（如 `pip` 和 `setuptools`）直接升級到 PyPI 上的最新版本。
- **`--without-scm-ignore-files`**：建立環境時，不自動生成原始碼控制的忽略檔（新版 Python 預設會自動產生 `.gitignore`）。

### 4. 啟動與退出虛擬環境

建立好之後，需要「啟動 (Activate)」它，讓系統知道接下來的操作都要在這個隔離環境內進行。

**啟動虛擬環境 (Windows Command Prompt)：**
```cmd
venv\Scripts\activate.bat
```

**啟動虛擬環境 (Windows PowerShell)：**
```powershell
venv\Scripts\Activate.ps1
```

**啟動虛擬環境 (macOS / Linux)：**
```bash
source venv/bin/activate
```

啟動成功後，終端機的提示字元前方通常會出現 `(venv)`，代表目前已經身處於虛擬環境中。

**退出虛擬環境：**
當開發結束，想要回到系統全域環境時，只需執行：
```bash
deactivate
```

### 5. 套件的安裝、匯出與批次移除

在虛擬環境啟動的狀態下，使用 `pip install` 安裝的任何套件，都會被存放在這個虛擬環境中，完全不會影響到系統。

**安裝套件：**
```bash
pip install requests
```

**匯出套件清單：**
為了讓專案能夠在其他電腦上重現相同的環境，會將目前安裝的所有套件名稱與版本匯出成一份清單。
```bash
pip freeze > requirements.txt
```

**從清單還原環境：**
當其他人拿到專案時，只要先建立並啟動自己的虛擬環境，就可以透過這份清單一次安裝所有必需的套件。
```bash
pip install -r requirements.txt
```

**強制清空環境的所有套件：**
如果環境遭到污染（裝了太多不相關的套件），或者想將目前環境打掉重練，可以利用 `pip freeze` 配合 `pip uninstall` 來一鍵批次卸載所有第三方套件。

1. 首先，將目前所有安裝的套件清單匯出到一個暫存檔：
```bash
pip freeze > uninstall.txt
```

2. 接著，讓 pip 讀取這個清單，並強制 (`-y`) 刪除裡面的所有套件：
```bash
pip uninstall -r uninstall.txt -y
```
*(備註：`pip freeze` 預設不會把基礎套件 `pip`、`setuptools`、`wheel` 列入清單，因此不用擔心會刪除到這三個核心套件。)*

3. 刪除完成後，再把暫存檔清掉即可：
```bash
# Windows 命令提示字元 (cmd):
del uninstall.txt

# Windows PowerShell:
Remove-Item uninstall.txt

# macOS / Linux:
rm uninstall.txt
```

### 6. 常見問題與注意事項

- **不要將 venv 資料夾加入版本控制**：虛擬環境資料夾體積龐大且包含系統特定的編譯檔案。請務必在 `.gitignore` 檔案中加入 `venv/`，避免將它推送到 GitHub。
- **PowerShell 執行原則錯誤**：在 Windows PowerShell 啟動時如果遇到「執行原則不允許」的紅色錯誤，請以系統管理員身分開啟 PowerShell 並執行 `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` 即可解決。

---

### 參考資料

- [Python 官方文件：venv — 建立虛擬環境](https://docs.python.org/zh-tw/3/library/venv.html)
