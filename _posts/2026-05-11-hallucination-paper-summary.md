---
categories:
- paper
date: 2026-05-11 21:46:43 +0800
layout: post
tags:
- 幻觉
- ICLR
- EMNLP
- ACL
title: 研究幻觉的论文
subject: ''
---






> 列出了找到和看过的研究幻觉的论文，对应之前博客里提出的方法。

上次还想补充的一个方法：

## 对比解码策略

DoLa 我觉得是一篇很好的论文，用的是层间对比解码，它不是对比两个模型，而是对比一个模型的不同层，发现在低层模型内部更偏向语言、在高层更接近语义和事实知识，DoLa 就是用高层的logits减去低层的logits，它主要是要凸显高层的语义事实信号，削弱中间、低层的语言先验。

$\text{score}(y) = \log p_{\text{good}}(y) - \lambda \log p_{\text{bad}}(y)$

### 强模型与弱模型

其实最基础的对比解码策略是:

$\text{score}(y) = \log p_{\text{large}}(y) - \lambda \log p_{\text{small}}(y)$

意思就是让大模型作为expert，小模型作为amateur，让大模型减去小模型的容易生成的模板化、与事实知识差别较大的token，这种方法最初是用于提升开放式文本生成的质量的，但是很多的缓解幻觉的方法都用了这个思想。

### 有上下文与无上下文：CAD

CAD(Context-Aware Decoding) 常用于减少上下文问答或 RAG 中的幻觉

$\text{score}(y) =(1+\alpha)\log p(y \mid q, c)-\alpha \log p(y \mid q)$

其中$p(y \mid q, c)$是有问题和上下文的分布，$p(y \mid q)$是仅有问题的分布。作用是强化那些由上下文真正支持的 token ，削弱那些没有上下文也会被模型输出的 token。所以 CAD 适合 RAG 问答、文档问答、摘要生成、和需要忠实于上下文的任务。

### 原图与扰动图：VCD

VCD(Visual Contrastive Decoding) 用于缓解多模态幻觉。主要是对比原始图像+问题与扰动图像（加入噪声）+问题的区别，其原理主要是如果一个 token 只有在真实图像下概率高，那就是说它更可能来自于视觉证据，反之如果在图像被破坏后概率仍然高，那么就更可能是来着语言先验，一般 VCD 用于减少 vLLM 的 object hallucination。

## 各种方法的论文

### 知识事实缓解检测：claim分解、事实核查、LLM judge

| 论文                                                                                                     |                                会议、年份 | 对应方法            | 意义                                    |
| ------------------------------------------------------------------------------------------------------ | -----------------------------------: | --------------- | ------------------------------------- |
| **HaluEval: A Large-Scale Hallucination Evaluation Benchmark for Large Language Models**               |                           EMNLP 2023 | 幻觉检测 benchmark  | 构建了大规模人工标注和模型生成的幻觉样本，用于评估 LLM 是否能识别幻觉。 |
| **SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models** |                           EMNLP 2023 | 多采样一致性检测        | 不依赖外部数据库，通过多次采样回答之间是否一致来判断是否可能幻觉。     |
| **FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation**        |                           EMNLP 2023 | atomic facts 评估 | 把长文本拆成原子事实，然后计算有多少事实被可靠知识源支持。         |
| **FELM: Benchmarking Factuality Evaluation of Large Language Models**                                  | NeurIPS 2023 Datasets and Benchmarks | 细粒度事实性评测        | 对 LLM 生成结果做细粒度事实标注，世界知识、数学、推理等领域的知识都有。   |


### RAG/上下文不忠实检测

