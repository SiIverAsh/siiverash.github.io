---
categories:
- study
date: 2026-03-25 18:50:51 +0800
layout: post
tags:

title: 见过的论文里的专有名词
subject: ''
---





> 整理一下目前为止见过的论文里的专有名词，虽然可以见到再查，但是为了方便自己看，还是整理一下，持续更新。

## 1、ML基础

| 名词 (Term) | 定义 / 描述 | 分类标签 |
|------------|------------|----------|
| 机器学习 (Machine Learning) | 让系统从数据中自动学习模式并做出预测或决策，无需显式编程。 | ML |
| 监督学习 (Supervised Learning) | 使用带标签的数据训练模型，学习输入到输出的映射。 | ML |
| 无监督学习 (Unsupervised Learning) | 从未标记数据中发现结构、聚类或分布。 | ML |
| 半监督学习 (Semi-supervised Learning) | 结合少量标签数据与大量无标签数据进行训练。 | ML |
| 自监督学习 (Self-supervised Learning) | 利用数据自身构造监督信号（如掩码预测）。 | ML |
| 在线学习 (Online Learning) | 模型在数据流中逐样本更新，适应动态环境。 | ML |
| 离线学习 (Offline Learning) | 在固定数据集上训练，不与环境交互。 | ML |
| 迁移学习 (Transfer Learning) | 将在源任务上学到的知识迁移到目标任务。 | ML |
| 元学习 (Meta-Learning) | 学习如何学习，使模型能快速适应新任务。 | ML |
| 少样本学习 (Few-shot Learning) | 仅用少量示例即可泛化到新类别。 | ML |
| 零样本学习 (Zero-shot Learning) | 在未见过类别上完成任务，依赖语义描述。 | ML |
| 主动学习 (Active Learning) | 模型主动选择最有价值的样本请求标注。 | ML |
| 对比学习 (Contrastive Learning) | 通过拉近正样本、推开负样本来学习表示。 | ML |
| 表示学习 (Representation Learning) | 自动发现数据的有效特征表示。 | ML |
| 特征工程 (Feature Engineering) | 人工设计输入特征以提升模型性能。 | ML |
| 过拟合 (Overfitting) | 模型在训练集上表现好，但在新数据上泛化差。 | ML |
| 欠拟合 (Underfitting) | 模型无法捕捉数据基本模式。 | ML |
| 偏差-方差权衡 (Bias-Variance Tradeoff) | 模型误差由偏差（欠拟合）和方差（过拟合）共同决定。 | ML |
| 交叉验证 (Cross-Validation) | 评估模型泛化能力的重采样技术。 | ML |
| 正则化 (Regularization) | 通过约束模型复杂度防止过拟合（如L1/L2）。 | ML |
| 损失函数 (Loss Function) | 衡量预测与真实值差异的目标函数。 | ML |
| 优化器 (Optimizer) | 用于更新模型参数以最小化损失的算法。 | ML |
| 梯度下降 (Gradient Descent) | 沿损失函数负梯度方向迭代更新参数。 | ML |
| 随机梯度下降 (SGD) | 每次用单个样本估计梯度，加速训练。 | ML |
| 动量 (Momentum) | 在梯度更新中引入历史速度，加速收敛。 | ML |
| Adam 优化器 | 结合动量与自适应学习率的高效优化算法。 | ML |
| 学习率 (Learning Rate) | 控制参数更新步长的超参数。 | ML |
| 批量大小 (Batch Size) | 每次参数更新所用样本数量。 | ML |
| 早停 (Early Stopping) | 在验证性能不再提升时终止训练，防过拟合。 | ML |
| 准确率 (Accuracy) | 分类正确的样本比例。 | 评估 |
| 精确率/召回率/F1 (Precision/Recall/F1) | 衡量分类性能，尤其在不平衡数据中。 | 评估 |
| ROC-AUC | 衡量二分类器在不同阈值下的整体性能。 | 评估 |
| 混淆矩阵 (Confusion Matrix) | 展示分类结果的详细统计。 | 评估 |
| 均方误差 (MSE) | 回归任务中预测与真实值平方差的平均。 | 评估 |
| KL散度 (Kullback-Leibler Divergence) | 衡量两个概率分布的差异。 | 信息论 |
| 交叉熵 (Cross-Entropy) | 分类任务常用损失函数，衡量预测分布与真实分布差异。 | ML |
| 最大似然估计 (MLE) | 选择使观测数据概率最大的模型参数。 | 统计 |
| 贝叶斯推断 (Bayesian Inference) | 基于先验和似然计算后验分布。 | 统计 |
| 集成学习 (Ensemble Learning) | 结合多个模型提升性能（如Bagging, Boosting）。 | ML |
| 随机森林 (Random Forest) | 基于决策树的Bagging集成方法。 | ML |
| 梯度提升机 (GBM / XGBoost) | 通过逐步拟合残差构建强模型。 | ML |

