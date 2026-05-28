# 💎 BlueOcean Product Selector · 全类目蓝海选品作战系统

> **本地单文件 HTML 选品工具** · 内置 318+ 产品方向 · AI Agent 顾问 · 多 LLM 支持 · 零部署成本

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![No Build](https://img.shields.io/badge/build-no--build-green)]()
[![Single File](https://img.shields.io/badge/distribution-single--file-blue)]()

---

## ✨ 这是什么

一个**真正的本地工具** — 双击 `index.html` 就能运行,所有数据保存在浏览器 localStorage,**不上传任何服务器**。

但它绝不是"静态网页"那么简单 —  内嵌完整的 **AI Agent 系统**,接入 DeepSeek/智谱/Perplexity/Claude 等 8 家 LLM,通过 Function Calling 协议让 AI 自动调用 15 个内部工具帮你做选品决策。

```
👤 你: "推荐 3 个低风险的宠物用品方向"
   ↓
💎 AI 主动调用 search_opportunities → 拿到机会库数据
   ↓
💎 给出 Markdown 表格 + TOP 3 推荐 + 可执行下一步按钮
   ↓
[+ 加入候选: 猫抓板] [+ 加入候选: 宠物除毛刷] [+ 查看候选池]
```

---

## 🎯 核心能力

### 14 个工作 Tab

| # | Tab | 功能 |
|---|------|------|
| 1 | 💎 **AI 选品顾问** | 自然语言对话,AI 自动调工具给方案 |
| 2 | 🎯 机会发现 | 15+ 维筛选,从内置 318 个产品方向找潜力品 |
| 3 | 📊 产品排行榜 | 7 种排序 × 12 种过滤 |
| 4 | ✅ 市场验证中心 | 6 区块深度验证 (供应链/竞品/利润/内容/风险) |
| 5 | ⚔️ 竞品分析 | 多竞品录入 + 自动汇总差异化建议 |
| 6 | 🏭 供应商对比 | 多供应商 6 维度评分 + 最优推荐 |
| 7 | 🎬 内容测款 | AI 生成短视频脚本/直播话术/标题/卖点 |
| 8 | 📋 候选池看板 | 8 状态流转 (待验证 → 已上架) + 优先级 + 标签 |
| 9 | 🔍 单品深度分析 | 7 节完整选品报告 |
| 10 | 🤖 AI 智能分析 | 单品深度 / 竞品对比 / 批量评估 / 趋势解读 |
| 11 | 📡 实时数据 | Perplexity 联网检索 + Cloudflare Worker 代理 |
| 12 | 📚 资料中心 | 一键全网汇总 + 私有知识库 + AI 可引用 |
| 13 | 📈 每日榜单 | CSV/JSON/智能粘贴导入 + 同款追踪 |
| 14 | 💾 数据导入导出 | 完整 JSON 备份/恢复 + Markdown 报告 |

### 318+ 内置产品方向

覆盖 **12 个主类目**: 宠物用品 / 家居收纳 / 厨房用品 / 清洁工具 / 数码配件 / 车载用品 / 母婴周边 / 服饰配件 / 运动户外 / 文具办公 / 礼品包装 DIY / 美妆个护工具

每个产品都预先标注 18 个维度评分 (新手友好度 / 内容种草能力 / 供应链难度 / 售后风险 / 合规风险 / 差异化空间...)

### 蓝海评分模型

100 分制,A/B/C/D 四级评定,8 维度加权 + 高风险红线库自动检测 + 20+ 标签自动生成。

### AI Agent · 15 个工具

```
search_opportunities   - 从机会库筛选产品
get_opportunity_detail - 查询单品 18 维度详情
add_to_candidate       - 加入候选池
get_candidates         - 查看候选池
compute_profit         - 算毛利/净利润/保本售价
detect_risk            - 风险检测 + 敏感词扫描
generate_content_plan  - 生成内容方案
get_competitors        - 查竞品
get_suppliers          - 查供应商
fetch_online_data      - Perplexity 联网检索
fetch_trend_radar      - 拉 TrendRadar 全网热点
search_library         - 搜索资料中心
save_to_library        - 保存资料
get_dashboard_stats    - 数据看板统计
list_categories        - 类目结构查询
```

---

## 🚀 快速开始 (3 分钟上手)

### 方式 1: 零配置体验 (无 AI,推荐先试这个)

```bash
# 直接双击 index.html,浏览器自动打开
# 首次启动会弹欢迎引导 → 点 "加载演示数据"
# 立即体验所有 13 个 Tab (排行榜 / 机会发现 / 验证中心 / 候选池)
```

### 方式 2: 接入 AI 顾问 (5 分钟)

#### 注册 DeepSeek (国内可用,推荐)

1. 访问 https://platform.deepseek.com → 手机号注册
2. 充值 **¥10** (够用几个月)
3. 创建 API Key (`sk-xxx`)
4. 打开 `index.html` → 按数字键 `0` 进入「系统设置」
5. 拉到底部 → AI 智能体配置:
   - 提供商: `DeepSeek`
   - API Key: 粘贴 `sk-xxx`
   - 模型: `deepseek-chat`
6. 保存 → 测试连接 → 按 `1` 回到 AI 顾问 → 开聊

也支持 **OpenAI / Claude / 智谱 GLM / 通义千问 / Kimi / 豆包 / 自定义 OpenAI 兼容**。

### 方式 3: 完整数据中台部署

参考 [DEPLOY.md](#部署完整版) 完成:
- ☁️ Cloudflare Worker 代理 (10 万次/天免费)
- 🔍 Perplexity 联网检索
- 📊 智谱 GLM-4-Plus (国内联网替代)
- 📡 TrendRadar 全网热点接入

---

## 🛠️ 项目结构

```
blueocean-product-selector/
├── index.html          # 主程序 (单文件,~5000 行,含完整 UI + Agent)
├── worker.js           # Cloudflare Worker 代理代码 (可选)
├── quick-setup.html    # 一键配置工具 (含 5 个数据源预设)
├── fix-agent.html      # AI 对话历史修复工具
├── test_agent.py       # AI Agent 自动化测试脚本
├── .env.example        # 环境变量示例
├── .gitignore          # Git 忽略规则
├── LICENSE             # MIT License
└── README.md           # 你正在看的这个
```

**单文件设计哲学**: 整个工具就是一个 `index.html`,**不需要 npm install / build / 服务器**。打开就用,关掉就走,所有数据在你本地。

---

## 🎨 特色功能

### 💎 AI 顾问的自然语言对话

```
你: 售价 39, 成本 8, 帮我算下利润
AI: [自动调用 compute_profit]
    ## 📊 利润分析
    | 项目 | 金额 |
    | 售价 | ¥39 |
    | 毛利 | ¥26 (66.7%) |
    | 净利润 | ¥20.29 (52.0%) |
    | 保本售价 | ¥17.20 |
    ✅ 良好水平,建议拿样测款
```

### 🛡️ 智能合规检测

- 食品 / 药品 / 医疗 / IP / 大件 等 8 类高风险自动标记
- 治疗 / 杀菌 / 100% 有效 / 祛痘 等 20+ 敏感词扫描
- 涉及高风险自动建议「不建议新手做」+ 具体合规要求

### 📊 纯 SVG 数据可视化

- 顶部数据看板 13 项指标
- 4 种图表 (机会等级饼图 / 类目分布柱状图 / 候选状态分布 / 榜单平台分布)
- 零依赖 (没有 D3.js / ECharts,纯手写 SVG)

### ⌨️ 完整快捷键

| 键 | 功能 |
|----|------|
| `Ctrl+K` | 全局搜索 (跨机会库 / 候选 / 竞品 / 榜单 / AI 历史) |
| `1-9, 0` | 切换 Tab |
| `Esc` | 关闭弹窗 |
| `Ctrl+S` | 保存当前验证 |
| `Ctrl+B` | 一键备份 |
| 🌙 / ☀️ | 切换暗色模式 |

### 🤖 AI Agent 简洁/详细模式

- **简洁模式** (默认): 只显示对话内容
- **详细模式**: 显示每次工具调用的输入参数和返回数据 (可折叠)

---

## ⚠️ 合规与免责声明

**这是一个本地决策辅助工具,不是投资顾问。**

- ❌ **不自动获取**平台实时数据 (抖音/淘宝/拼多多/小红书 等都不开放公开 API)
- ❌ **不保证**爆品 / 收益 / 销量
- ❌ **不构成**商业建议
- ✅ 真实销量 / GMV / 搜索量 / 退货率 / 供应商履约能力 等必须人工核实
- ✅ 涉及食品 / 药品 / 医疗 / 化妆品 / 强功效 / 品牌 IP 等需独立完成资质审查

工具中所有评分均来自**内置规则模型**和**用户录入数据**,真实市场表现需自行验证。

---

## 🧰 技术栈

- **前端**: 纯原生 HTML + CSS + JavaScript (ES6+) — **无构建无依赖**
- **存储**: 浏览器 localStorage (~5MB)
- **AI 集成**: OpenAI 兼容协议 + Anthropic Claude 协议 + Perplexity 扩展
- **数据可视化**: 纯 SVG
- **代理**: Cloudflare Worker (可选)
- **测试**: Python + requests (test_agent.py)

---

## 🤝 贡献

欢迎 PR:

- 扩充类目机会库 (修改 `index.html` 中的 `CATEGORY_DATA`)
- 新增 LLM 提供商支持 (修改 `LLM_PROVIDERS`)
- 优化 AI 工具调用 prompt
- 翻译为英文 / 其他语言

---

## 📜 License

[MIT License](LICENSE) © 2026 BlueOcean Contributors

---

## 🔗 相关资源

- DeepSeek API: https://platform.deepseek.com
- 智谱 AI: https://open.bigmodel.cn
- Perplexity API: https://www.perplexity.ai/settings/api
- Cloudflare Workers: https://workers.cloudflare.com
- TrendRadar (热点聚合): https://github.com/sansan0/TrendRadar

---

## 部署完整版

### Cloudflare Worker 代理 (5 分钟)

1. 编辑 `worker.js`,把 `SECRET_TOKEN = ''` 改成你的随机字符串
   ```bash
   openssl rand -hex 24
   ```
2. 访问 https://workers.cloudflare.com → 创建 Worker → 粘贴 `worker.js` 内容 → Deploy
3. 拿到 URL (例如 `https://your-proxy.workers.dev`)
4. 在 `index.html` → 实时数据 Tab → 全局代理 URL 填:
   ```
   https://your-proxy.workers.dev/?url={url}&token=YOUR_TOKEN
   ```

### 自动化测试

```bash
# 安装依赖
pip install requests python-dotenv

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入 DEEPSEEK_API_KEY

# 运行测试
python test_agent.py
```

---

**Made with 🤖 by Claude Code · Powered by DeepSeek / Anthropic / OpenAI**
