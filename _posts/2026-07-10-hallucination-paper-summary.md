---
categories:
- paper
date: 2026-07-10 23:31:30 +0800
layout: post
tags:
- 幻觉
title: 找方法参考的论文
subject: ''
---







> 找点方法


| 序号 | 论文标题 | 方法简述 |
|---|---|---|
| 1 | **HIVE: Understanding Post-Hallucination Reasoning in Vision Language Models** | 研究“幻觉出现之后”的推理过程；构造真实 caption 和幻觉 caption 的对照输入，分析幻觉语义进入上下文后如何影响模型后续判断。 |
| 2 | **PRISM: Probing Reasoning, Instruction, and Source Memory in LLM Hallucinations** | 提出一个幻觉诊断 benchmark，把幻觉拆成知识错误、知识缺失、推理错误、指令遵循错误等类型，用来定位模型到底在哪个阶段出错。 |
| 3 | **The Hidden Life of Tokens: Reducing Hallucination of Large Vision-Language Models via Visual Information Steering** | 提出 VISTA，分析真实视觉 token 和幻觉 token 在生成过程中的 logit 排名变化，再用视觉引导向量和早层 logits 增强视觉相关 token。 |
| 4 | **Rethinking Visual Neglect: Steering via Context-Preference for MLLM Hallucination Mitigation** | 提出 CAS，把视觉依赖拆成“视觉 vs 参数知识”和“视觉 vs 文本上下文”两条轴，提取 VFV/MRV 向量后在中早层 MLP 注入残差进行干预。 |
| 5 | **Vision-Language Introspection: Mitigating Overconfident Hallucinations in MLLMs via Interpretable Bi-Causal Steering** | 提出 VLI，定位可能导致幻觉的视觉锚点，构造 Anchor-Only 和 Context-Only 两种状态做双因果 steering，同时校准模型过度自信。 |
| 6 | **Towards Interpretable Hallucination Analysis and Mitigation in LVLMs via Contrastive Neuron Steering** | 提出 CNS，用 SAE 把视觉表示分解成可解释神经元，区分 always-on neurons 和 image-specific neurons，再通过干预图像相关神经元减少幻觉。 |
| 7 | **Visual Evidence Prompting Mitigates Hallucinations in Large Vision-Language Models** | 先从图像中提取对象、属性、区域等视觉证据，再把这些 evidence 放进 prompt，引导模型基于可见证据回答。 |
| 8 | **Activation Steering Decoding: Mitigating Hallucination in Large Vision-Language Models through Bidirectional Hidden State Intervention** | 提出 ASD，在解码阶段对 hidden state 做双向干预：增强真实视觉相关方向，同时抑制幻觉相关方向。 |
| 9 | **Decoupling Contrastive Decoding: Robust Hallucination Mitigation in Multimodal Large Language Models** | 属于对比解码类方法，通过解耦视觉信号和语言先验，对 logits 进行校正，降低模型生成不存在对象的概率。 |
| 10 | **Mitigating Hallucinations in Vision-Language Models through Image-Guided Head Suppression** | 提出 SPIN，动态找出对图像 token 关注很低的 attention heads，并在推理时抑制这些 heads，减少视觉忽略导致的幻觉。 |
| 11 | **Pixels Versus Priors: Controlling Knowledge Priors in Vision-Language Models through Visual Counterfacts** | 构造 Visual CounterFact 反事实图像数据，分析模型何时依赖图像像素、何时依赖世界知识先验，并用 PvP steering vectors 控制这种倾向。 |
| 12 | **Sufficient Context: A New Lens On Retrieval Augmented Generation Systems** | 从“检索上下文是否足够支持回答”的角度分析 RAG，把错误区分为检索内容不充分、上下文利用失败或生成阶段幻觉。 |
| 13 | **Adaptive Residual-Update Steering for Low-Overhead Hallucination Mitigation in Large Vision Language Models** | 提出 RUDDER，在残差流中进行低开销的自适应 steering；根据当前生成状态动态更新干预方向或强度，从而减少 LVLM 在解码阶段产生对象幻觉。 |
|