## 2、DL

| 名词 (Term) | 定义 / 描述 | 分类标签 |
|------------|------------|----------|
| 神经网络 (Neural Network) | 由互连节点（神经元）组成的计算模型，模拟人脑信息处理。 | DL |
| 感知机 (Perceptron) | 最简单的线性分类神经网络。 | DL |
| 多层感知机 (MLP) | 含一个或多个隐藏层的前馈神经网络。 | DL |
| 激活函数 (Activation Function) | 引入非线性（如 ReLU、Sigmoid、Tanh）。 | DL |
| 反向传播 (Backpropagation) | 通过链式法则计算梯度的算法。 | DL |
| 权重初始化 (Weight Initialization) | 合理设置初始参数以促进训练（如 Xavier、He）。 | DL |
| 批归一化 (Batch Normalization) | 对每批数据标准化，加速训练并稳定收敛。 | DL |
| 层归一化 (Layer Normalization) | 对单个样本的特征归一化，适用于 RNN / Transformer。 | DL |
| Dropout | 训练时随机屏蔽部分神经元，防止过拟合。 | DL |
| 全连接层 (Fully Connected Layer) | 每个神经元与前一层所有神经元相连。 | DL |
| 残差连接 (Residual Connection) | 跳跃连接，缓解深层网络中的梯度消失问题。 | DL |
| 自编码器 (Autoencoder) | 学习数据压缩表示并进行重建。 | DL |
| 去噪自编码器 (Denoising AE) | 从加噪输入中恢复原始数据。 | DL |
| 稀疏自编码器 (Sparse AE) | 通过稀疏约束学习更有效的特征表示。 | DL |
| 受限玻尔兹曼机 (RBM) | 两层无向图模型，用于特征学习。 | 经典DL |
| 深度置信网络 (DBN) | 由多层 RBM 堆叠构成的生成模型。 | 经典DL |
| 卷积神经网络 (CNN) | 使用卷积核提取局部空间特征，常用于图像任务。 | CV/DL |
| 卷积 (Convolution) | 通过滑动滤波器提取局部特征的操作。 | CV |
| 池化 (Pooling) | 下采样操作（如 Max Pooling），降低维度并增强不变性。 | CV |
| 残差网络 (ResNet) | 基于残差连接的深度卷积网络架构。 | CV |
| Inception 模块 | 并行多尺度卷积核提取特征。 | CV |
| U-Net | 编码器-解码器结构，常用于医学图像分割。 | CV |
| 胶囊网络 (Capsule Network) | 使用向量表示特征，保留空间层级信息。 | CV |
| Vision Transformer (ViT) | 将图像分块后输入 Transformer 进行建模。 | CV |
| Swin Transformer | 基于滑动窗口的层次化视觉 Transformer。 | CV |
| ConvNeXt | 现代化 CNN 架构，性能接近 Transformer。 | CV |
| 神经辐射场 (NeRF) | 使用神经网络表示 3D 场景，实现新视角合成。 | 3D视觉 |
| 循环神经网络 (RNN) | 通过隐藏状态建模序列数据依赖。 | NLP/DL |
| 长短期记忆 (LSTM) | 带门控机制的 RNN，解决长期依赖问题。 | NLP |
| 门控循环单元 (GRU) | LSTM 的简化版本，计算更高效。 | NLP |
| Transformer | 基于自注意力机制的序列建模架构。 | NLP/DL |
| 注意力机制 (Attention Mechanism) | 动态关注重要信息，提高建模能力。 | NLP/CV |
| 自注意力 (Self-Attention) | 建模序列内部元素之间的依赖关系。 | NLP |
| 多头注意力 (Multi-Head Attention) | 并行多个注意力头捕获不同特征。 | NLP |
| 交叉注意力 (Cross-Attention) | 在不同序列之间建立关联（如编码器-解码器）。 | NLP |
| 位置编码 (Positional Encoding) | 为序列引入位置信息。 | NLP |
| 编码器-解码器 (Encoder-Decoder) | 将输入编码后再解码生成输出序列。 | NLP/CV |
| Mamba | 基于状态空间模型的高效序列建模架构。 | NLP |
| 状态空间模型 (SSM) | 用连续动态系统建模长序列依赖。 | NLP |
| 图神经网络 (GNN) | 用于处理图结构数据的神经网络。 | 图学习 |
| 图卷积网络 (GCN) | 基于图结构的卷积操作进行信息聚合。 | 图学习 |
| 消息传递神经网络 (MPNN) | 统一 GNN 框架（消息、聚合、更新）。 | 图学习 |
| 时空图神经网络 (ST-GNN) | 同时建模时间与空间依赖关系。 | 图学习 |
| 生成对抗网络 (GAN) | 通过生成器与判别器对抗训练生成数据。 | 生成式AI |
| Wasserstein GAN (WGAN) | 使用 Wasserstein 距离提升训练稳定性。 | 生成式AI |
| 变分自编码器 (VAE) | 基于概率潜变量生成数据。 | 生成式AI |
| 扩散模型 (Diffusion Models) | 通过逐步去噪生成数据。 | 生成式AI |
| 潜在扩散模型 (LDM) | 在潜在空间进行扩散以降低计算成本。 | 生成式AI |
| 自回归模型 (Autoregressive Models) | 按序列逐步生成数据。 | 生成式AI |
| 流模型 (Normalizing Flows) | 通过可逆变换建模复杂分布。 | 生成式AI |
| 能量基模型 (EBM) | 使用能量函数定义概率分布。 | 生成式AI |
| 对比散度 (Contrastive Divergence) | 训练 EBM 或 RBM 的近似方法。 | 生成式AI |
| 混合专家 (MoE) | 由多个专家网络组成，动态选择激活。 | 大模型 |
| 门控网络 (Gating Network) | 在 MoE 中决定激活哪些专家。 | 大模型 |
| 稀疏激活 (Sparse Activation) | 每次仅激活部分参数，提高效率。 | 大模型 |
| 知识蒸馏 (Knowledge Distillation) | 用大模型指导小模型训练。 | 模型压缩 |
| 模型剪枝 (Pruning) | 移除冗余参数以压缩模型。 | 模型压缩 |
| 量化 (Quantization) | 降低数值精度以减少计算与存储成本。 | 部署 |


