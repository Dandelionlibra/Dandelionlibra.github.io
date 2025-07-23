---
title: BAAI/bge-reranker-v2-m3 — Hugging Face 官方整理
description: 簡單說明 FlagEmbedding 與 Hugging Face Transformers 實作 BGE Reranker 模型的差異與用途。
slug: bge-reranker-hf-flagembedding-note
date: 2025-07-23 03:51:00+0800
categories:
  - note
tags:
  - AI
  - Large language model
  - LLM
  - Reranker
  - FlagEmbedding
  - Hugging Face
  - BGE
weight: 1
---

## Reranker 模型與函式庫使用差異筆記
這份筆記整理了 FlagEmbedding 和 Hugging Face Transformers 在實作不同 Reranker 模型（標準型、LLM 型、分層式 LLM 型）時的關鍵差異。

---

### 核心實作比較
#### FlagEmbedding
`FlagEmbedding` 函式庫提供了更簡潔、高度封裝的 API，適合快速整合和高效能應用。

1. 標準 Reranker (bge-reranker-base / large / v2-m3)
* 方法: 使用 `FlagReranker` 類別。
* 特點: 最直接、優化的方法，簡化模型載入和計算。
* 程式碼範例:
   ``` python
   from FlagEmbedding import FlagReranker
   # Setting use_fp16 to True speeds up computation with a slight performance degradation
   reranker = FlagReranker('BAAI/bge-reranker-v2-m3', use_fp16=True)

   score = reranker.compute_score(['query', 'passage'])
   print(score) # -5.65234375

   # Map the scores into 0-1 by set "normalize=True", which will apply sigmoid function to the score
   score = reranker.compute_score(['query', 'passage'], normalize=True)
   print(score) # 0.003497010252573502

   scores = reranker.compute_score([['what is panda?', 'hi'], ['what is panda?', 'The giant panda (Ailuropoda melanoleuca), sometimes called a panda bear or simply panda, is a bear species endemic to China.']])
   print(scores) # [-8.1875, 5.26171875]

   # set "normalize=True"
   scores = reranker.compute_score([['what is panda?', 'hi'], ['what is panda?', 'The giant panda (Ailuropoda melanoleuca), sometimes called a panda bear or simply panda, is a bear species endemic to China.']], normalize=True)
   print(scores) # [0.00027803096387751553, 0.9948403768236574]

   ```

2. LLM-based Reranker
* 方法: 利用 `FlagLLMReranker` 類別。
* 特點: 將大型語言模型（如 Llama）作為 Reranker，利用其語言理解能力進行細緻排序。需要大量 VRAM (>40G)。
* 程式碼範例:
   ``` python
   from FlagEmbedding import FlagLLMReranker
   # Setting use_fp16 to True speeds up computation with a slight performance degradation
   reranker = FlagLLMReranker('BAAI/bge-reranker-v2-gemma', use_fp16=True) 

   score = reranker.compute_score(['query', 'passage'])
   print(score)

   scores = reranker.compute_score([['what is panda?', 'hi'], ['what is panda?', 'The giant panda (Ailuropoda melanoleuca), sometimes called a panda bear or simply panda, is a bear species endemic to China.']])
   print(scores)

   ```

3. LLM-based Layerwise Reranker
* 方法: 透過 FlagLLMReranker 的 compute_score_layerwise 方法。
* 特點: 可從 LLM 的不同層獲取分數，提供對模型決策過程的深入洞察。
* 程式碼範例:
   ``` python
   from FlagEmbedding import LayerWiseFlagLLMReranker
   # Setting use_fp16 to True speeds up computation with a slight performance degradation
   reranker = LayerWiseFlagLLMReranker('BAAI/bge-reranker-v2-minicpm-layerwise', use_fp16=True) 
   
   # Adjusting 'cutoff_layers' to pick which layers are used for computing the score.
   score = reranker.compute_score(['query', 'passage'], cutoff_layers=[28]) 
   print(score)

   scores = reranker.compute_score([['what is panda?', 'hi'], ['what is panda?', 'The giant panda (Ailuropoda melanoleuca), sometimes called a panda bear or simply panda, is a bear species endemic to China.']], cutoff_layers=[28])
   print(scores)
   ```