| 论文                                                                                                                       |      会议、年份 | 对应方法                             | 意义                                                                               |
| ------------------------------------------------------------------------------------------------------------------------ | ---------: | -------------------------------- | -------------------------------------------------------------------------------- |
| **RAGTruth: A Hallucination Corpus for Developing Trustworthy Retrieval-Augmented Language Models**                      |   ACL 2024 | RAG 幻觉标注数据集                      | 提供 case-level 和 word-level 幻觉标注，主要是研究回答是否被检索证据支持。                       |
| **MiniCheck: Efficient Fact-Checking of LLMs on Grounding Documents**                                                    | EMNLP 2024 | grounding document fact-checking | 用较小模型对 claim 是否能被 grounding documents 支持进行事实核查，目标是降低 GPT-4 fact-checking 的成本。 |
| **Lookback Lens: Detecting and Mitigating Contextual Hallucinations in Large Language Models Using Only Attention Maps** | EMNLP 2024 | attention map 检测                 | 只用 attention map 中“模型看上下文还是看自己生成内容”的比例来检测 contextual hallucination。              |


### 模型不确定性检测

| 论文                                                                                                |                      发表来源 | 对应方法                                | 意义                                          |
| ------------------------------------------------------------------------------------------------- | ------------------------: | ----------------------------------- | ------------------------------------------- |
| **Detecting hallucinations in large language models using semantic entropy**                      |               Nature 2024 | semantic entropy                    | 通过多次生成答案，并按语义聚类计算语义熵，检测 confabulation 类型幻觉。 |
| **Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs** | ICLR 2024 / OpenReview 版本 | verbalized confidence / uncertainty | 系统评估 LLM 能否表达自己的不确定性，用于置信度校准和失败预测。          |


### 内部状态检测

| 论文                                                                                                       |             会议/年份 | 对应方法                                       | 意义                                              |
| -------------------------------------------------------------------------------------------------------- | ----------------: | ------------------------------------------ | ----------------------------------------------- |
| **Unsupervised Real-Time Hallucination Detection based on the Internal States of Large Language Models** | ACL Findings 2024 | internal states                            | MIND，用 LLM 内部状态做无监督实时幻觉检测。                   |
| **Lookback Lens**                                                                                        |        EMNLP 2024 | attention map / classifier-guided decoding | 既做检测，也做缓解，用每个 head 对上下文和生成 token 的注意力比例判断上下文幻觉。 |


### 多模态幻觉

| 论文                                                                                                                                        |      会议/年份 | 对应方法                                     | 意义                                               |
| ----------------------------------------------------------------------------------------------------------------------------------------- | ---------: | ---------------------------------------- | ------------------------------------------------ |
| **Evaluating Object Hallucination in Large Vision-Language Models**                                                                       | EMNLP 2023 | POPE / object hallucination              |  LVLM object hallucination，提出 POPE 。    |
| **Unified Hallucination Detection for Multimodal Large Language Models**                                                                  |   ACL 2024 | MHaluBench / UNIHD                       | 提出统一多模态幻觉检测框架 UNIHD，用辅助工具验证多模态生成中的幻觉。            |
| **THRONE: An Object-based Hallucination Benchmark for the Free-form Generations of Large Vision-Language Models**                         |  CVPR 2024 | free-form object hallucination benchmark | 关注开放式图像描述中的 object hallucination，而不只看 yes or no 问答。 |
| **HallusionBench: An Advanced Diagnostic Suite for Entangled Language Hallucination and Visual Illusion in Large Vision-Language Models** |  CVPR 2024 | 多模态推理幻觉 benchmark                        | 用复杂图像上下文推理问题评估 LVLM 中语言幻觉和视觉错觉交织的问题。             |


### 生成后验证并修正

| 论文                                                                       |             会议/年份 | 对应方法 | 意义                              |
| ------------------------------------------------------------------------ | ----------------: | ---- | ------------------------------- |
| **Chain-of-Verification Reduces Hallucination in Large Language Models** | ACL Findings 2024 | CoVe | 先生成草稿，再生成验证问题，然后独立回答验证问题，然后修正原回答。 |


### 上述的对比解码、上下文感知解码、层间对比

