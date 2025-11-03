---
title: Data mining
description: 由資料探勘課程中講義改寫並整理而成。
slug: Data-mining
date: 2025-11-03 11:20:00+0800
categories:
    - note
tags:
    - Data mining

weight: 1
---
> 這份簡報檔案是關於「進階資料探勘」(Advanced Data Mining) 課程的介紹，授課教師為莊秀敏 (Hsiu-Min Chuang) 教授，隸屬於中原大學資訊工程學系。

# 為什麼需要資料探勘?
* 動機： 資訊的爆炸性增長（從 TB 到 PB 等級）。我們處於「資料充斥 (drowning in data)，但缺乏知識 (starving for knowledge)」的狀態 。
* 需求：資料探勘的出現是為了「自動化分析巨量資料集」。

# 什麼是資料探勘?
* 定義：資料探勘是「從巨量資料中，萃取出有趣的 (非顯而易見、隱含的、先前未知且具有潛在用途的) 模式或知識」。
* 別名：它也被稱為 KDD (資料庫知識發現)、知識萃取、資料/模式分析等 。

---

## Knowledge Discovery (KDD) Process
1. 資料整合 (Data Integration) 
2. 資料清理 (Data Cleaning) 
3. 資料倉儲 (Data Warehouse) 
4. 選取任務相關資料 (Task-relevant Data / Selection) 
5. 資料探勘 (Data Mining) 
6. 模式評估 (Pattern Evaluation) 
7. 知識呈現 (Knowledge)

---

## 資料探勘的功能 (Patterns/Functions)
### 概化 (Generalization)  
將低層次、詳細的資料，轉換為高層次、更易於理解的摘要資訊，助於從宏觀的角度來理解資料的總體特徵。
1. 資訊整合與資料倉儲建構：  
* 將來自不同來源的資料進行清理 (cleaning)、轉換 (transformation) 和整合 (integration)。
* 目標是建立一個多維度資料模型 (multidimensional data model)，這也是資料倉儲 (Data Warehouse) 的基礎。

2. 資料方塊技術：
* 使用可擴展的方法 (Scalable methods) 來預先計算 (computing / materializing) 各種維度組合下的彙總值 (aggregates)。

3. 多維度概念描述：  
這是概化的具體應用，主要分為兩種：  
* 特徵化 (Characterization)： 描述某一特定資料群組的總體特徵。例如：總結「高額度信用卡客戶」的共同特徵（如年齡、收入、職業分佈）。
* 區辨 (Discrimination)： 比較兩個或多個不同資料群組之間的特徵差異 。例如，投影片中的例子：比較「乾燥地區 (dry region)」與「潮濕地區 (wet region)」在特性上的差異 。

---
### 關聯性分析(Association Analysis)  
找出資料中經常一起出現的項目，例如「買了尿布的顧客，也很常一起買啤酒」。
* 頻繁樣式 (Frequent patterns)： 指經常一起出現的項目組合 (itemsets)。例如，在超市中，「尿布」和「啤酒」是否經常被一起購買？
* 關聯規則 (Association rule)： 用來表示項目間關聯性的規則。
* 「關聯 (Association)」或「相關 (Correlation)」不等於「因果關係 (Causality)」。(買尿布並不會導買啤酒)。

---
### 分類 (Classification)  
為一項「監督式學習」任務，根據已知的訓練資料建立模型，用以預測未知資料的類別標籤。例如判斷信用卡交易是否為盜刷。

* 流程：
    1. 建立模型：依據一組已知的「訓練範例 (training examples)」來建立一個模型或函數。
    2. 預測未來：使用這個模型來描述和區分不同的類別，並預測「未知類別標籤」的資料。
* 範例：
    * 根據「氣候 (climate)」來分類國家。
    * 根據「油耗 (gas mileage)」來分類汽車。
* 典型方法：決策樹 (Decision trees)、貝氏分類 (naïve Bayesian)、支持向量機 (SVM)、神經網路 (neural networks)、迴歸 (logistic regression) 等。
* 典型應用：信用卡詐欺偵測、精準行銷、疾病分類、網頁分類等。