---

#### Hugging Face Transformers
Hugging Face Transformers 函式庫提供了更通用和靈活的方法，適合需要深度自訂和學術研究的場景。
1. 標準 Reranker (bge-reranker-base / large / v2-m3)
* 方法: 載入 AutoTokenizer 和 AutoModelForSequenceClassification。
* 特點: 標準流程，提供更多自訂空間。
* 程式碼範例:
   ``` python
   import torch
   from transformers import AutoModelForSequenceClassification, AutoTokenizer

   tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-reranker-v2-m3')
   model = AutoModelForSequenceClassification.from_pretrained('BAAI/bge-reranker-v2-m3')
   model.eval()

   pairs = [['what is panda?', 'hi'], ['what is panda?', 'The giant panda (Ailuropoda melanoleuca), sometimes called a panda bear or simply panda, is a bear species endemic to China.']]
   with torch.no_grad(): # 無梯度下降
      inputs = tokenizer(pairs, padding=True, truncation=True, return_tensors='pt', max_length=512)
      scores = model(**inputs, return_dict=True).logits.view(-1, ).float()
      print(scores)
   ```

2. LLM-based Reranker
* 方法: 載入 AutoTokenizer 和 AutoModelForCausalLM。
* 特點: 需要手動處理模型輸出以獲得分數，提供最大的靈活性和控制力。
* 程式碼範例:
   ``` python
   import torch
   from transformers import AutoModelForCausalLM, AutoTokenizer

   def get_inputs(pairs, tokenizer, prompt=None, max_length=1024):
      if prompt is None:
         prompt = "Given a query A and a passage B, determine whether the passage contains an answer to the query by providing a prediction of either 'Yes' or 'No'."
      sep = "\n"
      prompt_inputs = tokenizer(prompt,
                                 return_tensors=None,
                                 add_special_tokens=False)['input_ids']
      sep_inputs = tokenizer(sep,
                              return_tensors=None,
                              add_special_tokens=False)['input_ids']
      inputs = []
      for query, passage in pairs:
         query_inputs = tokenizer(f'A: {query}',
                                    return_tensors=None,
                                    add_special_tokens=False,
                                    max_length=max_length * 3 // 4,
                                    truncation=True)
         passage_inputs = tokenizer(f'B: {passage}',
                                    return_tensors=None,
                                    add_special_tokens=False,
                                    max_length=max_length,
                                    truncation=True)
         item = tokenizer.prepare_for_model(
               [tokenizer.bos_token_id] + query_inputs['input_ids'],
               sep_inputs + passage_inputs['input_ids'],
               truncation='only_second',
               max_length=max_length,
               padding=False,
               return_attention_mask=False,
               return_token_type_ids=False,
               add_special_tokens=False
         )
         item['input_ids'] = item['input_ids'] + sep_inputs + prompt_inputs
         item['attention_mask'] = [1] * len(item['input_ids'])
         inputs.append(item)
      return tokenizer.pad(
               inputs,
               padding=True,
               max_length=max_length + len(sep_inputs) + len(prompt_inputs),
               pad_to_multiple_of=8,
               return_tensors='pt',
      )

   tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-reranker-v2-gemma')
   model = AutoModelForCausalLM.from_pretrained('BAAI/bge-reranker-v2-gemma')
   yes_loc = tokenizer('Yes', add_special_tokens=False)['input_ids'][0]
   model.eval()

   pairs = [['what is panda?', 'hi'], ['what is panda?', 'The giant panda (Ailuropoda melanoleuca), sometimes called a panda bear or simply panda, is a bear species endemic to China.']]
   with torch.no_grad():
      inputs = get_inputs(pairs, tokenizer)
      scores = model(**inputs, return_dict=True).logits[:, -1, yes_loc].view(-1, ).float()
      print(scores)
   ```