| 论文                                                                                    |      会议/年份 | 对应方法                       | 意义                                                                  |
| ------------------------------------------------------------------------------------- | ---------: | -------------------------- | ------------------------------------------------------------------- |
| **Contrastive Decoding: Open-ended Text Generation as Optimization**                  |   ACL 2023 | 原始 contrastive decoding    | 用 expert LM 与 amateur LM 做对比，并加入 plausibility constraint，提高开放式生成质量。 |
| **Trusting Your Evidence: Hallucinate Less with Context-aware Decoding**              | NAACL 2024 | CAD                        | 对比“有上下文”和“无上下文”的输出分布，强化上下文支持的 token。                                |
| **DoLa: Decoding by Contrasting Layers Improves Factuality in Large Language Models** |  ICLR 2024 | 高层 logits vs 低层 logits     | 对比同一模型不同层的 logits，让高层事实知识更突出，从而减少事实错误。                              |
| **Lookback Lens**                                                                     | EMNLP 2024 | classifier-guided decoding | 先用 attention map 检测上下文幻觉，再用 classifier-guided decoding 缓解幻觉。        |


### 事实性FT、偏好优化、拒答

| 论文                                                                                                        |      会议/年份 | 对应方法                                 | 意义                              |
| --------------------------------------------------------------------------------------------------------- | ---------: | ------------------------------------ | ------------------------------- |
| **Fine-Tuning Language Models for Factuality**                                                            |  ICLR 2024 | factuality preference / DPO          | 用自动生成的事实性偏好排序微调模型，提高开放式生成事实性。   |
| **R-Tuning: Instructing Large Language Models to Say “I Don’t Know”**                                     | NAACL 2024 | refusal-aware instruction tuning     | 训练模型在超出自身知识范围时说“不知道”，而不是强行编答案。  |
| **Can LLMs Learn Uncertainty on Their Own? Expressing Uncertainty Effectively in a Self-training Manner** | EMNLP 2024 | uncertainty-aware instruction tuning | 让模型更好表达自身不确定、减少过度自信回答。 |


### 视觉对比解码、干预注意力

| 论文                                                                                                                            |               会议/年份 | 对应方法                                           | 意义                                                                 |
| ----------------------------------------------------------------------------------------------------------------------------- | ------------------: | ---------------------------------------------- | ------------------------------------------------------------------ |
| **Mitigating Object Hallucinations in Large Vision-Language Models through Visual Contrastive Decoding**                      |           CVPR 2024 | VCD                                            | 对比原始图像和扰动图像下的输出分布，压制语言先验导致的 object hallucination。                  |
| **OPERA: Alleviating Hallucination in Multi-Modal Large Language Models via Over-Trust Penalty and Retrospection-Allocation** |           CVPR 2024 | over-trust penalty / decoding intervention     | 发现 MLLM 生成时过度依赖少数 summary tokens，而忽视 image tokens，在解码阶段加入惩罚与回溯分配。 |
| **V-DPO: Mitigating Hallucination in Large Vision Language Models via Vision-guided Direct Preference Optimization**          | EMNLP Findings 2024 | multimodal DPO                                 | 用偏好学习缓解 LVLM 对 LLM backbone 语言先验的过度依赖，增强对视觉输入的关注。                  |
| **Hallucination Augmented Contrastive Learning for Multimodal Large Language Model**                                          |           CVPR 2024 | contrastive learning                           | 拉近非幻觉文本与视觉样本表示，推远幻觉文本表示，从表示学习角度缓解多模态幻觉。                            |
| **Understanding and Mitigating Hallucination in Large Vision-Language Models via Modular Attribution and Intervention**       |           ICLR 2025 | causal mediation / attention head intervention | 通过因果中介分析定位导致幻觉的模块，然后发现了 MHA 对幻觉词生成有重要影响。                             |
| **Mitigating Hallucinations in Large Vision-Language Models via DPO: On-Policy Data Hold the Key**                            |           CVPR 2025 | OPA-DPO                                        | 强调 DPO 数据要和当前策略 on-policy 对齐，用专家修正的幻觉回答构造偏好数据。                     |


