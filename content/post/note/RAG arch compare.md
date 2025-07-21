---
title: 三種 RAG 架構比較與應用解析 — Naive、Advanced、Modular RAG 差異整理
description: 系統性比較 Naive RAG、Advanced RAG 與 Modular RAG 三種檢索增強生成（RAG）架構，解析其組成、技術細節、應用場景與優劣，協助選擇最適合的 RAG 解決方案。
slug: rag-type-compare-note
date: 2025-07-21 09:16:00+0800
categories:
    - note
tags:
    - AI
    - Retrieval-Augmented Generation
    - RAG
    - Research Summary
weight: 1
---

# 三種 RAG 技術架構比較：Naive RAG、Advanced RAG 與 Modular RAG

本文比較《Retrieval-Augmented Generation for Large Language Models: A Survey》中提出的三種檢索增強生成（RAG）技術架構：Naive RAG、Advanced RAG 和 Modular RAG。RAG 旨在結合大型語言模型（LLM）的內部知識與外部資料檢索，以提升事實正確性與時效性。這三種架構代表了 RAG 技術的演進路徑，各自引入不同模組與策略來克服先前架構的侷限。本文將從架構組成、實作方式、技術細節、應用場景與優劣比較等面向，深入剖析三類架構的差異與適用性。

---

## 架構組成與流程差異

### Naive RAG

最早期且基礎的 RAG 架構，僅包含索引（Indexing）、檢索（Retrieval）與生成（Generation）三個串連模組。流程為：資料向量化 → 檢索前 $K$ 個相關片段 → 查詢與檢索結果一併餵給 LLM 產生回答。此架構流程簡單、模組單一，缺乏查詢優化或反饋機制，適合快速原型開發。

![Naive RAG 架構圖](https://www.ibm.com/content/dam/connectedassets-adobe-cms/worldwide-content/creative-assets/s-migr/ul/g/e0/d6/naive-rag.png)


### Advanced RAG

在 Naive 基礎上增加前處理與後處理模組，如查詢優化、重排序、內容過濾/壓縮等。流程仍為索引→檢索→生成，但在檢索前後插入優化步驟，提升檢索品質與生成相關性。組件包含查詢改寫、混合檢索、重排序等，能針對性強化檢索與生成階段。

![Advanced RAG 架構圖](https://www.ibm.com/content/dam/connectedassets-adobe-cms/worldwide-content/creative-assets/s-migr/ul/g/8f/cb/advances-rag.png)
### Modular RAG

最新階段，強調積木式模組化設計。除繼承前述流程外，允許多輪檢索-生成、平行資訊融合、自適應流程等。可靈活增減如網路搜尋、長程記憶、路由決策等模組，流程可重組、迭代或分支，適應複雜多變的任務需求。

![Modular RAG 架構圖](https://www.ibm.com/content/dam/connectedassets-adobe-cms/worldwide-content/creative-assets/s-migr/ul/g/a7/e6/modular-rag.component.crop-16by9-m.ts=1740501066286.png/content/adobe-cms/us/en/think/topics/rag-techniques/jcr:content/root/table_of_contents/body-article-8/image_1228195012)

---

## 實作方式與系統特性

- **Naive RAG**：實作最直接，僅需嵌入模型、向量資料庫與 LLM。模組線性串接，無需微調，部署維護成本低，適合簡單應用。
- **Advanced RAG**：需引入查詢優化、重排序等模組，常用 LlamaIndex、LangChain 等框架。系統複雜度提升，需調校多個子系統，適合中等複雜度任務。
- **Modular RAG**：高度模組化，常用流水線編排框架。每個功能獨立封裝，系統可為有向圖結構，便於擴充與維護，但開發協調成本高。

---

## 核心技術細節

### 資料預處理與嵌入

- **Naive RAG**：文本清洗、切分、嵌入，建立向量索引，重點在語義表示。
- **Advanced RAG**：細粒度切分、滑動視窗、metadata 標註、混合嵌入（密集+稀疏），提升檢索覆蓋率與精確性。
- **Modular RAG**：動態資料處理，可即時抓取新資料、多模態資料、記憶模組自我增強，嵌入策略多元且可演化。

### 檢索策略與查詢優化

- **Naive RAG**：單輪語義相似度檢索，無查詢優化或多輪交互。
- **Advanced RAG**：查詢重寫/擴展、多次/混合檢索、重排序與過濾，提升檢索準確率與覆蓋率。
- **Modular RAG**：自適應多階段檢索、路由決策、平行多查詢、遞歸式檢索，根據任務動態調度檢索策略。

### 上下文融合與資訊增強

- **Naive RAG**：直接拼接查詢與檢索內容，無額外處理，易受雜訊干擾。
- **Advanced RAG**：重排序、壓縮、過濾、明確引導模型引用檢索內容，提升訊息品質。
- **Modular RAG**：多步融合、示範-搜索-預測、動態記憶、事後校驗，深度整合外部知識與模型推理。

### 回答生成與控制

- **Naive RAG**：LLM 直接生成，控制力弱，易出現幻覺或拼貼。
- **Advanced RAG**：提示工程、微調、反饋迴路、生成後過濾，強化可靠性與安全性。
- **Modular RAG**：示範模組、迭代生成、後處理校驗、用戶反饋迴路，實現嚴謹的生成管控。

---

## 適用場景與限制

- **Naive RAG**：適合原型、FAQ、內部知識庫等低複雜度場景，開發快但不適合高精度或多步推理任務。
- **Advanced RAG**：適用於醫療、法律、教育等知識密集型問答，能處理較大規模知識庫，但資源需求與維護成本較高。
- **Modular RAG**：適合大型企業、跨領域系統、需多階段推理或多源資訊整合的場景，擴展性與維護性最佳，但開發複雜度與初始成本高。

---

## 優劣比較

| 架構         | 實用性         | 可擴展性       | 維護成本     |
| ------------ | -------------- | -------------- | ------------ |
| Naive RAG    | 高（易用）     | 低～中         | 低           |
| Advanced RAG | 中（需專業）   | 中～高         | 中           |
| Modular RAG  | 低（複雜）     | 極高           | 高（初始），低（局部維護） |

- **Naive RAG**：簡單易用、成本低，但遇到複雜任務易達天花板。
- **Advanced RAG**：性能與複雜度平衡，適合多數專業應用，維護需專業投入。
- **Modular RAG**：彈性與擴展性最強，適合高端需求，但開發與協調成本高。

---

## 結論

三種 RAG 架構各有適用場景與優劣。Naive RAG 適合快速原型與簡單應用，Advanced RAG 適合專業領域與中大型知識庫，Modular RAG 則為高複雜度、需長期演化的系統提供最佳解決方案。選擇何種架構，應根據實際需求、資源與長期維護考量權衡取捨。

## Reference

- [Retrieval-Augmented Generation for Large Language Models: A Survey](https://arxiv.org/abs/2312.10997)
- [Three Paradigms of Retrieval-Augmented Generation (RAG) for LLMs](https://www.thecloudgirl.dev/blog/three-paradigms-of-retrieval-augmented-generation-rag-for-llms#:~:text=,on%20embeddings%20from%20language%20models)
- [RAG Techniques | IBM Think](https://www.ibm.com/think/topics/rag-techniques#:~:)