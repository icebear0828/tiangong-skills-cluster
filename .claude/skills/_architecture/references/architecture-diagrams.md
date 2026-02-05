# TianGong Skills Cluster 架构图

> 由 code-visualizer skill 自动生成

## 1. 整体架构图

```mermaid
graph TB
    subgraph User["用户入口"]
        Task[用户任务]
    end

    subgraph L0["L0 指挥层 - Commanders"]
        MC[Meta Commander<br/>任务路由]
        EC[Evaluation Commander<br/>评估路由]
        LC[Learning Commander<br/>学习路由]
    end

    subgraph L1["L1 编排层 - Orchestrators"]
        CO[Code<br/>Orchestrator]
        DO[Doc<br/>Orchestrator]
        DAO[Data<br/>Orchestrator]
        MAO[Multi-Agent<br/>Orchestrator]
        MRO[Multi-Round<br/>Eval Orchestrator]
        LO[Learning<br/>Orchestrator]
        KGO[Knowledge Graph<br/>Orchestrator]
        VO[Verification<br/>Orchestrator]
        MPO[Micro-Project<br/>Orchestrator]
    end

    subgraph L2_Code["L2 代码类 Skills"]
        CG[code-gen]
        CR[code-review]
        TG[test-gen]
        DB[debug]
        RF[refactor]
    end

    subgraph L2_Doc["L2 文档类 Skills"]
        DG[doc-gen]
        CV[code-visualizer]
    end

    subgraph L2_Data["L2 数据类 Skills"]
        AD[api-design]
        DS[db-schema]
    end

    subgraph L2_Quality["L2 质量类 Skills"]
        SA[security-audit]
        PO[perf-optimize]
    end

    subgraph L2_Eval["L2 评估类 Skills"]
        IS[initial-screener]
        VA[vote-aggregator]
        DA[defect-analyzer]
        DVA[devils-advocate]
        CB[consensus-builder]
        RS[ranking-synthesizer]
        RE[resurrection-evaluator]
        FCR[final-candidate-reviewer]
        CC[confidence-calculator]
    end

    subgraph L2_Learn["L2 学习类 Skills"]
        KE[knowledge-extractor]
        AE[analogy-explainer]
        SEV[self-explanation-validator]
        CCU[content-curator]
        SQ[socratic-questioner]
        SM[spatial-mapper]
    end

    subgraph L2_Exp["L2 实验类 Skills"]
        CreC[creative-code]
        ArcE[arch-explore]
        Proto[prototype]
        DiagG[diagram-generator]
    end

    subgraph Infra["基础设施层"]
        SR[Skill Registry<br/>技能注册表]
        LM[Lifecycle Manager<br/>生命周期]
        EE[Eval Engine<br/>评估引擎]
        RLAIF[RLAIF Engine<br/>自我改进]
    end

    subgraph Genesis["进化层"]
        PM[Prime Mover<br/>技能进化]
    end

    Task --> MC
    MC --> CO & DO & DAO & MAO
    MC --> EC
    MC --> LC
    EC --> MRO
    LC --> LO & KGO & VO & MPO

    CO --> CG & CR & TG & DB & RF
    DO --> DG & CV
    DAO --> AD & DS
    CO --> SA & PO
    MRO --> IS & VA & DA & DVA & CB
    MRO --> RS & RE & FCR & CC
    LO --> KE & AE & SEV
    KGO --> CCU & SM
    VO --> SQ
    MAO --> L2_Exp

    SR -.-> L0 & L1 & L2_Code & L2_Doc
    LM -.-> L0 & L1 & L2_Code
    EE -.-> L2_Eval
    RLAIF -.-> PM
    PM -.-> SR

    style L0 fill:#e1f5fe
    style L1 fill:#fff3e0
    style L2_Code fill:#e8f5e9
    style L2_Doc fill:#e8f5e9
    style L2_Data fill:#e8f5e9
    style L2_Quality fill:#e8f5e9
    style L2_Eval fill:#fce4ec
    style L2_Learn fill:#f3e5f5
    style L2_Exp fill:#fffde7
    style Infra fill:#eceff1
    style Genesis fill:#fff8e1
```

## 2. 分层架构简图

