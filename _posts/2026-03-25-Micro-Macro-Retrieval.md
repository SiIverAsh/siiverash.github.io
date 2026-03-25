---
categories:
- emo
date: 2026-03-19 11:50:51 +0800
layout: post
tags:

title: Micro-Macro Retrieval 笔记
subject: ''
---





> ICLR 2026的论文 通过外部环境缓解幻觉，还有打标签

## 背景

现有的 RAG 模型虽然能够通过引入外部知识库来弥补模型的参数、记忆不足，但是再长文本语境下依旧面临 Lost in Lengthy Context 问题。

### 问题

1、**信息冗余与捕获困难**：外部检索得到的结果经常包含很多无关信息，这种冗余的输入会导致模型在生成输出的过程中难以精准定位真正的关键信息。

2、**长推理链导致的遗忘**：在生成长篇大论的过程中由于上下文长度的限制可能会导致模型忘记推理早期获得的中间结果，最终导致结论出现逻辑断裂或者事实漂移。

## 本文贡献

对比现有的多轮检索框架（ReAct、Self-RAG等）不同，M2R不仅仅检索外部文档（宏观），还通过在推理过程中建立 Key Information Repository 来让模型对自身生成的证据再利用。在生成回答的过程中，M2R会立即插入检索到的关键事实（微观），体现了从"粗粒度文档注入"到"细粒度事实锚定"的思想。

## 方法

边检索边生成

### 双阶段推理结构

推理过程被明确划分为两个阶段，通过特定的标签进行管理

#### 思维阶段

1、宏观检索（Macro Retrieval）：< macro_tool_call > 标签通过向外部 browser 或者知识库发起多轮 query，获取粗粒度背景证据。

2、关键信息保存（Key Information Saving）：模型在推理过程中识别出与答案直接相关的事实片段，用 < key_info_save > 标签以 json 格式存入 Key Information Repository。


#### 回答阶段

1、微观检索（Micro Retrieval）：模型发出 < micro_tool_call > 标签，请求 Key Information Repository 中的信息。

2、微观生成：检索到的事实通过 < micro_response > 返回，并用 \boxed{} 标记

### 基于 GRPO 的RL优化

是为了让模型学会tool call 和 利用 Key Information Repository 中的信息。

#### 优化目标

GRPO 不仅用于优化最终答案生成还监督模型的生成行为，包括何时调用检索、如何编写json仓库、如何在回答时引用仓库信息

#### 检索结果掩码（Retrieval Result Mask）：

在计算 loss 时，模型仅对自身生成的 Token ，对于外部返回的检索结果，用二进制掩码mt进行剔除，为的是防止错误的信用分配，保证稳定训练。 

#### KL 约束：

引入了 D<sub>kl</sub> 正则化项，可以保证更新后的策略π<sub>θ</sub>不会偏离原始基座模型太远。

### 自定义规则奖励模型

1、格式奖励：检查< macro_tool_call > 的使用是否合规，json 格式是否合法

2、答案奖励：
综合三个F1 Score：
- 最终答案准确性（s<sub>final</sub>）
- 关键信息准确性（s<sub>key</sub>）
- 一致性得分（s<sub>cons</sub>）


## 实验

- 四个多跳 QA 基准：Hotpot （多样化推理）、2WikiMutiHopQA（结构化推理）、MuSiQue（高难度组合推理）、Bamboogle（两步推理挑战）
- 模型底座： Qwen2.5-3B-Instruct、Qwen2.5-7B-Instruct
- 训练数据：MuSiQue 的训练集
- 检索环境：基于 FlashRAG 构建
- 底层知识库：2018.12 版本的 Wikipedia 快照

## 结果

1、准确性大幅提升

| 基准测试 | Qwen2.5-7B-ReSearch (EM) | Qwen2.5-7B-M2R (EM) | 提升幅度 (%) |
|----------|--------------------------|----------------------|--------------|
| HotpotQA | 43.52                    | 65.98                | +22.46       |
| 2Wiki    | 54.22                    | 57.01                | +2.79        |
| MuSiQue  | 22.30                    | 24.12                | +1.82        |
| Bamboogle| 42.40                    | 56.89                | +14.49       |

2、长上下文幻觉抑制

本文构造了 HotpotQA-2Q 和 HotpotQA-3Q 任务（即将多个问题合并为一个推理实例），传统 RAG 和 ReSearch 的幻觉率迅速上升，而 M2R 依旧保持在稳定的高准确率 。

