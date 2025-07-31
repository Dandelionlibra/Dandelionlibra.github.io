---
title: GraphRAG vs LightRAG 
description: 比較兩種 RAG 的差異。
slug: graphrag-lightrag-compare
date: 2025-07-31 03:24:00+0800
categories:
  - note
tags:
  - AI
  - Retrieval-Augmented Generation
  - RAG
  - Graph RAG
  - LightRAG
weight: 1
---

# RAG 種類

## Native RAG
嘗試解決內部資訊缺失的問題。  
RAG 在回答前會先基於提問與資料庫中內容的語意相似度篩選出最具關連的段落 (chunk) 再將這些資訊傳給 LLM 進行回答，但受限於檢索到的 chunk 內容，因此若是詢問的問題比較全面，例如主題大綱等等，因為需要全面的資料內容，但檢索後卻使會提供給 LLM 部分內容而已，因此可預測回答準確率大概不高，但是若是法規等問題回答結果會更精確。

##


---

# 引言

## 現有 RAG 系統的局限性
* **依賴平面資料表示：** 許多方法依賴於平面資料表示（flat data representations），限制了它們根據實體之間複雜關係來理解和檢索資訊的能力。  

* **缺乏上下文感知：** 這些系統通常缺乏維持不同實體及其相互關係之間連貫性所需的上下文感知能力，導致回應可能無法完全解決用戶查詢。

  > 例：考慮用戶提問「電動車的興起如何影響城市空氣品質和大眾運輸基礎設施？」現有 RAG 方法可能檢索到關於電動車、空氣污染和公共交通挑戰的獨立文檔，但難以將這些信息綜合為一個連貫的回應。它們可能無法解釋電動車的普及如何改善空氣品質，進而可能影響公共交通規劃，用戶可能收到一個碎片化的答案，未能充分捕捉這些主題之間複雜的相互依賴關係。

## LightRAG 模型概述

增強了系統捕捉實體之間複雜相互依賴關係的能力，從而產生更連貫和上下文更豐富的回應。

* **高效雙層檢索策略：** 
  * 低層次檢索（low-level retrieval）： 側重於關於特定實體及其關係的精確資訊。
  * 高層次檢索（high-level retrieval）： 涵蓋更廣泛的主題和概念。
  * 優勢： 透過結合詳細和概念性檢索，LightRAG 有效適應多樣化的查詢範圍，確保用戶收到符合其特定需求的相關且全面的回應。

* **圖結構與向量表示的整合：** 透過將圖結構與向量表示整合在一起，本 LightRAG 促進了相關實體和關係的高效檢索，同時透過從所構建的知識圖中獲取相關結構信息，增強了結果的全面性。

## 本研究在 RAG 系統中的關注點  

<p align="center">
ℳ=(𝒢,ℛ=(φ,ψ)) <br>
ℳ​(q;𝒟)=𝒢​(q,ψ​(q;𝒟^)) <br>
𝒟^=φ​(𝒟)
</p>

* **全面信息檢索** (Comprehensive Information Retrieval)： 索引功能 ϕ(⋅) 必須善於提取全局信息，這對於增強模型有效回答查詢的能力至關重要。

* **高效且低成本檢索** (Efficient and Low-Cost Retrieval)： 索引化的資料結構 𝒟^ 必須能夠實現快速且具成本效益的檢索，以有效處理高容量的查詢。

* **快速適應數據變化** (Fast Adaptation to Data Changes)： 能夠迅速有效地調整數據結構以整合來自外部知識庫的新信息，這對於確保系統在不斷變化的信息環境中保持更新和相關性至關重要。

---

# 內文

## LightRAG 框架的整體架構
![LightRAG 框架總覽](https://raw.githubusercontent.com/HKUDS/LightRAG/refs/heads/main/README.assets/b2aaf634151b4706892693ffb43d9093.png)  
*圖 1. LightRAG 框架總覽（取自原論文）*

架構如圖 1 所示。  

流程從**原始文本塊**開始，這些文本塊首先透過**基於圖形的文本索引**（Graph-based Text Indexing）階段進行處理，過程包含幾個關鍵子組件：**實體與關係提取**（Entity & Rel Extraction）、**LLM 剖析**（LLM Profiling）和**去重**（Deduplication），最後的輸出是一個用於檢索的**索引圖**（Index Graph）。  
接著，Query LLM 接收輸入查詢，並從中生成**低層級關鍵字**（Low-level Keys，包括實體和關係）和**高層級關鍵字**（High-level Keys，包括語境和原始文本塊）。這些關鍵字隨後被送入**雙層級檢索範式**（Dual-level Retrieval Paradigm），此範式與「索引圖」和「原始文本塊」互動，以檢索相關資訊。最終，檢索到的資訊被傳回 Query LLM 進行檢索增強的答案生成（Retrieval-Augmented Answer Generation）。   
圖中展示了以「索引圖」作為核心儲存庫，這張圖不僅用來整理新資訊（索引），也用來尋找資訊（檢索），這代表系統不再只是儲存一堆零散的文字片段，而是將知識組織成一個有結構的網路，能更智慧地找出事物之間的關聯。  
此外，處理查詢的 LLM 在 LightRAG 多次出現，它不只負責生成最終答案，還會參與理解問題、引導系統去尋找相關資訊，並將找到的資料整合起來。


## 基於圖形的文本索引
LightRAG 透過將文件分割成更小、更易於管理的片段來增強檢索系統。這種策略允許快速識別和存取相關資訊，而無需分析整個文件 。隨後，系統利用大型語言模型（LLMs）來識別和提取各種實體（例如，名稱、日期、位置和事件）以及它們之間的關係 。透過這個過程收集到的資訊將用於創建一個全面的知識圖譜，突顯整個文件集合中的連結和見解。

圖形生成模組正式表示為 𝒟^=(𝒱^,ℰ^)=Dedupe∘Prof​(𝒱,ℰ),𝒱,ℰ=∪𝒟i∈𝒟Recog​(𝒟i)

---

# 實驗



---



---

# Reference

- [LightRAG: Simple and Fast Retrieval-Augmented Generation-ar5iv 可視化版本](https://ar5iv.labs.arxiv.org/html/2410.05779)