## 3、NLP

| 名词 (Term) | 定义 / 描述 | 分类标签 |
|------------|------------|----------|
| 自然语言处理 (NLP) | 让计算机理解和生成人类语言的技术。 | NLP |
| 分词 (Tokenization) | 将文本切分为词或子词单元。 | NLP |
| 分词器 (Tokenizer) | 执行文本切分并建立 token 与 id 映射的组件。 | NLP |
| Byte Pair Encoding (BPE) | 通过频繁子串合并构建子词词表的方法。 | NLP |
| WordPiece | 常用于 BERT 系列的子词切分方法。 | NLP |
| SentencePiece | 面向原始文本训练子词词表的分词工具。 | NLP |
| 词干提取 (Stemming) | 去除词缀得到词干（如 running → run）。 | NLP |
| 词形还原 (Lemmatization) | 将词还原为词典形式。 | NLP |
| 词嵌入 (Word Embedding) | 将词映射为稠密向量（如 Word2Vec）。 | NLP |
| 上下文词嵌入 (Contextual Embedding) | 根据上下文动态生成词向量（如 BERT）。 | NLP |
| 词性标注 (POS Tagging) | 标注词的语法类别。 | NLP |
| 命名实体识别 (NER) | 识别人名、地名、组织等实体。 | NLP |
| 实体链接 (Entity Linking) | 将文本实体映射到知识库。 | NLP |
| 关系抽取 (Relation Extraction) | 识别实体之间的关系。 | NLP |
| 事件抽取 (Event Extraction) | 提取事件及其参与要素。 | NLP |
| 开放信息抽取 (Open IE) | 无需预定义关系直接抽取三元组。 | NLP |
| 共指消解 (Coreference Resolution) | 判断不同指代是否为同一实体。 | NLP |
| 语义角色标注 (SRL) | 标注句子中的语义角色关系。 | NLP |
| 依存句法分析 (Dependency Parsing) | 构建词语依赖关系树。 | NLP |
| 成分句法分析 (Constituency Parsing) | 构建句子短语结构树。 | NLP |
| 文本分类 (Text Classification) | 将文本划分到类别。 | NLP |
| 情感分析 (Sentiment Analysis) | 判断文本情感倾向。 | NLP |
| 文本蕴含 (NLI) | 判断句子间逻辑关系。 | NLP |
| 语义相似度 (Semantic Similarity) | 衡量文本语义接近程度。 | NLP |
| 机器翻译 (Machine Translation) | 自动翻译不同语言。 | NLP |
| 神经机器翻译 (NMT) | 基于神经网络的翻译方法。 | NLP |
| 束搜索 (Beam Search) | 近似最优解码策略。 | NLP |
| 文本摘要 (Text Summarization) | 生成文本简要概括。 | NLP |
| 抽取式摘要 | 从原文提取关键句。 | NLP |
| 生成式摘要 | 生成新的摘要文本。 | NLP |
| 问答系统 (QA) | 根据上下文回答问题。 | NLP |
| 开放域问答 (Open QA) | 从大规模知识中回答问题。 | NLP |
| 机器阅读理解 (MRC) | 从给定文本中定位答案。 | NLP |
| 对话系统 (Dialogue System) | 与用户进行多轮交互。 | NLP |
| 任务型对话 | 完成具体任务（如订票）。 | NLP |
| 闲聊对话 | 开放域自然对话。 | NLP |
| 对话状态跟踪 (DST) | 跟踪用户意图与状态。 | NLP |
| 信息检索 (IR) | 从文档集合中查找相关内容。 | IR |
| 倒排索引 (Inverted Index) | 支持高效检索的数据结构。 | IR |
| TF-IDF | 衡量词的重要性（用于检索与表示）。 | IR/NLP |
| BM25 | 改进 TF-IDF 的排序算法。 | IR |
| 词袋模型 (Bag-of-Words) | 忽略词序，仅统计词频。 | NLP |
| TF-IDF 向量 | 基于 TF-IDF 的文本表示。 | NLP |
| 语言模型 (Language Model) | 建模词序列概率分布。 | NLP |
| n-gram 模型 | 基于马尔可夫假设的语言模型。 | NLP |
| 困惑度 (Perplexity) | 衡量语言模型不确定性。 | 评估 |
| 主题模型 (Topic Modeling) | 发现文本中的潜在主题。 | NLP |
| 潜在狄利克雷分配 (LDA) | 经典概率主题模型。 | NLP |
| Word2Vec | 基于预测任务学习词向量。 | NLP |
| GloVe | 基于共现统计学习词向量。 | NLP |
| FastText | 基于子词建模词向量。 | NLP |
| ELMo | 基于双向 LSTM 的上下文表示。 | NLP |
| BERT | 双向 Transformer 预训练模型。 | NLP |
| RoBERTa | 优化版 BERT。 | NLP |
| ALBERT | 参数共享的轻量 BERT。 | NLP |
| DistilBERT | 蒸馏版 BERT。 | NLP |
| T5 | 统一为文本到文本任务框架。 | NLP |
| GPT | 自回归语言模型架构。 | NLP |
| GPT-2 / GPT-3 | 大规模预训练语言模型。 | NLP |
| 大语言模型 (LLM) | 超大规模通用语言模型。 | NLP |
| FLAN | 基于指令微调的模型。 | NLP |
| 指令微调 (Instruction Tuning) | 用指令数据优化模型行为。 | NLP |
| 提示工程 (Prompt Engineering) | 设计输入以引导模型输出。 | NLP |
| 上下文学习 (In-Context Learning) | 利用示例完成任务，无需训练。 | NLP |
| 链式思维 (CoT) | 生成中间推理步骤。 | NLP |
| 自洽性 (Self-Consistency) | 多路径推理投票选择答案。 | NLP |
| 程序辅助语言模型 (PAL) | 将推理转为程序执行。 | NLP |
| 思维树 (Tree of Thoughts) | 树状结构搜索推理路径。 | NLP |
| 反思 (Reflexion) | 自我反馈优化推理过程。 | NLP |
| 检索增强生成 (RAG) | 结合检索与生成提升准确性。 | NLP |
| LangChain | LLM 应用开发框架。 | 工具 |
| LlamaIndex | 面向 RAG 的数据框架。 | 工具 |
| 知识图谱 (Knowledge Graph) | 结构化实体关系网络。 | KG |
| 知识图谱补全 (KGC) | 预测缺失关系。 | KG |
| BLEU | 基于 n-gram 的翻译评估指标。 | 评估 |
| ROUGE | 摘要任务评估指标。 | 评估 |
| METEOR | 考虑语义匹配的评估指标。 | 评估 |
| BERTScore | 基于语义嵌入的评估指标。 | 评估 |
| MAUVE | 衡量生成分布差异。 | 评估 |
| SuperGLUE / GLUE | 综合 NLP 基准测试。 | 评估 |
| MMLU | 多学科知识评估数据集。 | 评估 |
| GSM8K | 数学推理数据集。 | 评估 |
| TruthfulQA | 测试事实性与幻觉。 | 评估 |
| BIG-bench | 多任务评估集合。 | 评估 |
| HELM | 全面评估框架。 | 评估 |
| 幻觉 (Hallucination) | 生成内容与事实不符。 | 问题 |
| 偏见 (Bias) | 模型中的不公平倾向。 | 伦理 |
| 公平性 (Fairness) | 确保不同群体公平对待。 | 伦理 |
| 可解释性 (Explainability) | 理解模型决策过程。 | 可信AI |
| LIME / SHAP | 模型解释方法。 | 可信AI |

