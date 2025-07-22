---
title: LightRAG 論文導讀 — Simple and Fast Retrieval-Augmented Generation 筆記
description: 導讀《LightRAG-Simple and Fast Retrieval-Augmented Generation》論文，解析其結合知識圖譜與雙層檢索策略的高效 RAG 架構設計與應用。
slug: lightrag-paper-review
date: 2025-07-22 05:27:00+0800
categories:
  - note
tags:
  - AI
  - Retrieval-Augmented Generation
  - RAG
  - Graph RAG
  - LightRAG
  - Knowledge Graph
  - Research Summary
weight: 1
---

> 本文整理自：[LightRAG: Simple and Fast Retrieval-Augmented Generation](https://arxiv.org/abs/2410.05779)  
> 作者：Zirui Guo, Lianghao Xia, Yanhua Yu, Tu Ao, Chao Huang  
> 發佈於 arXiv，2024年10月

# 摘要
《LightRAG: Simple and Fast Retrieval-Augmented Generation》提出一種輕量且高效的檢索增強生成（RAG）框架，透過結合圖結構知識與雙層檢索策略來提升大型語言模型的回應品質。現有 RAG 系統常受限於扁平資料表徵與缺乏上下文關聯，導致回答內容片段化、無法捕捉實體之間的複雜關係。為了解決這些問題，LightRAG 在文本索引和檢索過程中引入知識圖譜，並採用雙層（低階/高階）檢索架構，同時整合圖結構與向量表示以高效檢索相關實體及其關係。此框架還包含一套漸進式更新演算法，能及時融合新知識，確保模型在動態資料環境中保持有效和即時。實驗結果顯示，相較既有方法，LightRAG 在檢索準確率與效率上都有顯著提升。研究已開源並提供原始碼供社群使用。