---
### 分群 (Cluster Analysis)  
為一項「非監督式學習」任務，在沒有類別標籤的情況下(非監督式，將資料依照「群內相似度高、群間相似度低」的原則，自動分成數個群組)。  
* 基本原則：
    * 最大化「群內」相似度 (Maximizing intra-class similarity)：同一群集內的資料點彼此盡可能相像。
    * 最小化「群間」相似度 (Minimizing interclass similarity)：不同群集之間的資料點彼此盡可能不同。

* 範例： 對房屋資料進行分群，以找出其分佈模式。

---
### 離群值分析 (Outlier Analysis)  
偵測出「不符合資料一般行為」的資料，可用於詐欺偵測或稀有事件分析。

* 離群值 (Outlier)：是一個資料物件，其行為不符合資料的「一般行為 (general behavior)」。
* 重要概念：離群值是「雜訊 (Noise)」還是「特例 (Exception)」？「一個人的垃圾可能是另一個人的寶藏 (One person's garbage could be another person's treasure)」。這意味著離群值雖然異常，但可能蘊含著非常重要的資訊。

---
### 時間和順序 (Time and Ordering) 相關的資料探勘功能  
分析有時間順序的模式 (如先買A、再買B) ，或是結構性資料 (如社群網路、圖形)。

1. 序列、趨勢與演化分析 (Sequence, trend and evolution analysis)  
* 趨勢、時間序列與偏差分析 (Trend, time-series, and deviation analysis)： 這類分析著重於資料隨時間的變化趨勢，例如使用「迴歸 (regression)」來進行「數值預測 (value prediction)」。

* 序列模式探勘 (Sequential pattern mining)： 找出經常「依序發生」的事件模式。
    * 例如：顧客「先 買了數位相機，然後 才去買大容量 SD 記憶卡」。這和關聯規則 (同時購買) 不同，這裡強調的是「先後順序」。

* 週期性分析 (Periodicity analysis)： 找出資料中重複出現的循環或週期 (例如：季節性銷售高峰)。

* 基序與生物序列分析 (Motifs and biological sequence analysis)： 找出在序列資料中 (例如 DNA 或蛋白質序列) 反覆出現的子序列或「基序 (motifs)」，包含「近似 (approximate)」或「連續 (consecutive)」的模式。

* 相似性分析 (Similarity-based analysis)： 比較不同時間序列或序列模式之間的相似度。

2. 探勘資料串流 (Mining data streams)  
資料串流的特性是：有順序性 (Ordered)、隨時間變化 (time-varying)，且可能是無限的 (potentially infinite)。例如：感測器資料、網站點擊流 (clickstreams) 或金融交易資料，這些資料必須即時且連續地進行分析。

---

# 認識你的資料
## 資料集的組成
* 一個資料集（Data Set）是由多個資料物件（Data Objects）所構成。
* 每個資料物件代表一個實體（Entity），也就是現實世界中可被觀察或分析的對象。

## 屬性描述資料物件
* 每個資料物件是由一組屬性（Attributes）來描述的。
* 在資料庫中，每一列（row）代表一個資料物件，每一欄（column）則代表一個屬性。

## 資料集的類型
### 記錄型資料
* 關聯式記錄（Relational Records）：如資料庫中的表格，每列為一筆資料，每欄為一個屬性。

* 資料矩陣（Data Matrix）：例如數值矩陣或交叉表（crosstabs），常見於統計分析。

* 文件資料（Document Data）：文字文件可轉換為「詞頻向量（Term-Frequency Vector）」

    |    | team | coach | ball |
    | ---- | ---- | ---- | ---- |
    | Document1 | 3 | 0 | 5 |
    | Document2 | 0 | 7 | 0 |
    | Document3 | 0 | 1 | 0 |


* 交易資料（Transaction Data）：每筆交易包含一組項目，例如購物籃中的商品。
    | TID | Items |
    | ---- | ---- |
    | 1 | Bread, Coke, Milk |
    | 2 | Beer, Bread |
    | 3 | Beer, Coke, Diaper, Milk |