3. LLM-based Layerwise Reranker
* 方法: 透過手動存取 AutoModelForCausalLM 的隱藏層輸出或注意力權重，並自行計算分數。
* 特點: 提供對 LLM 內部決策過程最細緻的控制和分析，但實作複雜度高，需要深入理解模型架構。
* 程式碼範例:
   ``` python
   import torch
   from transformers import AutoModelForCausalLM, AutoTokenizer

   def get_inputs(pairs, tokenizer, prompt=None, max_length=1024):
      if prompt is None:
         prompt = "Given a query A and a passage B, determine whether the passage contains an answer to the query by providing a prediction of either 'Yes' or 'No'."
      sep = "\n"
      prompt_inputs = tokenizer(prompt,
                                 return_tensors=None,
                                 add_special_tokens=False)['input_ids']
      sep_inputs = tokenizer(sep,
                              return_tensors=None,
                              add_special_tokens=False)['input_ids']
      inputs = []
      for query, passage in pairs:
         query_inputs = tokenizer(f'A: {query}',
                                    return_tensors=None,
                                    add_special_tokens=False,
                                    max_length=max_length * 3 // 4,
                                    truncation=True)
         passage_inputs = tokenizer(f'B: {passage}',
                                    return_tensors=None,
                                    add_special_tokens=False,
                                    max_length=max_length,
                                    truncation=True)
         item = tokenizer.prepare_for_model(
               [tokenizer.bos_token_id] + query_inputs['input_ids'],
               sep_inputs + passage_inputs['input_ids'],
               truncation='only_second',
               max_length=max_length,
               padding=False,
               return_attention_mask=False,
               return_token_type_ids=False,
               add_special_tokens=False
         )
         item['input_ids'] = item['input_ids'] + sep_inputs + prompt_inputs
         item['attention_mask'] = [1] * len(item['input_ids'])
         inputs.append(item)
      return tokenizer.pad(
               inputs,
               padding=True,
               max_length=max_length + len(sep_inputs) + len(prompt_inputs),
               pad_to_multiple_of=8,
               return_tensors='pt',
      )

   tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-reranker-v2-minicpm-layerwise', trust_remote_code=True)
   model = AutoModelForCausalLM.from_pretrained('BAAI/bge-reranker-v2-minicpm-layerwise', trust_remote_code=True, torch_dtype=torch.bfloat16)
   model = model.to('cuda')
   model.eval()

   pairs = [['what is panda?', 'hi'], ['what is panda?', 'The giant panda (Ailuropoda melanoleuca), sometimes called a panda bear or simply panda, is a bear species endemic to China.']]
   with torch.no_grad():
      inputs = get_inputs(pairs, tokenizer).to(model.device)
      all_scores = model(**inputs, return_dict=True, cutoff_layers=[28])
      all_scores = [scores[:, -1].view(-1, ).float() for scores in all_scores[0]]
      print(all_scores)
   ```
---

### 核心概念解析
#### 標準 Reranker (Cross-Encoder)
* 原理: 將「查詢」和「文件」成對地同時輸入到模型中，模型利用兩者之間的交互資訊判斷相關性。
* 輸出: 單一相關性分數。
* 流程: 查詢 + 文件 → Cross-Encoder 模型 → 相關性分數

#### LLM-based Reranker
* 原理: 使用完整的大型語言模型（LLM）作為 Reranker，利用其龐大知識和推理能力理解深層語義關係。
* 輸出: 通常透過特定 token（如 [Yes] 或 [No]）的機率計算分數。
* 流程: 查詢 + 文件 → 大型語言模型 (LLM) → 基於生成機率的分數

#### 總結與比較

| 比較維度       | FlagEmbedding                        | Hugging Face Transformers                |
|---------------|--------------------------------------|------------------------------------------|
| 易用性         | 高（API 封裝良好）                   | 中（需要更多手動設定）                   |
| 靈活性         | 中（專為 Reranking 優化）             | 高（可完全自訂流程）                     |
| 特色功能       | Layerwise 分數計算                   | 與整個 Hugging Face 生態系無縫接軌       |
| 推薦使用情境   | 需要快速實現高效能 Reranking 的應用   | 需要深度自訂模型行為或進行學術研究       |