## 4、CV

| 名词 (Term) | 定义 / 描述 | 分类标签 |
|------------|------------|----------|
| 计算机视觉 (Computer Vision) | 让机器理解和分析图像与视频内容。 | CV |
| 图像分类 (Image Classification) | 为整张图像分配类别标签。 | CV |
| 目标检测 (Object Detection) | 定位并识别图像中的多个物体。 | CV |
| 边界框 (Bounding Box) | 用矩形框标注目标位置。 | CV |
| 实例分割 (Instance Segmentation) | 对每个目标实例进行像素级分割。 | CV |
| 语义分割 (Semantic Segmentation) | 为每个像素分配类别标签。 | CV |
| 全景分割 (Panoptic Segmentation) | 统一实例分割与语义分割。 | CV |
| 关键点检测 (Keypoint Detection) | 定位物体关键点（如人体关节）。 | CV |
| 姿态估计 (Pose Estimation) | 估计人体或物体姿态结构。 | CV |
| 光流 (Optical Flow) | 估计像素在时间上的运动。 | CV |
| 立体视觉 (Stereo Vision) | 从双目图像恢复深度信息。 | CV |
| 深度估计 (Depth Estimation) | 从单目或视频预测深度。 | CV |
| 图像去噪 (Image Denoising) | 去除图像中的噪声。 | CV |
| 超分辨率 (Super-Resolution) | 提升图像分辨率。 | CV |
| 图像修复 (Image Inpainting) | 填补图像缺失区域。 | CV |
| 风格迁移 (Style Transfer) | 将图像风格迁移到另一图像。 | CV |
| 图像配准 (Image Registration) | 对齐不同来源图像。 | CV |
| 特征点检测 (Feature Detection) | 提取稳定关键点（如 SIFT）。 | CV |
| 特征描述子 (Feature Descriptor) | 描述关键点局部特征。 | CV |
| 边缘检测 (Edge Detection) | 提取图像边界（如 Canny）。 | CV |
| 霍夫变换 (Hough Transform) | 检测直线、圆等几何结构。 | CV |
| 图像金字塔 (Image Pyramid) | 多尺度图像表示方法。 | CV |
| 非极大值抑制 (NMS) | 去除重复检测框。 | CV |
| 交并比 (IoU) | 衡量两个框的重叠程度。 | 评估 |
| mAP | 目标检测综合评估指标。 | 评估 |
| PSNR / SSIM | 图像质量评估指标。 | 评估 |
| YOLO | 单阶段实时目标检测模型。 | CV |
| Faster R-CNN | 两阶段目标检测模型。 | CV |
| Mask R-CNN | 增加实例分割分支的检测模型。 | CV |
| EfficientDet | 基于 EfficientNet 的检测模型。 | CV |
| DETR | 基于 Transformer 的检测模型。 | CV |
| SAM | 通用图像分割模型。 | CV |
| Grounded-SAM | 结合检测与分割的开放词汇模型。 | CV |
| CLIP | 对齐图像与文本表示的模型。 | 多模态 |
| BLIP / BLIP-2 | 图文理解与生成模型。 | 多模态 |
| Flamingo | 支持交错图文输入的模型。 | 多模态 |
| KOSMOS-1/2 | 微软多模态大模型。 | 多模态 |
| LLaVA | 视觉+语言对话模型。 | 多模态 |
| 多模态大语言模型 (MLLM) | 处理多模态输入的语言模型。 | 多模态 |
| 视觉问答 (VQA) | 回答关于图像的问题。 | 多模态 |
| 图像描述生成 (Image Captioning) | 为图像生成文本描述。 | 多模态 |
| 跨模态检索 (Cross-modal Retrieval) | 图文互相检索。 | 多模态 |
| 视频分类 (Video Classification) | 对视频进行类别分类。 | 视频 |
| 动作识别 (Action Recognition) | 识别视频中的动作。 | 视频 |
| 视频目标检测 | 在视频中检测目标。 | 视频 |
| 视频跟踪 (Video Tracking) | 持续跟踪目标位置。 | 视频 |
| 多目标跟踪 (MOT) | 同时跟踪多个目标。 | 视频 |
| SORT / DeepSORT | 基于卡尔曼滤波的跟踪算法。 | 视频 |
| 光度立体视觉 (Photometric Stereo) | 从多光照恢复表面法线。 | 3D |
| 结构光 (Structured Light) | 通过投影图案获取深度。 | 3D |
| ToF (Time-of-Flight) | 基于飞行时间测距。 | 3D |
| 点云 (Point Cloud) | 三维空间中的点集合。 | 3D |
| PointNet / PointNet++ | 点云处理模型。 | 3D |
| 体素 (Voxel) | 三维网格表示单位。 | 3D |
| Mesh | 基于顶点与面的3D表示。 | 3D |
| 3D Gaussian Splatting | 基于高斯分布的3D表示方法。 | 3D |
| SLAM | 同步定位与建图技术。 | 机器人 |
| ORB-SLAM | 基于 ORB 特征的 SLAM 系统。 | 机器人 |
| 医学图像分割 | 医学图像中的结构分割任务。 | 医疗CV |
| nnU-Net | 自动化医学分割框架。 | 医疗CV |
| 遥感图像分析 | 分析卫星或航拍图像。 | 遥感 |
| 变化检测 | 检测不同时相图像差异。 | 遥感 |
| ImageNet | 大规模图像分类数据集。 | 数据集 |
| COCO | 检测、分割等多任务数据集。 | 数据集 |
| PASCAL VOC | 经典目标检测数据集。 | 数据集 |
| Cityscapes | 城市场景分割数据集。 | 数据集 |
| KITTI | 自动驾驶数据集。 | 数据集 |
| ActivityNet | 视频理解数据集。 | 数据集 |
| Kinetics | 视频动作分类数据集。 | 数据集 |
| ADE20K | 场景解析数据集。 | 数据集 |
| Open Images | 大规模多任务视觉数据集。 | 数据集 |

