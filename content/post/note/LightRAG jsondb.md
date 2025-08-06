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

## 1. 環境設定與安裝


kv_store_doc_status.json
kv_store_full_docs.json
kv_store_llm_response_cache.json
kv_store_text_chunks.json
vdb_chunks.json
vdb_entities.json
vdb_relationships.json


---

## 4. 總結

LightRAG 的 API Server 提供了一個標準化且功能豐富的介面，讓開發者能將複雜的 RAG 流程部署為一個獨立服務。透過遵循 OpenAI 的 API 格式並提供完整的文件管理 API，它極大地降低了整合門檻，無論是進行快速原型設計，還是將其整合到現有的應用程式中，都變得非常方便。希望本篇教學能幫助您順利踏出使用 LightRAG 的第一步。
