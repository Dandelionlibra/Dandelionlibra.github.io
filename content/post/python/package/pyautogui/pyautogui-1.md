---
title: 如何使用 PyAutoGUI（一）：安裝與滑鼠控制
description: 本文介紹 PyAutoGUI 的基本概念、安裝方式，以及完整的滑鼠控制函式教學，包含點擊、移動、拖曳與滾輪操作。
slug: how-to-use-pyautogui-mouse
date: 2026-04-30 00:00:00+0800
categories:
    - tutorial
tags:
    - PyAutoGUI
    - Python
    - automation
weight: 1
---

## 內容大綱

1. [PyAutoGUI 基本介紹](#1-pyautogui-基本介紹)
2. [安裝 PyAutoGUI](#2-安裝-pyautogui)
3. [螢幕座標系統](#3-螢幕座標系統)
4. [安全機制：Fail-Safe](#4-安全機制fail-safe)
5. [取得螢幕資訊](#5-取得螢幕資訊)
6. [滑鼠點擊](#6-滑鼠點擊)
   - [點擊](#點擊-click)
   - [雙擊](#雙擊-doubleclick)
   - [右鍵點擊](#右鍵點擊-rightclick)
   - [中鍵點擊](#中鍵點擊-middleclick)
   - [分開按下與放開](#分開按下與放開-mousedown--mouseup)
7. [滑鼠移動](#7-滑鼠移動)
   - [移動到絕對座標](#移動到絕對座標-movetox-y-durationnum_seconds)
   - [移動到相對座標](#移動到相對座標-movelrelxoffset-yoffset-durationnum_seconds)
   - [拖曳到絕對座標](#拖曳到絕對座標-dragtox-y-durationnum_seconds)
   - [拖曳到相對座標](#拖曳到相對座標-dragrelxoffset-yoffset-durationnum_seconds)
8. [滾輪操作](#8-滾輪操作)
   - [垂直滾動](#垂直滾動-scroll)
   - [水平滾動](#水平滾動-hscroll)

---

### 1. PyAutoGUI 基本介紹

PyAutoGUI 是一個跨平台的 Python GUI 自動化套件，可以程式化地控制**滑鼠**與**鍵盤**，適用於 Windows、macOS 和 Linux。常見應用場景包括：

- **重複性操作自動化**：自動填表、批次處理檔案。
- **GUI 測試**：模擬使用者操作，進行介面測試。
- **螢幕截圖與圖像辨識**：截圖並尋找特定圖案位置，再進行點擊。

> **⚠️ 注意事項**  
> PyAutoGUI 會直接控制系統的滑鼠與鍵盤，執行時請先確認不會誤操作重要視窗，建議先在測試環境中嘗試。

---

### 2. 安裝 PyAutoGUI

在終端機輸入以下指令：

```bash
pip install pyautogui
```

若有多個版本的 python 可以指定特定版本：

```bash
py -3.8 -m pip install pyautogui
```

**macOS：**
```bash
python3 -m pip install pyautogui
```

**Linux：**  
還需要安裝額外依賴套件。
```bash
sudo apt-get install python3-tk python3-dev scrot
python3 -m pip install pyautogui
```

安裝完成後，驗證是否成功：

```python
import pyautogui
print(pyautogui.size())  # 印出螢幕解析度，例如 Size(width=1920, height=1080)
```

---

### 3. 螢幕座標系統

在開始自動化之前，我們必須先了解電腦螢幕的座標系統（Coordinate System）：

*   **原點 (0, 0)**：位於螢幕的 **左上角 (Top-Left)**。
*   **X 軸**：水平方向，由左向右遞增。
*   **Y 軸**：垂直方向，由上向下遞增。

如果你想更直觀地了解座標位置，可以使用下方我開發的小工具。移動滑鼠即可即時顯示座標，點擊畫面則可以釘選座標點。

> **互動小工具：螢幕座標地圖**
> 建議點擊右上角的「全螢幕」按鈕或將瀏覽器視窗最大化，以獲得最準確的座標參考。  
程式碼已開源於：[screen-coordinate-map](https://dandelionlibra.github.io/tools/screen_coordinate_map.html)

<iframe src="https://dandelionlibra.github.io/tools/screen_coordinate_map.html" width="100%" height="500px" style="border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; background: #0d0d0f;"></iframe>

---

### 4. 安全機制：Fail-Safe

PyAutoGUI 內建一個防呆安全機制：**當滑鼠快速移動到螢幕左上角（座標 0, 0）時，會自動丟出 `FailSafeException` 並中止程式。**

這個機制可以讓你在程式失控時，快速移動滑鼠到左上角以強制停止。

```python
import pyautogui

# 安全機制，正式使用時請保持啟用（預設為 True）
pyautogui.FAILSAFE = True

# 若確定不需要此機制（不建議）可關閉
pyautogui.FAILSAFE = False
```

此外，還有一個全域延遲設定，讓每個操作之間自動暫停，避免操作太快：

```python
# 每次 PyAutoGUI 函式呼叫後，暫停 0.5 秒（預設為 0.1）
pyautogui.PAUSE = 0.5
```

---

### 5. 取得螢幕資訊

```python
import pyautogui

# 取得螢幕解析度
width, height = pyautogui.size()
print(f"螢幕寬度：{width}，高度：{height}")

# 取得滑鼠目前位置
x, y = pyautogui.position()
print(f"目前滑鼠座標：({x}, {y})")
```

> **💡 小技巧**：執行以下程式碼，可以即時追蹤滑鼠座標，按 `Ctrl+C` 停止：
>
> ```python
> import pyautogui, time
> try:
>     while True:
>         x, y = pyautogui.position()
>         print(f"\r目前座標：({x:4}, {y:4})", end="", flush=True)
>         time.sleep(0.1)
> except KeyboardInterrupt: # 按下 Ctrl+C 會中斷程式
>     print("\n已停止追蹤")
> ```

---

### 6. 滑鼠點擊

#### 點擊 `click()`：

```python
import pyautogui

pyautogui.click() # 在目前位置點擊左鍵

pyautogui.click(500, 300) # 點擊指定座標

pyautogui.click(500, 300, button='right') # 指定按鍵 'left'、'right'、'middle'

pyautogui.click(500, 300, clicks=2) # 連續點擊
pyautogui.click(500, 300, clicks=2, interval=0.25) # 設定兩次點擊之間的間隔（秒）
pyautogui.click(button='right', clicks=3, interval=0.25) # 指定按鍵並連續點擊
```

#### 雙擊 `doubleClick()`：

```python
# 在指定位置雙擊
pyautogui.doubleClick(500, 300)
```
> **註解**  
> 也有 `tripleClick()` 函數，用以點擊三次螢幕。


#### 右鍵點擊 `rightClick()`：
```python
pyautogui.rightClick(500, 300)
```

#### 中鍵點擊 `middleClick()`：

```python
pyautogui.middleClick(500, 300)
```

#### 分開按下與放開 `mouseDown()` / `mouseUp()`：

```python
# 按下與放開皆預設為左鍵
pyautogui.mouseDown()   # 按下左鍵（不放開）
pyautogui.mouseUp()     # 放開左鍵

# 按下右鍵（不放開）
pyautogui.mouseDown(500, 300, button='right')

# 放開右鍵
pyautogui.mouseUp(500, 300, button='right')
```

---
### 7. 滑鼠移動

#### 移動到絕對座標 `moveTo(x, y, duration=num_seconds)`：

```python
import pyautogui

# 移動到螢幕座標 (500, 300)
pyautogui.moveTo(500, 300)

# 移動到 (500, 300)，花費 1 秒（加入緩動效果）
pyautogui.moveTo(500, 300, duration=1)

# 使用緩動函式（easing），讓動作更自然
pyautogui.moveTo(500, 300, duration=1, tween=pyautogui.easeInOutQuad)
```

#### 移動到相對座標 `moveRel(xOffset, yOffset, duration=num_seconds)`：

```python
# 從目前位置，向右移動 100px、向下移動 50px
pyautogui.moveRel(100, 50)

# moveRel 與 move 完全相同
pyautogui.move(100, 50, duration=0.5)
```

#### 拖曳到絕對座標 `dragTo(x, y, duration=num_seconds)`：

```python
import pyautogui

# 從目前位置拖曳到 (700, 400)，花費 0.5 秒
pyautogui.dragTo(700, 400, duration=0.5)

# 指定使用左鍵拖曳
pyautogui.dragTo(700, 400, duration=0.5, button='left')
```

#### 拖曳到相對座標 `dragRel(xOffset, yOffset, duration=num_seconds)`：

```python
# 從目前位置向右拖曳 200px、向下 100px
pyautogui.dragRel(200, 100, duration=0.5)

# drag 與 dragRel 完全相同
pyautogui.drag(200, 100, duration=0.5)
```

> **實用範例：拖曳視窗**
>
> ```python
> import pyautogui
> import time
> 
> # 點擊視窗標題列(假設(400, 30)有視窗標題)
> pyautogui.click(400, 30)
> time.sleep(0.2)
> 
> # 拖曳視窗到新位置
> pyautogui.dragTo(800, 200, duration=1, button='left')
> ```

**常用 tween 緩動函式：**

| 函式 | 效果 | 範例指令 |
|------|------|----------|
| `pyautogui.linear` | 等速移動（預設） | `pyautogui.moveTo(x, y, tween=pyautogui.linear)` |
| `pyautogui.easeInQuad` | 由慢到快 | `pyautogui.moveTo(x, y, tween=pyautogui.easeInQuad)` |
| `pyautogui.easeOutQuad` | 由快到慢 | `pyautogui.moveTo(x, y, tween=pyautogui.easeOutQuad)` |
| `pyautogui.easeInOutQuad` | 先慢後快再慢 | `pyautogui.moveTo(x, y, tween=pyautogui.easeInOutQuad)` |
| `pyautogui.easeInBounce` | 到達目標後反彈 | `pyautogui.moveTo(x, y, tween=pyautogui.easeInBounce)` |

---

### 8. 滾輪操作

#### 垂直滾動 `scroll()`

```python
import pyautogui

# 向上滾動 3 格（正值向上，負值向下）
pyautogui.scroll(3)

# 在指定座標向下滾動 5 格
pyautogui.scroll(-5, x=500, y=400)
```

#### 水平滾動 `hscroll()`

```python
# 向右水平滾動 3 格
pyautogui.hscroll(3)

# 向左水平滾動 3 格
pyautogui.hscroll(-3)
```

---

## 練習題

<details>
<summary>📝 練習題 1：滑鼠畫正方形</summary>

**題目**：使用 `moveTo()` 讓滑鼠依序移動到四個角落，畫出一個邊長 200px 的正方形路徑（從座標 (200, 200) 出發）。

  <details>
  <summary>答案：</summary>

  ```python
  import pyautogui
  import time

  pyautogui.PAUSE = 0.5

  pyautogui.moveTo(200, 200, duration=0.5)
  pyautogui.moveTo(400, 200, duration=0.5)
  pyautogui.moveTo(400, 400, duration=0.5)
  pyautogui.moveTo(200, 400, duration=0.5)
  pyautogui.moveTo(200, 200, duration=0.5)

  print("正方形路徑完成！")
  ```

  </details>
</details>

---

<details>
<summary>📝 練習題 2：自動右鍵選單</summary>

**題目**：在桌面空白處模擬右鍵點擊，然後按下 `Escape` 關閉選單（需搭配第二篇的鍵盤操作）。

  <details>
  <summary>答案：</summary>

  ```python
  import pyautogui
  import time

  time.sleep(2)  # 給自己時間切換到桌面

  # 在桌面中央右鍵點擊
  screen_w, screen_h = pyautogui.size()
  pyautogui.rightClick(screen_w // 2, screen_h // 2)
  time.sleep(0.5)

  # 按 Escape 關閉選單
  pyautogui.press('escape')
  ```

  </details>
</details>

---

<details>
<summary>📝 練習題 3：計算並移動到螢幕中心</summary>

**題目**：用程式取得螢幕解析度後，計算出螢幕中心點，並將滑鼠移動過去。

  <details>
  <summary>答案：</summary>

  ```python
  import pyautogui

  width, height = pyautogui.size()
  center_x = width // 2
  center_y = height // 2

  print(f"螢幕中心：({center_x}, {center_y})")
  pyautogui.moveTo(center_x, center_y, duration=1)
  ```

  </details>
</details>

---

## 參考資料

- [PyAutoGUI 官方文件](https://pyautogui.readthedocs.io/en/latest/)
- [PyAutoGUI GitHub 原始碼](https://github.com/asweigart/pyautogui)
- [Al Sweigart 的 PyAutoGUI 教學（英文）](https://automatetheboringstuff.com/2e/chapter20/)