## 5、RL

| 名词 (Term) | 定义 / 描述 | 分类标签 |
|------------|------------|----------|
| 马尔可夫决策过程 (MDP) | 强化学习的标准数学建模框架。 | RL |
| 部分可观测MDP (POMDP) | 状态不可完全观测的扩展MDP。 | RL |
| 状态 (State) | 环境在某一时刻的表示。 | RL |
| 动作 (Action) | 智能体可执行的操作。 | RL |
| 奖励 (Reward) | 环境对动作的即时反馈信号。 | RL |
| 策略 (Policy) | 从状态到动作的映射函数。 | RL |
| 价值函数 (Value Function) | 衡量状态或状态-动作的长期回报。 | RL |
| Q函数 (Action-Value Function) | Q(s,a) 表示在状态 s 下执行动作 a 的期望回报。 | RL |
| 贝尔曼方程 (Bellman Equation) | 描述价值函数的递归关系。 | RL |
| 贝尔曼最优方程 | 描述最优策略的价值函数关系。 | RL |
| 探索 vs 利用 (Exploration vs Exploitation) | 在探索新策略与利用已有策略之间权衡。 | RL |
| ε-贪婪策略 (ε-Greedy) | 以 ε 概率随机探索，否则选择最优动作。 | RL |
| 蒙特卡洛方法 (Monte Carlo) | 基于完整轨迹估计回报。 | RL |
| 时序差分学习 (TD Learning) | 基于一步估计更新价值函数。 | RL |
| SARSA | 基于 on-policy 的 TD 控制算法。 | RL |
| Q-learning | 基于 off-policy 的 TD 控制算法。 | RL |
| 深度Q网络 (DQN) | 用神经网络近似 Q 函数。 | 深度RL |
| 经验回放 (Experience Replay) | 重用历史经验以提高样本效率。 | 深度RL |
| 目标网络 (Target Network) | 延迟更新目标值以稳定训练。 | 深度RL |
| Double DQN | 缓解 Q 值过估问题。 | 深度RL |
| Dueling DQN | 分离状态价值与优势函数。 | 深度RL |
| 优先经验回放 (PER) | 按 TD 误差优先采样经验。 | 深度RL |
| Rainbow | 集成多种 DQN 改进的算法。 | 深度RL |
| 策略梯度 (Policy Gradient) | 直接优化策略参数的方法。 | RL |
| REINFORCE | 基于蒙特卡洛的策略梯度算法。 | RL |
| Actor-Critic | 同时学习策略（Actor）与价值（Critic）。 | 深度RL |
| A3C / A2C | 异步/同步的 Actor-Critic 方法。 | 深度RL |
| PPO | 通过裁剪策略更新提高稳定性。 | 深度RL |
| TRPO | 通过 KL 约束限制策略更新幅度。 | 深度RL |
| DDPG | 连续动作空间的确定性策略梯度算法。 | 深度RL |
| TD3 | 改进 DDPG，降低过估问题。 | 深度RL |
| SAC | 基于最大熵的强化学习方法。 | 深度RL |
| IMPALA | 分布式 Actor-Learner 框架。 | 深度RL |
| Dreamer / DreamerV2 / V3 | 基于世界模型的强化学习方法。 | 深度RL |
| 世界模型 (World Model) | 学习环境动态用于规划与决策。 | 深度RL |
| 模型基RL (Model-Based RL) | 显式学习环境模型进行决策。 | RL |
| 无模型RL (Model-Free RL) | 不建模环境，直接学习策略或价值。 | RL |
| 离线强化学习 (Offline RL) | 在固定数据集上训练策略。 | RL |
| BCQ | 限制策略分布的离线 RL 方法。 | 离线RL |
| CQL | 保守 Q 学习，避免过高估计。 | 离线RL |
| Decision Transformer | 将 RL 建模为序列预测问题。 | 离线RL |
| IQL | 无需显式策略网络的离线 RL 方法。 | 离线RL |
| 多智能体强化学习 (MARL) | 多个智能体共同学习与交互。 | RL |
| 博弈论 (Game Theory) | 多智能体决策的理论基础。 | MARL |
| 纳什均衡 (Nash Equilibrium) | 各方策略稳定的博弈解。 | MARL |
| 逆强化学习 (Inverse RL) | 从专家行为中推断奖励函数。 | IL |
| 模仿学习 (Imitation Learning) | 模仿专家策略进行学习。 | IL |
| 行为克隆 (Behavior Cloning) | 将模仿学习转化为监督学习。 | IL |
| DAgger | 通过交互数据缓解分布偏移。 | IL |
| 课程学习 (Curriculum Learning) | 从简单任务逐步学习复杂任务。 | RL/ML |
| 奖励塑形 (Reward Shaping) | 设计辅助奖励加速学习。 | RL |
| 稀疏奖励 (Sparse Reward) | 仅在少数状态提供奖励。 | RL |
| 内在动机 (Intrinsic Motivation) | 基于好奇心驱动探索。 | RL |
| ICM | 基于预测误差的内在动机模块。 | RL |
| HER | 重标记目标以提高样本利用率。 | RL |
| 多任务RL (Multi-task RL) | 同时学习多个任务。 | RL |
| 元强化学习 (Meta-RL) | 快速适应新任务的 RL 方法。 | RL |
| 安全强化学习 (Safe RL) | 在约束条件下学习策略。 | 安全RL |
| 约束MDP (CMDP) | 带约束条件的 MDP 扩展。 | 安全RL |

