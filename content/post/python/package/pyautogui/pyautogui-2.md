---
title: 如何使用 PyAutoGUI（二）：鍵盤控制
description: 本文介紹 PyAutoGUI 的完整鍵盤控制函式，包含文字輸入、按鍵模擬、組合鍵、熱鍵，以及訊息彈出視窗的應用。
slug: how-to-use-pyautogui-keyboard
date: 2026-05-01 19:20:00+0800
categories:
    - tutorial
tags:
    - PyAutoGUI
    - Python
    - automation
weight: 2
---

## 內容大綱
1. [文字輸入](#1-文字輸入)
2. [單鍵操作](#2-單鍵操作)
   - [按下並放開單一按鍵](#按下並放開單一按鍵-press)
   - [按住不放與放開按鍵](#按住不放與放開按鍵-keydown--keyup)
   - [上下文管理器](#上下文管理器-hold)
   - [組合鍵與熱鍵](#組合鍵與熱鍵-hotkey)
3. [常用 Key 名稱對照表](#3-常用-key-名稱對照表)
4. [訊息彈出視窗](#4-訊息彈出視窗)
   - [alert()](#顯示訊息-alert)
   - [confirm()](#確認視窗-confirm)
   - [prompt()](#文字輸入視窗-prompt)
   - [password()](#密碼輸入視窗-password-遮蔽顯示)
5. [實用範例：自動開啟記事本並輸入文字](#5-實用範例自動開啟記事本並輸入文字)

---

### 1. 文字輸入

#### `typewrite()` / `write()`

兩者完全相同，用於模擬逐鍵輸入文字：



```python
import pyautogui

# 在目前焦點位置輸入文字
pyautogui.typewrite('Hello, World!')

# 設定每個字元之間的間隔（秒），模擬真實打字速度
pyautogui.typewrite('Hello!', interval=0.1)

# write() 與 typewrite() 完全相同
pyautogui.write('Python automation', interval=0.05)
```

> **⚠️ 注意：中文輸入限制**  
> `typewrite()` 只支援 ASCII 字元，**無法直接輸入中文**。若要輸入中文，需改用剪貼簿方式：
>
> ```python
> import pyautogui
> import pyperclip  # pip install pyperclip
>
> # 將中文複製到剪貼簿，再貼上
> pyperclip.copy('你好，世界！')
> pyautogui.hotkey('ctrl', 'v') # 稍後會介紹 hotkey 函數
> ```

---

### 2. 單鍵操作：

#### 按下並放開單一按鍵 `press()`：

```python
import pyautogui

# 按下 Enter 鍵
pyautogui.press('enter')

# 按下 Tab 鍵
pyautogui.press('tab')

# 按下方向鍵（上下左右）
pyautogui.press('up')
pyautogui.press('down')
pyautogui.press('left')
pyautogui.press('right')

# 連續按多次（按 3 次空白鍵）
pyautogui.press('space', presses=3)

# 設定每次按鍵之間的間隔
pyautogui.press('tab', presses=5, interval=0.2)

# 也可以傳入 list，依序按下多個鍵
pyautogui.press(['up', 'up', 'down', 'down', 'left', 'right'])
```

#### 按住不放與放開按鍵 `keyDown()` / `keyUp()`：

```python
import pyautogui

# 按住 Shift 鍵不放
pyautogui.keyDown('shift')

# 輸入文字（若無鎖定`CAPSLOCK`，此時會全部變大寫）
pyautogui.typewrite('hello')  # 實際輸入 HELLO

# 放開 Shift 鍵
pyautogui.keyUp('shift')
```

> **實際應用：按住 Shift 並點擊以選取文字**
>
> ```python
> import pyautogui
> # 先點擊起始位置
> pyautogui.click(200, 300)
> # 按住 Shift
> pyautogui.keyDown('shift')
> # 點擊結束位置（選取這段範圍的文字）
> pyautogui.click(600, 300)
> # 放開 Shift
> pyautogui.keyUp('shift')
> ```

#### 上下文管理器 `hold()`：

```python
import pyautogui

# 該shift鍵將在上下文區塊期間保持按住狀態。
with pyautogui.hold('shift'):
  pyautogui.press(['left', 'left', 'left'])
```


#### 組合鍵與熱鍵 `hotkey()`：

```python
import pyautogui

pyautogui.hotkey('ctrl', 'c') # Ctrl + C（複製）
pyautogui.hotkey('ctrl', 'v') # Ctrl + V（貼上）

# Alt + F4（關閉視窗，Windows）
pyautogui.hotkey('alt', 'f4')
# Ctrl + Alt + Delete（Windows）
pyautogui.hotkey('ctrl', 'alt', 'delete')
# macOS 截圖：Cmd + Shift + 4
pyautogui.hotkey('command', 'shift', '4')
# Ctrl + Shift + T（重開分頁，瀏覽器）
pyautogui.hotkey('ctrl', 'shift', 't')
```

---

### 3. 常用 Key 名稱對照表

以下是 `press()`、`keyDown()`、`keyUp()`、`hotkey()` 可接受的常用鍵名：

| 類別 | Key 名稱 |
|------|---------|
| **修飾鍵** | `shift`、`ctrl`、`alt`、`command`（macOS）、`win`（Windows）|
| **功能鍵** | `f1` ~ `f12` |
| **方向鍵** | `up`、`down`、`left`、`right` |
| **特殊鍵** | `enter`、`esc`、`tab`、`backspace`、`delete`、`space`、`capslock` |
| **Page 鍵** | `pageup`、`pagedown`、`home`、`end` |
| **數字鍵盤** | `num0` ~ `num9`、`numlock`、`add`、`subtract`、`multiply`、`divide` |
| **媒體鍵** | `volumemute`、`volumedown`、`volumeup`、`playpause` |
| **符號鍵** | `!`、`@`、`#`、`$`、`%`、`^`、`&`、`*`、`(`、`)` |
| **字母/數字** | `a`～`z`、`0`～`9` |

查看所有支援的鍵名：

```python
import pyautogui
print(pyautogui.KEYBOARD_KEYS)
```

你也可以使用下方的互動式工具，快速搜尋按鍵名稱與對應的變數寫法：

> **互動小工具：鍵盤按鍵對照查詢**
> 支援分類篩選與關鍵字搜尋，點擊按鍵卡片可產生範例程式碼。  
程式碼已開源於：[pynput-key-reference](https://dandelionlibra.github.io/tools/pynput_key_reference.html)

<iframe src="https://dandelionlibra.github.io/tools/pynput_key_reference.html" width="100%" height="500px" style="border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; background: #0d0d0f;"></iframe>

---

### 4. 訊息彈出視窗

PyAutoGUI 提供了簡易的 GUI 彈出視窗函式，可在自動化流程中提示使用者或取得確認。

#### 顯示訊息 `alert()`：

```python
import pyautogui

# 顯示提示訊息
pyautogui.alert('操作完成！')

# 自訂標題
pyautogui.alert(text='備份成功。', title='通知', button='確定')
```

#### 確認視窗 `confirm()`：

```python
result = pyautogui.confirm('確定要刪除嗎？', title='確認', buttons=['確定', '取消'])
print(result)  # 使用者點了哪個按鈕的文字
```

#### 文字輸入視窗 `prompt()`：

```python
name = pyautogui.prompt('請輸入你的名字：', title='輸入', default='')
if name:
    print(f'你好，{name}！')
```

#### 密碼輸入視窗 `password()`（遮蔽顯示）：

```python
pwd = pyautogui.password('請輸入密碼：', title='登入', default='', mask='*')
print(f'輸入的密碼：{pwd}')
```

---

### 5. 實用範例：自動開啟記事本並輸入文字

以下範例示範如何在 Windows 上自動開啟記事本，並輸入一段文字再儲存：

```python
import pyautogui
import subprocess
import time

# 開啟記事本
subprocess.Popen(['notepad.exe'])
time.sleep(1.5)  # 等待視窗開啟

pyautogui.press('shift') # 切換鍵盤成英文

# 輸入文字
pyautogui.typewrite('Hello from PyAutoGUI!', interval=0.05)
pyautogui.press('enter')
pyautogui.typewrite('This is automated typing.', interval=0.05)

# 儲存（Ctrl + S）
pyautogui.hotkey('ctrl', 's')
time.sleep(1)

# 在另存新檔視窗中輸入檔名
pyautogui.typewrite('auto_test.txt', interval=0.05)
pyautogui.press('enter')

print("完成！已儲存為 auto_test.txt")
```

---

## 練習題

<details>
<summary>📝 練習題 1：自動全選並複製</summary>

**題目**：在任意文字編輯器中，用 PyAutoGUI 執行「全選→複製→游標移至末尾→貼上」的操作序列。

  <details>
  <summary>答案：</summary>

  ```python
  import pyautogui
  import time

  time.sleep(2)  # 手動切換到目標視窗

  pyautogui.hotkey('ctrl', 'a')   # 全選
  time.sleep(0.3)
  pyautogui.hotkey('ctrl', 'c')   # 複製
  time.sleep(0.3)
  pyautogui.press('end')          # 移至末尾
  pyautogui.press('enter')        # 換行
  pyautogui.hotkey('ctrl', 'v')   # 貼上
  ```

  </details>
</details>

---

<details>
<summary>📝 練習題 2：詢問使用者再執行</summary>

**題目**：用 `confirm()` 彈出確認視窗，若使用者點「確定」，才執行自動輸入文字的動作；若點「取消」，則印出「已取消」。

  <details>
  <summary>答案：</summary>

  ```python
  import pyautogui
  import time

  result = pyautogui.confirm('是否要開始自動輸入？', title='確認', buttons=['確定', '取消'])

  if result == '確定':
      time.sleep(2)  # 切換到目標視窗
      pyautogui.typewrite('自動輸入的文字！', interval=0.1)
  else:
      print('已取消')
  ```

  </details>
</details>

---

<details>
<summary>📝 練習題 3：模擬 Vim 儲存並離開</summary>

**題目**：假設 Vim 已開啟並在 Normal mode，用 PyAutoGUI 模擬輸入 `:wq` 後按 Enter 來儲存並離開。

  <details>
  <summary>答案：</summary>

  ```python
  import pyautogui
  import time

  time.sleep(2)  # 切換到 Vim 視窗

  # 確保在 Normal mode
  pyautogui.press('esc')
  time.sleep(0.2)

  # 輸入 :wq 指令
  pyautogui.typewrite(':wq', interval=0.1)
  pyautogui.press('enter')
  ```

  </details>
</details>

---

## 參考資料

- [PyAutoGUI 官方文件 — Keyboard](https://pyautogui.readthedocs.io/en/latest/keyboard.html)
- [PyAutoGUI 官方文件 — Message Box](https://pyautogui.readthedocs.io/en/latest/msgbox.html)
- [PyAutoGUI GitHub 原始碼](https://github.com/asweigart/pyautogui)
- [Automate the Boring Stuff with Python — Chapter 20](https://automatetheboringstuff.com/2e/chapter20/)
