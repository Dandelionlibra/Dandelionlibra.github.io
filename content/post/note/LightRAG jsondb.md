---
title: LightRAG API Server 教學：快速上手指南
description: 未完成 本文提供 LightRAG 使用 JSON 作為資料庫時的檔案儲存基本介紹。
slug: lightrag-json-db
date: 2025-08-06 09:03:00+0800
categories:
    - note
tags:
    - AI
    - Retrieval-Augmented Generation
    - RAG
    - LightRAG
    - JSON
weight: 1
---

# LightRAG API Server 教學：快速上手指南

[LightRAG](https://github.com/HKUDS/LightRAG) 是一個輕量級、模組化的 RAG（檢索增強生成）框架，旨在簡化 RAG 應用的開發與部署。其內建的 API Server 遵循 OpenAI API 標準，並提供一套完整的 Web UI API 來管理文件與知識圖譜，讓開發者能輕易地將自訂的 RAG 流程封裝成服務，並與現有生態系無縫接軌。本文將引導初學者完成從環境設定到 API 呼叫的完整流程。

---



## kv_store_doc_status.json  
功能：紀錄每份文件在知識庫中的處理狀態與相關資訊。

**主要欄位**
* `__id__`：文件的唯一識別碼。
* `file_path`：原始文件檔名或路徑。
* `status`：處理狀態（如：processed, pending, error）。
* `updated_at`：最後更新時間。

**用途**
* 監控文件是否已完成切割、嵌入與存入向量資料庫。
* 方便追蹤與除錯。

---
## kv_store_full_docs.json
功能：儲存完整的原始文檔，作為語義檢索的來源。

**主要欄位**
* `__id__`：文件唯一 ID。
* `file_path`：檔案來源路徑。
* `content`：完整文件的文字內容。
* `metadata`：附屬資訊（如標題、作者、分類）。

**用途**
* 保留完整語境，便於 LLM 在回答時回溯全文。
* 提供「非分塊」的全文檢索。

---

## kv_store_llm_response_cache.json
功能：作為 LLM 查詢結果的快取，避免重複計算。

**主要欄位**
* `query`：使用者輸入的查詢字串。
* `response`：LLM 生成的回答。
* `timestamp`：快取生成時間。
* `hit_count`：該查詢被重複使用的次數。

**用途**

* 提升系統效能，減少模型重複推理。
* 允許分析熱門查詢。

---

## kv_store_text_chunks.json
功能：儲存將文件切割後的小片段（chunks），方便向量檢索。

**主要欄位**
* `__id__`：文本片段 ID。
* `file_path`：來源文件名稱。
* `chunk_index`：片段順序號。
* `content`：片段內容文字。
* `embedding_vector`（可選）：對應的向量嵌入。

**用途**
* 支援語意檢索（RAG: Retrieval-Augmented Generation）。
* 每個 chunk 對應一組 embedding，利於近似搜尋。


存有 token 數。


---

## vdb_chunks.json
功能：儲存經嵌入處理的文本向量（Vector DB 核心）。

**主要欄位**

* `__id__`：chunk 的唯一識別碼。
* `embedding_dim`：向量維度（如 1024）。
* `embedding_vector`：嵌入向量。
* `content`：對應文本。
* `source_id`：來源 chunk 的 ID。

**用途**
* 提供高效相似度搜尋。
* 是 RAG 系統的核心檢索資料來源。

---

## vdb_entities.json
功能：儲存從文本中抽取的命名實體與相關描述。

**主要欄位**
* `__id__`：實體 ID。
* `entity_name`：實體名稱（如「林致远」「阿墨」）。
* `content`：實體的描述或定義。
* `file_path`：來源檔案。
* `source_id`：對應文本片段 ID。
* `__created_at__`：建立時間戳。
* `embedding_dim`：嵌入向量維度（如 1024）。

**特色**
* 一個實體可能來自多個文本片段，用 <SEP> 分隔。
* 可支援多語言或多版本（如 知一书屋 vs 知一書屋）。

**用途**
* 為知識圖譜中的節點（entities）。
* 支援語義關聯檢索與上下文補全。

---

## vdb_relationships.json
功能：儲存實體之間的語義關係，形成知識圖譜 (Knowledge Graph)。

**主要欄位**
* `__id__`：關係 ID。
* `src_id`：關係的起始實體名稱。
* `tgt_id`：關係的目標實體名稱。
* `content`：關係的描述與類別（可能包含多種語意標籤，如 companionship, ownership）。
* `file_path`：來源文件。
* `source_id`：對應的文本 chunk。
* `__created_at__`：建立時間。

**用途**
* 支援「語義圖譜檢索」，例如：  
  問「阿墨和林致远的關係？」 → 檢索 companionship 與 mysterious connection。
* 提供結構化的語意推理，補強向量檢索。

---

## 4. 總結
* kv_store* 系列 → 偏向文件與片段的管理、狀態與快取。
* vdb* 系列 → 偏向語義層面的知識圖譜與向量檢索。
* entities 與 relationships → 構成知識圖譜 (Knowledge Graph)。
* chunks 與 embeddings → 構成語意檢索的基礎。
