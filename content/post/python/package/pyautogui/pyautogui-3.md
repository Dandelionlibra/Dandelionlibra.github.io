---
title: 如何使用 PyAutoGUI（三）：螢幕截圖與圖像辨識
description: 本文介紹 PyAutoGUI 的截圖功能與圖像辨識技術，包含全螢幕截圖、區域截圖、尋找圖案位置，以及像素顏色偵測，並結合完整的自動化實戰範例。
slug: how-to-use-pyautogui-screenshot
date: 2026-04-30 00:00:02+0800
categories:
    - tutorial
tags:
    - PyAutoGUI
    - Python
    - automation
    - 圖像辨識
weight: 3
---

## 內容大綱

1. [截取螢幕畫面](#1-截取螢幕畫面)
   - [全螢幕截圖](#全螢幕截圖-screenshot)
   - [區域截圖](#區域截圖-screenshotregion)
2. [圖像辨識：在螢幕上尋找圖片](#2-圖像辨識在螢幕上尋找圖片)
   - [尋找圖片位置](#尋找圖片位置-locateonscreen)
   - [取得圖片中心座標](#取得圖片中心座標-locatecentersonscreen)
   - [尋找所有符合位置](#尋找所有符合位置-locateallonscreen)
   - [在圖片中搜尋](#在圖片中搜尋-locate非螢幕)
3. [像素顏色偵測](#3-像素顏色偵測)
   - [取得指定座標的像素顏色](#取得指定座標的像素顏色-pixel)
   - [判斷像素顏色是否符合](#判斷像素顏色是否符合-pixelmatchescolor)
4. [實戰範例：自動點擊指定按鈕](#4-實戰範例自動點擊指定按鈕)
5. [實戰範例：等待圖案出現再執行](#5-實戰範例等待圖案出現再執行)
6. [常見問題與除錯技巧](#6-常見問題與除錯技巧)

---

### 1. 截取螢幕畫面

#### 全螢幕截圖 `screenshot()`：  
在 1920 x 1080 的螢幕上，`screenshot()`大約需要 100 毫秒。

```python
import pyautogui

# 截取全螢幕，回傳 PIL Image 物件
img = pyautogui.screenshot()

# 顯示圖片（需安裝 Pillow）
img.show()

# 直接儲存為檔案
pyautogui.screenshot('screenshot.png')

# 截圖並儲存
img = pyautogui.screenshot('my_screen.png')
print(f"截圖尺寸：{img.size}")  # (寬, 高)
```

#### 區域截圖 `screenshot(region=(...)))`：

`region` 參數格式為 `(left, top, width, height)`，分別表示要截圖區域的左側、頂部、寬度和高度。

```python
import pyautogui

# 截取左上角 400x300 的區域
img = pyautogui.screenshot(region=(0, 0, 400, 300))

# 截取螢幕中央的 200x200 區域
screen_w, screen_h = pyautogui.size()
cx = screen_w // 2 - 100
cy = screen_h // 2 - 100
img = pyautogui.screenshot(region=(cx, cy, 200, 200))
img.save('center_crop.png')
```

> **💡 補充說明：PIL Image 物件**  
> `screenshot()` 回傳的是 [Pillow](https://pillow.readthedocs.io/) 的 `Image` 物件，可以進一步進行旋轉、裁切、濾鏡等影像處理，也可以轉成 NumPy 陣列配合 OpenCV 使用：
>
> ```python
> import numpy as np
> import cv2
>
> img = pyautogui.screenshot()
> frame = np.array(img)
> frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
> cv2.imwrite('screen_cv2.png', frame)
> ```

---

### 2. 圖像辨識：在螢幕上尋找圖片

PyAutoGUI 可以在當前螢幕畫面中搜尋指定圖片，回傳其位置。

> **前置條件**：需先準備好要搜尋的圖片（`.png` 格式最佳），可用截圖工具截取目標按鈕或圖案。

> **⚠️ 注意：新舊版本差異**  
> 在新版 PyAutoGUI 中，若找不到圖片會拋出 `pyautogui.ImageNotFoundException`；如果是舊版，則會回傳 `None`，可以使用 `if location:` 來判斷。  
建議統一使用 `try...except` 來確保程式不會崩潰。

#### 尋找圖片位置 `locateOnScreen()`：

```python
import pyautogui

try:
    # 在螢幕上尋找 button.png，找到則回傳 Box(left, top, width, height)
    location = pyautogui.locateOnScreen('button.png')
    print(f"找到圖片：{location}")
    # location.left, location.top, location.width, location.height
except pyautogui.ImageNotFoundException:
    print("找不到圖片")
```

#### 取得圖片中心座標 `locateCenterOnScreen()`：

```python
import pyautogui

try:
    # 找到圖片並直接回傳中心點座標 (x, y)
    center = pyautogui.locateCenterOnScreen('button.png')
    x, y = center
    print(f"圖片中心：({x}, {y})")
    pyautogui.click(x, y)
except pyautogui.ImageNotFoundException:
    print("找不到圖片")
```

#### 調整信心值（confidence）

當截圖與螢幕畫面因縮放或顯示設定略有差異時，可調整 `confidence` 參數（需安裝 `opencv-python`）：

```bash
pip install opencv-python
```

```python
import pyautogui

# confidence 介於 0~1，預設為 1.0（完全相符）
# 降低至 0.8 可接受 80% 的相似度
try:
    location = pyautogui.locateOnScreen('button.png', confidence=0.8)
    print(f"找到圖片：{location}")
except pyautogui.ImageNotFoundException:
    print("找不到圖片")
```

#### 尋找所有符合位置 `locateAllOnScreen()`：

```python
import pyautogui

try:
    # 回傳所有符合位置的 generator
    all_locations = list(pyautogui.locateAllOnScreen('icon.png'))
    print(f"共找到 {len(all_locations)} 個符合位置")
    for loc in all_locations:
        print(loc)
except pyautogui.ImageNotFoundException:
    print("找不到任何符合的圖片")
```

#### 在圖片中搜尋 `locate()`（非螢幕）：

```python
from PIL import Image
import pyautogui

# 在一張截圖檔案中搜尋另一張圖片
haystack = Image.open('fullscreen.png')
needle = Image.open('button.png')

try:
    location = pyautogui.locate(needle, haystack, confidence=0.9)
    print(location)
except pyautogui.ImageNotFoundException:
    print("在圖片中找不到目標圖案")
```

---

### 3. 像素顏色偵測

#### 取得指定座標的像素顏色 `pixel()`：

```python
import pyautogui

# 取得座標 (100, 200) 的 RGB 顏色值
r, g, b = pyautogui.pixel(100, 200)
print(f"顏色：RGB({r}, {g}, {b})")
```

#### 判斷像素顏色是否符合 `pixelMatchesColor()`：

```python
import pyautogui

# 判斷 (100, 200) 是否為紅色 (255, 0, 0)
is_red = pyautogui.pixelMatchesColor(100, 200, (255, 0, 0))
print(f"是紅色嗎？{is_red}")

# 允許一定的顏色誤差（tolerance 預設為 0）
is_approx_red = pyautogui.pixelMatchesColor(100, 200, (255, 0, 0), tolerance=30)
print(f"接近紅色嗎？{is_approx_red}")
```

**實用應用：偵測載入完成**

```python
import pyautogui
import time

# 等待某個座標的顏色變成綠色（表示載入完成）
print("等待載入完成...")
while True:
    r, g, b = pyautogui.pixel(500, 300)
    if g > 200 and r < 100 and b < 100:  # 接近綠色
        print("載入完成！")
        break
    time.sleep(0.5)
```

---

### 4. 實戰範例：自動點擊指定按鈕

以下範例示範如何找到螢幕上的「送出」按鈕圖片並自動點擊：

```python
import pyautogui
import time

def click_button(image_path, confidence=0.9, timeout=10):
    """
    在螢幕上搜尋圖片並點擊，若超過 timeout 秒仍找不到則拋出例外。
    """
    start_time = time.time()

    while True:
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
            if location:
                pyautogui.click(location)
                print(f"成功點擊：{image_path}")
                return True
        except pyautogui.ImageNotFoundException:
            pass

        if time.time() - start_time > timeout:
            raise TimeoutError(f"超過 {timeout} 秒仍找不到：{image_path}")

        time.sleep(0.5)

# 使用範例
try:
    click_button('submit_button.png', confidence=0.85, timeout=15)
except TimeoutError as e:
    print(f"錯誤：{e}")
```

---

### 5. 實戰範例：等待圖案出現再執行

```python
import pyautogui
import time

def wait_for_image(image_path, confidence=0.85, check_interval=1.0):
    """
    持續等待直到螢幕出現指定圖片，回傳中心座標。
    """
    print(f"等待出現：{image_path}")

    while True:
        try:
            center = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
            if center:
                print(f"已找到，座標：{center}")
                return center
        except pyautogui.ImageNotFoundException:
            pass

        time.sleep(check_interval)


# 完整自動化流程範例
import pyautogui, time

time.sleep(3)  # 等待目標程式啟動

# 等待「登入」按鈕出現
login_btn = wait_for_image('login_button.png')
pyautogui.click(login_btn)
time.sleep(0.5)

# 輸入帳號密碼
pyautogui.typewrite('user@example.com', interval=0.05)
pyautogui.press('tab')
pyautogui.typewrite('mypassword', interval=0.05)

# 等待「送出」按鈕出現並點擊
submit_btn = wait_for_image('submit_button.png')
pyautogui.click(submit_btn)

# 等待「歡迎」畫面出現，確認登入成功
wait_for_image('welcome_screen.png')
print("登入成功！")
```

---

### 6. 常見問題與除錯技巧

#### 問題 1：`locateOnScreen()` 找不到圖片

可能原因與解決方式：

| 原因 | 解決方式 |
|------|---------|
| 螢幕縮放不同（HiDPI / Retina） | 降低 `confidence` 值，例如 `0.8` |
| 圖片有些微色差 | 加入 `grayscale=True` 進行灰階比對 |
| 圖片不在當前可視範圍 | 確認視窗是否最小化或被遮擋 |
| 圖片解析度不符 | 重新截取在目標機器上的按鈕圖片 |

```python
# 灰階比對，對顏色差異更有容忍度
location = pyautogui.locateOnScreen('button.png', grayscale=True, confidence=0.8)
```

#### 問題 2：macOS 截圖需要授權

在 macOS 上，需至「系統設定 → 隱私權與安全性 → 螢幕錄製」，將執行 Python 的終端機加入允許清單。

#### 問題 3：速度太快造成錯誤

```python
import pyautogui

# 增加全域延遲
pyautogui.PAUSE = 0.3

# 或在關鍵步驟加入 time.sleep()
import time
time.sleep(0.5)
```

#### 取得當前像素顏色的小工具

```python
import pyautogui, time

print("移動滑鼠到目標位置，3 秒後擷取顏色")
time.sleep(3)
x, y = pyautogui.position()
r, g, b = pyautogui.pixel(x, y)
print(f"座標 ({x}, {y}) 的顏色：RGB({r}, {g}, {b})")
```

---

## 練習題

<details>
<summary>📝 練習題 1：截取並儲存指定區域</summary>

**題目**：截取螢幕右下角 300x200 的區域，儲存為 `corner.png`。


  <details>
  <summary>答案：</summary>

  ```python
  import pyautogui

  w, h = pyautogui.size()
  region = (w - 300, h - 200, 300, 200)
  pyautogui.screenshot('corner.png', region=region)
  print("已儲存右下角截圖：corner.png")
  ```

  </details>
</details>

---

<details>
<summary>📝 練習題 2：確認按鈕存在才點擊</summary>

**題目**：嘗試在螢幕上尋找 `ok_button.png`，若找到則點擊，否則印出「找不到按鈕」。

  <details>
  <summary>答案：</summary>

  ```python
  import pyautogui

  try:
      center = pyautogui.locateCenterOnScreen('ok_button.png', confidence=0.85)
      if center:
          pyautogui.click(center)
          print("已點擊 OK 按鈕")
  except pyautogui.ImageNotFoundException:
      print("找不到按鈕")
  ```

  </details>
</details>

---

<details>
<summary>📝 練習題 3：像素顏色監控</summary>

**題目**：每秒偵測座標 (960, 540) 的像素顏色，若 R 值超過 200 則印出警告訊息並停止，最多監控 30 秒。

  <details>
  <summary>答案：</summary>

  ```python
  import pyautogui
  import time

  print("開始監控像素顏色...")
  for i in range(30):
      r, g, b = pyautogui.pixel(960, 540)
      print(f"第 {i+1} 秒：RGB({r}, {g}, {b})")
      if r > 200:
          print("⚠️ 警告：R 值超過 200！")
          break
      time.sleep(1)
  else:
      print("監控結束，未觸發警告")
  ```

  </details>
</details>

---

## 參考資料

- [PyAutoGUI 官方文件 — Screenshot](https://pyautogui.readthedocs.io/en/latest/screenshot.html)
- [PyAutoGUI 官方文件 — Locating](https://pyautogui.readthedocs.io/en/latest/screenshot.html#locating-on-screen)
- [Pillow 官方文件](https://pillow.readthedocs.io/en/stable/)
- [OpenCV-Python 教學](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [PyAutoGUI GitHub 原始碼](https://github.com/asweigart/pyautogui)
- [Automate the Boring Stuff with Python — Chapter 20](https://automatetheboringstuff.com/2e/chapter20/)
