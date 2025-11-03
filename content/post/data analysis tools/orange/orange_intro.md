---
title: Orange3
description: 。
slug: Data-mining
date: 2025-07-21 09:16:00+0800
categories:
    - note
    - tool
tags:
    - Data mining
    - Orange3


weight: 1
---

## 什麼是 Orange3？
Orange3 是一款開源 (Open Source) 的資料探勘與機器學習工具。它最大的特色是**視覺化的流程介面** (Visual Programming)。

使用者不需要撰寫程式碼，只需要透過拖拉、連接不同的 **「元件」 (Widgets)**，就可以建構出完整的資料分析、資料前處理、模型訓練與評估的流程。

## 核心優勢

* **視覺化工作流：** 整個分析流程一目了然，非常適合用來教學和展示。
* **無需程式碼：** 大幅降低了機器學習的入門門檻。
* **互動式探索：** 任何元件的參數一經調整（例如你調整 `Random Forest` 的樹木數量），下游所有元件的結果（如 `Test & Score`）都會**即時更新**，便於快速實驗。
* **功能完整：** 涵蓋了資料探勘的完整步驟，從資料讀取到複雜的模型評估都包含在內。

## 核心元件 (Widgets) 介紹

Orange3 的所有功能都包裝在左側的「元件庫」中。以下是我們在房價預測專案中使用到的關鍵元件：

### 1. Data (資料)

這是分析的起點。

* **File (檔案):** 用於載入你的資料集。支援 CSV, Excel, `.tab` 檔案，也內建了許多經典資料集 (例如 `boston.tab`)。
* **Select Columns (選擇欄位):** **極度重要**的步驟。在這裡，我們要告訴 Orange 我們的「目標 (Target)」是什麼 (例如 `MEDV` 房價)，以及哪些是「特徵 (Features)」(例如 `RM`, `LSTAT` 等)。

### 2. Transform (轉換 / 資料前處理)

原始資料通常不能直接拿來建模，需要先「清洗」。

* **Impute (插補缺失值):** 處理資料中的空白格。雖然波士頓資料集很乾淨，但真實世界的資料常用到。
* **Preprocess (前處理):** 一個強大的打包元件，我們用它來做**正規化 (Normalize Features)**。正規化 (例如 Z-score) 可以消除不同特徵間的尺度差異 (例如 `RM` 房間數 3~9 vs. `TAX` 稅率 200~700)，讓模型訓練更穩定。

### 3. Visualize (視覺化)

分析特徵與目標之間的關係。

* **Box Plot (箱型圖):** 非常適合用來比較 **「類別變數」** 與 **「數值變數」** 的關係。
    * *範例：* 我們用 `CHAS` (是否臨河) 作為分組 (Subgroups)，觀察 `MEDV` (房價) 的分佈，清楚地看到臨河的房價中位數更高。
* **Scatter Plot (散點圖):** 用來觀察 **「兩個數值變數」** 之間的關係。
    * *範例：* 我們設定 X 軸為 `RM` (房間數)、Y 軸為 `MEDV` (房價)，看到了明顯的「正相關」。
    * *進階：* 還可以加入 **顏色 (Color)** (例如 `LSTAT`) 或 **形狀 (Shape)** (例如 `CHAS`) 來同時呈現 3~4 個維度的資訊。
* **Rank (排名):** 用來回答「**哪些特徵最重要？**」。它會計算所有特徵與目標變數的相關性分數，是回答 Q2 的關鍵。

### 4. Model (模型)

我們選擇用來預測的演算法。

* **Linear Regression (線性迴歸):** 迴歸任務的基準模型。它會找出一個最佳的線性公式 (例如 `房價 = a*RM - b*LSTAT + c`)。
* **Random Forest (隨機森林):** 一種強大的整合模型。它會建立數百棵決策樹，並將它們的預測結果平均起來。通常準確率高，且不易發生過擬合。
* *(其他常用模型：`Tree` (決策樹), `SVM` (支援向量機), `Gradient Boosting` (梯度提升))*

### 5. Evaluate (評估)

用來評斷模型「好壞」的元件。

* **Test & Score (測試與評分):** **評估的核心**。我們把資料 (`Preprocess`) 和模型 (`Linear Regression`, `Random Forest`) 都連到這裡。
* **Cross-validation (交叉驗證):** `Test & Score` 內最重要的設定。它會自動將資料分成 N 份（例如 10 份），輪流將 9 份當作訓練集、1 份當作測試集，最後算出平均分數。這能有效**避免過擬合**，得到一個可靠的效能指標。

<!-- ## Reference

- [Retrieval-Augmented Generation for Large Language Models: A Survey](https://arxiv.org/abs/2312.10997)
- [Three Paradigms of Retrieval-Augmented Generation (RAG) for LLMs](https://www.thecloudgirl.dev/blog/three-paradigms-of-retrieval-augmented-generation-rag-for-llms#:~:text=,on%20embeddings%20from%20language%20models)
- [RAG Techniques | IBM Think](https://www.ibm.com/think/topics/rag-techniques#:~:) -->