### 圖形與網路資料
這類資料具有節點與連結的結構。  
* 全球資訊網（World Wide Web）：網頁之間的超連結形成網路結構。
* 社群或資訊網路（Social/Information Networks）：如 Facebook、LinkedIn 的人際關係圖。
* 分子結構（Molecular Structures）：化學分子可表示為原子節點與鍵結邊。

### 有序資料
這類資料具有時間或順序性。  
* 影像資料（Video Data）：由一連串影像構成。
* 時間序列資料（Temporal Data）：如股價、氣溫等隨時間變化的資料。
* 序列資料（Sequential Data）：如顧客購物行為序列、網頁瀏覽路徑。

### 空間、影像與多媒體資料
這類資料通常具有位置或視覺特性。

* 空間資料（Spatial Data）：如地圖、地理資訊系統（GIS）。
* 影像與影片資料（Image & Video Data）：如照片、監視器錄影、醫學影像。

## 屬性（Attributes）概念與分類
* 屬性（也稱為維度、特徵、變數）是資料物件的特徵欄位。
* 每個屬性代表一種特性，例如：顧客的 ID、姓名、地址。
* 在資料表中，每一欄（column）就是一個屬性。

### 屬性類型
* 名目型屬性（Nominal）
    * 表示分類或名稱，無順序性。
    * 適合用於分類分析。

* 二元屬性（Binary）
    * 只有兩種狀態，通常以 0 和 1 表示。
    * 對稱二元（Symmetric Binary）：兩種狀態同等重要，例如性別。
    * 非對稱二元（Asymmetric Binary）：其中一種狀態較重要，例如醫療檢測結果（陽性 vs 陰性），通常將重要狀態設為 1。

* 序位型屬性（Ordinal）
    * 屬性值有明確的順序，但無法量化差距。
    * 範例：尺寸 = {小、中、大}

* 數值型屬性（Numeric）
    * 區間尺度（Interval-Scaled）
        * 有順序，且單位間距相等，無絕對零點。
        * 例，日期。
    * 比例尺度（Ratio-Scaled）
        * 有順序，且單位間距相等，有絕對零點。
        * 例，長度、金額、計數。

* 離散與連續屬性
    * 離散屬性（Discrete）：只有有限或可數無限個值。
    * 連續屬性（Continuous）：屬性值為實數，通常以浮點數表示，實際上受限於儀器精度。


## 結構化資料的重要特性
### 維度性（Dimensionality）
* 指資料中屬性的數量，也就是每筆資料的欄位數。

### 稀疏性（Sparsity）
* 指資料中大多數欄位值為零或缺值，只有少數欄位有意義的值。
* 在這種情況下，「有出現」比「沒出現」更重要。

### 解析度（Resolution）
* 指資料的尺度或精細程度。

### 分布性（Distribution）
* 指資料值的分布情形，包括集中趨勢與離散程度。
    * 集中性（Centrality）：如平均值、中位數，反映資料的中心位置。
    * 離散性（Dispersion）：如變異數、標準差，反映資料的擴散程度。



<!-- 
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

三種 RAG 架構各有適用場景與優劣。Naive RAG 適合快速原型與簡單應用，Advanced RAG 適合專業領域與中大型知識庫，Modular RAG 則為高複雜度、需長期演化的系統提供最佳解決方案。選擇何種架構，應根據實際需求、資源與長期維護考量權衡取捨。 -->

<!-- ## Reference

- [Retrieval-Augmented Generation for Large Language Models: A Survey](https://arxiv.org/abs/2312.10997)
- [Three Paradigms of Retrieval-Augmented Generation (RAG) for LLMs](https://www.thecloudgirl.dev/blog/three-paradigms-of-retrieval-augmented-generation-rag-for-llms#:~:text=,on%20embeddings%20from%20language%20models)
- [RAG Techniques | IBM Think](https://www.ibm.com/think/topics/rag-techniques#:~:) -->