## 6、LLM

| 名词 (Term) | 定义 / 描述 | 分类标签 |
|------------|------------|----------|
| 基础模型 (Foundation Model) | 在大规模数据上预训练的通用模型。 | 大模型 |
| 预训练 (Pretraining) | 在通用语料上学习通用能力。 | 大模型 |
| 监督微调 (SFT) | 在高质量数据上优化模型表现。 | 大模型 |
| 参数高效微调 (PEFT) | 仅训练少量新增或选定参数完成微调。 | 大模型 |
| LoRA | 通过低秩适配器高效微调大模型。 | 大模型 |
| QLoRA | 结合量化与 LoRA 的低成本微调方法。 | 大模型 |
| Prefix Tuning | 通过学习前缀向量引导模型完成任务。 | 大模型 |
| P-Tuning | 用可学习提示向量替代人工离散提示。 | 大模型 |
| 人类反馈强化学习 (RLHF) | 使用人类偏好优化模型输出。 | 对齐 |
| 奖励模型 (Reward Model) | 评估输出质量的模型。 | 对齐 |
| 直接偏好优化 (DPO) | 不使用RL直接优化偏好。 | 对齐 |
| ORPO | 将偏好优化与监督目标结合的对齐方法。 | 对齐 |
| KTO | 基于 Kahneman-Tversky 理论的偏好优化方法。 | 对齐 |
| 宪法AI (Constitutional AI) | 基于规则进行自我对齐。 | 对齐 |
| Self-Alignment | 模型自生成数据进行对齐。 | 对齐 |
| 拒绝采样 (Rejection Sampling) | 从候选中选择高质量输出。 | 推理 |
| KV Cache | 缓存历史键值张量以加速自回归解码。 | 推理优化 |
| 对齐税 (Alignment Tax) | 对齐带来的性能损失。 | 对齐 |
| 奖励黑客 (Reward Hacking) | 利用奖励漏洞而非完成任务。 | 风险 |
| 欺骗性对齐 (Deceptive Alignment) | 模型伪装为对齐状态。 | 风险 |
| 潜伏代理 (Sleeper Agents) | 在特定触发下执行隐藏行为。 | 风险 |
| 红队测试 (Red Teaming) | 主动攻击模型发现问题。 | 安全 |
| AI安全 (AI Safety) | 确保AI行为可控与安全。 | 安全 |
| AI治理 (AI Governance) | 规范AI开发与使用的制度。 | 治理 |
| AI审计 (AI Auditing) | 对AI系统进行合规检查。 | 治理 |
| 差分隐私 (Differential Privacy) | 通过噪声保护数据隐私。 | 隐私 |
| 水印 (Watermarking) | 在生成内容中嵌入标识。 | 版权 |
| 绿色AI (Green AI) | 优化能耗与碳排放。 | 可持续 |
| 模型崩溃 (Model Collapse) | 在合成数据上训练导致退化。 | 风险 |
| 涌现能力 (Emergent Abilities) | 大模型规模带来的新能力。 | 大模型 |
| Agent | 能自主规划与行动的系统。 | Agent |
| 具身智能 (Embodied AI) | 在物理环境中交互的AI。 | 机器人 |
| Speculative Decoding | 用小模型加速大模型生成。 | 推理优化 |
| Continuous Batching | 动态合批多个请求以提升推理吞吐。 | 推理优化 |
| FlashAttention | 优化注意力计算效率。 | 系统 |
| PagedAttention | 通过分页管理 KV Cache 提升推理内存效率。 | 系统 |
| RoPE | 旋转位置编码方法。 | 架构 |
| ALiBi | 线性偏置位置编码。 | 架构 |
| RMSNorm | 不减均值的归一化方法，常见于大模型。 | 架构 |
| SwiGLU | 常用于 Transformer 前馈层的激活结构。 | 架构 |
| 分组查询注意力 (GQA) | 多个查询头共享较少键值头的注意力机制。 | 架构 |
| 多查询注意力 (MQA) | 所有查询头共享同一组键值头以降低缓存开销。 | 架构 |
| RWKV | RNN与Transformer混合架构。 | 架构 |
| DeepSpeed | 大模型训练优化框架。 | 系统 |
| ZeRO | 分布式内存优化策略。 | 系统 |
| FSDP | PyTorch分布式训练方法。 | 系统 |
| Megatron-LM | NVIDIA大模型训练框架。 | 系统 |
| 张量并行 (Tensor Parallelism) | 将计算拆分到多个设备。 | 系统 |
| 流水线并行 (Pipeline Parallelism) | 按层分布执行模型。 | 系统 |
| 混合精度训练 | 使用低精度加速训练。 | 训练 |
| 学习率预热 | 初期逐步增大学习率。 | 训练 |
| 余弦退火 | 学习率周期性衰减。 | 训练 |
| 梯度检查点 | 用计算换显存。 | 训练 |
| 数据增强 | 提升数据多样性。 | 训练 |
| 对抗样本 (Adversarial Example) | 微小扰动导致错误预测。 | 安全 |
| 对抗训练 | 提升模型鲁棒性。 | 安全 |
| OOD检测 | 识别分布外数据。 | 可信AI |
| 不确定性估计 | 衡量预测置信度。 | 可信AI |
| 校准 (Calibration) | 概率与真实准确率一致。 | 可信AI |
| 模型卡片 (Model Cards) | 描述模型行为与风险。 | 治理 |
| 数据卡片 (Data Cards) | 描述数据来源与偏见。 | 治理 |
| 系统卡片 (System Cards) | 描述完整AI系统行为。 | 治理 |
| FLOPs | 浮点运算量。 | 评估 |
| 延迟 (Latency) | 单次推理耗时。 | 评估 |
| 吞吐量 (Throughput) | 单位时间处理能力。 | 评估 |
| 显存占用 (VRAM Usage) | GPU内存消耗。 | 评估 |
| 碳足迹 (Carbon Footprint) | AI运行的环境影响。 | 评估 |
| 提示注入 (Prompt Injection) | 利用输入操控模型行为。 | 安全 |
| 越狱 (Jailbreaking) | 绕过模型安全限制。 | 安全 |
| 数据投毒 (Data Poisoning) | 恶意污染训练数据。 | 安全 |
| 模型窃取 (Model Stealing) | 复制模型能力。 | 安全 |
| 成员推断攻击 | 判断数据是否参与训练。 | 隐私 |
| 模型反演 | 从输出恢复训练数据。 | 隐私 |