```mermaid
graph TD
    subgraph L0["L0 - 指挥层"]
        direction LR
        MC["Meta Commander"]
        EC["Evaluation Commander"]
        LC["Learning Commander"]
    end

    subgraph L1["L1 - 编排层 (9个)"]
        direction LR
        O1["Code Orch"]
        O2["Doc Orch"]
        O3["Data Orch"]
        O4["Multi-Agent"]
        O5["..."]
    end

    subgraph L2["L2 - 执行层 (30个)"]
        direction LR
        S1["Core (17)"]
        S2["Extended (9)"]
        S3["Experimental (4)"]
    end

    subgraph Support["支撑层"]
        direction LR
        I["Infrastructure (4)"]
        G["Genesis (1)"]
    end

    L0 -->|路由| L1
    L1 -->|调度| L2
    Support -.->|支撑| L0 & L1 & L2

    style L0 fill:#1976d2,color:#fff
    style L1 fill:#ff9800,color:#fff
    style L2 fill:#4caf50,color:#fff
    style Support fill:#9e9e9e,color:#fff
```

## 3. 领域分布图

```mermaid
pie showData
    title Skills 领域分布 (47个)
    "Learning (12)" : 12
    "Evaluation (11)" : 11
    "Code (9)" : 9
    "Orchestration (9)" : 9
    "Other (6)" : 6
```

## 4. Tier 层级与契约关系

```mermaid
graph LR
    subgraph Core["Core Tier (28个)"]
        direction TB
        C1["严格契约 Strict"]
        C2["输入/输出验证"]
        C3["高可靠性"]
    end

    subgraph Extended["Extended Tier (15个)"]
        direction TB
        E1["标准契约 Standard"]
        E2["中等灵活性"]
        E3["稳定功能"]
    end

    subgraph Experimental["Experimental Tier (4个)"]
        direction TB
        X1["灵活契约 Flexible"]
        X2["高探索性"]
        X3["快速迭代"]
    end

    Experimental -->|晋升| Extended
    Extended -->|晋升| Core
    Core -->|降级| Extended
    Extended -->|降级/归档| Experimental

    style Core fill:#4caf50,color:#fff
    style Extended fill:#2196f3,color:#fff
    style Experimental fill:#ff9800,color:#fff
```

## 5. 任务流转时序图

```mermaid
sequenceDiagram
    participant U as 用户
    participant MC as Meta Commander
    participant CO as Code Orchestrator
    participant CG as code-gen
    participant CR as code-review
    participant TG as test-gen
    participant SR as Skill Registry

    U->>MC: 提交复杂任务
    MC->>SR: 查询可用 Skills
    SR-->>MC: 返回 Skill 列表
    MC->>MC: 分析任务复杂度
    MC->>CO: 路由到 Code Orchestrator
    CO->>CO: 构建执行 DAG
    CO->>CG: 调用 code-gen
    CG-->>CO: 返回代码
    CO->>CR: 调用 code-review
    CR-->>CO: 返回审查结果
    CO->>TG: 调用 test-gen
    TG-->>CO: 返回测试代码
    CO-->>MC: 合并结果
    MC-->>U: 返回最终输出
```

## 6. 目录结构图

```mermaid
graph LR
    subgraph Root[".claude/skills/_architecture/"]
        L0D["L0-*-commander/"]
        L1D["L1-orchestrators/"]
        L2D["L2-execution/"]
        InfraD["infra/"]
        GenesisD["genesis/"]
        RefsD["references/"]
    end

    subgraph L2Sub["L2-execution/"]
        Core["core/ (17)"]
        Extended["extended/ (9)"]
        Experimental["experimental/ (4)"]
    end

    L2D --> L2Sub

    style Root fill:#f5f5f5
    style L2Sub fill:#e8f5e9
```

## 架构统计

| 层级 | 数量 | 说明 |
|------|------|------|
| L0 指挥层 | 3 | Meta/Evaluation/Learning Commander |
| L1 编排层 | 9 | 各领域 Orchestrator |
| L2 执行层 | 30 | Core(17) + Extended(9) + Experimental(4) |
| Infrastructure | 4 | Registry/Lifecycle/Eval/RLAIF |
| Genesis | 1 | Prime Mover |
| **总计** | **47** | |

## 渲染说明

- **VS Code**: 安装 "Markdown Preview Mermaid Support" 扩展
- **在线渲染**: https://mermaid.live/
- **GitHub/GitLab**: 直接支持 Mermaid 代码块
- **Obsidian**: 原生支持

---

*生成时间: 2026-02-05*
