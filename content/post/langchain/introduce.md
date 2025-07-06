---
title: Introduction langchain
# image: "/unsplash.jpg"
description: 本文介紹 LangChain 框架的基本概念。
slug: introlangchain
date: 2025-07-06 00:00:00+0000
categories:
    - tutorial
tags:
    - langchain
    - AI
    - Large language model
    - LLM
weight: 1       # You can add weight to some posts to override the default sorting (date descending)
---

# 介紹 LangChain
LangChain 為 2022 年發布的開源框架，主要用於開發由語言模型驅動的應用程式，可連接多種語言模型與外部工具。

## 優點
* 開源工具
* 支持多種開源模型
* 可整合多項外部服務

## 主要組件
* 模型 (Models)
    * 語言模型、文本嵌入模型等等...
* 記憶體 (Memory)
    * 短期與長期記憶，用於儲存與檢索聊天歷史
    * 包含對話緩衝記憶體、實體記憶體、向量儲存記憶體
* 代理 (Agents)
    * 推理引擎
    * 可以根據給定的情境與數據做出合理的決策與推理

LangChain 藉由這些組件連結各種模型與工具，以達成檢索與分析數據，並可進行個性化的訂製。

<!-- 從網頁中作文本提取，並自動生成總結文稿 -->

## 主要解決問題
* 如何格式化輸出?
* 如何輸出很長的文本?
* 如何呼叫多次 api?
* 如何使 api 能呼叫外部的服務、工具?
* 如何進行標準化的開發?
* ...

# Reference
* https://www.youtube.com/watch?v=feFp5TbrVMo
* https://www.youtube.com/playlist?list=PLAr9oL1AT4OElxInUijCzCgU3CpgHTjTI
