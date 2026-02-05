# 文档自动分类系统设计方案

## 目标
建立一个可维护、可扩展的文档自动分类系统，利用 Gemini CLI 进行智能分类。

## 用户偏好
- ✅ 创建新目录: `09-资源与素材` + `10-期刊文章`
- ✅ 图片处理: 跟随引用它的md文件
- ✅ 运行模式: 全自动（gemini yolo模式）

## 现状分析
- **现有分类**: 8个主题目录 (01-08) + 特殊项目目录
- **根目录待整理**: 30+ 未分类文件（md、canvas、png等）
- **工具**: Gemini CLI 可用，支持 yolo 模式和 json 输出

---

## 实施方案

### 1. 创建分类配置文件 `.doc-classifier.yaml`

位置: `D:\codeai\Obsidian\文档\.doc-classifier.yaml`

```yaml
categories:
  "01-安全与攻防":
    description: "LLM安全、红队测试、越狱技术、逆向工程、攻击防御"
    keywords: ["越狱", "攻击", "安全", "逆向", "jailbreak", "prompt injection"]
    subcategories:
      "越狱提示词/Google": "Google/Gemini相关系统提示词"
      "越狱提示词/Anthropic": "Claude相关系统提示词"
      "越狱提示词/OpenAI": "GPT相关系统提示词"
      "越狱提示词/国产模型": "国产AI模型系统提示词"
      "越狱提示词/其他平台": "其他AI平台系统提示词"

  "02-API与数据采集":
    description: "API文档、数据爬取、数据库规范、脚本工具"
    keywords: ["API", "数据", "爬取", "数据库", "payload", "fetch"]

  "03-Prompt技巧":
    description: "提示词工程、角色扮演、内容生成、视觉创作提示词"
    keywords: ["prompt", "提示词", "角色", "风格", "生成"]

  "04-AI系统与提示词":
    description: "AI系统配置、Agent架构、系统提示词模板"
    keywords: ["system prompt", "agent", "系统提示词", "架构"]

  "05-工作与项目":
    description: "工作备忘、项目规划、工作流、需求文档"
    keywords: ["工作", "项目", "备忘", "需求", "规划"]

  "06-变现与商业":
    description: "商业化策略、盈利模式、出海"
    keywords: ["变现", "商业", "盈利", "出海"]

  "07-个人":
    description: "个人日记、自传、私人笔记"
    keywords: ["日记", "自传", "个人"]

  "08-技术文档":
    description: "架构设计、开发规范、技术对比、开发指南"
    keywords: ["架构", "规范", "设计", "开发", "技术"]

  "09-资源与素材":
    description: "数据集、参考素材、独立资源"
    keywords: ["数据集", "素材"]

  "10-期刊文章":
    description: "期刊、杂志、文章合集"
    keywords: ["magazine", "期刊", "issue"]

special_directories:
  - "opan"
  - "obsidian-skills"
  - "游戏"
  - ".obsidian"

ignore_patterns:
  - "README*.md"
  - "*.canvas"  # 保留在根目录
  - "*.base"    # 保留在根目录
```

### 2. 创建分类脚本 `scripts/classify_docs.py`

位置: `D:\codeai\Obsidian\文档\scripts\classify_docs.py`

功能:
- 扫描根目录未分类文件
- 调用 Gemini CLI 分析文件内容
- 根据 AI 判断移动到合适目录
- 生成分类报告

核心逻辑:
```python
# 伪代码
1. 读取 .doc-classifier.yaml 配置
2. 扫描根目录中的 .md 文件（排除特殊目录和忽略模式）
3. 对每个文件:
   a. 读取文件内容
   b. 构造 prompt 发送给 gemini cli
   c. gemini 返回推荐分类 (JSON格式)
   d. 确认后移动文件
4. 生成分类报告
```

### 3. Gemini 分类 Prompt 模板

```
你是文档分类助手。请分析以下文档内容，判断它应该归入哪个目录。

可用目录:
{从配置文件读取的目录列表及描述}

文档内容:
"""
{文件内容前2000字符}
"""

请返回JSON格式:
{
  "category": "目录名",
  "subcategory": "子目录名（如有）",
  "confidence": 0.0-1.0,
  "reason": "分类理由"
}
```

### 4. 使用方式

```bash
# 预览模式（只显示分类建议，不移动）
python scripts/classify_docs.py --preview

# 交互模式（每个文件确认后移动）
python scripts/classify_docs.py --interactive

# 自动模式（使用gemini yolo模式）
python scripts/classify_docs.py --auto

# 分类单个文件
python scripts/classify_docs.py --file "某文件.md"
```

---

## 文件清单

### 需要创建的文件
| 文件 | 说明 |
|------|------|
| `.doc-classifier.yaml` | 分类规则配置 |
| `scripts/classify_docs.py` | 主分类脚本（支持gemini全自动模式） |
| `09-资源与素材/` | 新建目录（数据集、独立素材） |
| `10-期刊文章/` | 新建目录（期刊、杂志） |

### 图片处理逻辑
- 脚本会扫描所有md文件，检测 `![[xxx.png]]` 引用
- 图片跟随引用它的md文件移动到同目录
- 未被引用的图片保留根目录或移至素材目录

### 需要整理的根目录文件

**高优先级（明确可分类）**:
| 文件 | 建议目录 |
|------|----------|
| `youmind数据集.md` | 09-资源与素材 |
| `攻击数据集.md` | 01-安全与攻防 |
| `kimi 2.5.md`, `kimi2.5 agent.md` | 04-AI系统与提示词 |
| `光影.md`, `面部、毛发、风格.md`, 等视觉相关 | 03-Prompt技巧 |
| `MAGAZINE_*.md` | 10-期刊文章 |
| 7个 `.png` 图片 | 跟随引用的md文件 |

**保留根目录**:
- `README_目录导航.md` - 主导航
- `目录脑图.canvas` - 思维导图
- `知识图谱.canvas` - 知识关系
- `ANTIGRAVITY_HOME.md` - 首页

---

## 验证方式

1. 运行 `python scripts/classify_docs.py --preview` 查看分类建议
2. 手动确认几个文件的分类结果
3. 运行完整分类后检查目录结构
4. 更新 `README_目录导航.md`

---

## 未来扩展

- 添加 git hook：在 commit 前自动检查未分类文件
- 添加 Obsidian 插件集成
- 支持批量重命名规范化文件名
