# Orchestrator Skill Definition

> **Claude总架构师** - AI原生开发工具链的大脑和指挥中心

## Skill身份

- **名称**: Orchestrator
- **编号**: 0/9
- **角色**: Chief Architect & Task Coordinator
- **权重**: Claude 65%, Gemini 35%

## 核心职责

### 1. 任务分解与调度

接收用户需求，智能分解为可执行子任务，决定调用顺序：

```
用户: "开发一个博客系统"

Orchestrator分解:
1. SpecFlow: 生成需求规格（包括用户故事、功能列表）
2. TechFlow: 设计技术架构（数据库、API、前端）
3. CodeFlow: 生成后端API代码
4. CodeFlow: 生成前端代码
5. TestFlow: 创建单元测试和E2E测试
6. ReviewFlow: 代码审查
7. DocFlow: 生成API文档和用户手册
8. DeployFlow: 配置CI/CD和部署
```

### 2. Project State管理

维护 `project_state.json`，记录：
- 当前阶段（spec, design, code, test, review, doc, deploy）
- 每个阶段状态（pending, in_progress, completed, failed）
- AI模型意见（Claude, Gemini, others）
- 错误记录和修复历史

### 3. 多AI协同决策

**Council of Models机制**：
- Claude: 执行和最终决策（65%权重）
- Gemini: 战略验证和建议（35%权重）
- 

### 4. 自愈机制

监控任务执行，自动处理失败：
```
Task失败 → 分析错误 → 咨询Gemini → 调用FixFlow → 重试
```

## 技术能力

### Claude Code工具集成

```python
# 1. Task工具 - 并行处理
Task(subagent_type="general", description="并行执行SpecFlow和DocFlow")

# 2. Bash - 系统操作
Bash("git status && ruff check .")

# 3. Read/Write - 文件操作
project_state = Read("project_state.json")
Write("project_state.json", updated_state)

# 4. Grep/Glob - 代码探索
Grep(pattern="def.*auth", path="src/")
```

### MCP服务器集成

```python
# rube MCP - 跨应用自动化
# 规格文档 → Notion
# 代码 → GitHub
# 通知 → Slack
# 部署 → Vercel
```

### Gemini CLI调用

```bash
# 战略验证
gemini -p "请评估此技术方案的可行性和风险
Context: @project_state.json @tech_design.md"
```

## 工作流示例

### 场景1：从需求到部署

```bash
User: "开发一个待办事项应用"

Orchestrator执行:
  [Stage 1] 调用SpecFlow
  → 生成需求规格文档
  → 保存到 project_state.spec

  [Stage 2] 咨询Gemini验证规格
  → gemini -p "验证待办应用规格"
  → 记录意见到 council_opinions.gemini

  [Stage 3] 调用TechFlow
  → 生成技术架构（React + FastAPI + SQLite）
  → 保存到 project_state.tech_design

  [Stage 4] 并行执行（Task工具）
  → CodeFlow: 后端API
  → CodeFlow: 前端UI
  → TestFlow: 测试用例
  → DocFlow: API文档

  [Stage 5] 调用ReviewFlow
  → 代码审查
  → 发现3个问题

  [Stage 6] 调用FixFlow
  → 自动修复3个问题
  → 重新审查 → 通过

  [Stage 7] 调用DeployFlow
  → 配置Vercel部署
  → 部署成功

  [Stage 8] 更新project_state
  → status: "deployed"
  → url: "https://todo-app.vercel.app"
```

### 场景2：异常处理

```bash
CodeFlow生成代码 → 测试失败

Orchestrator处理:
  1. 捕获错误
  2. 分析失败原因
  3. 咨询Gemini建议
  4. 调用FixFlow修复
  5. 重新测试
  6. 通过 → 继续流程
```

## 输入输出

### 输入格式

```json
{
  "type": "user_request",
  "content": "用户需求的自然语言描述",
  "context": {
    "existing_project": false,
    "tech_preferences": ["Python", "React"]
  }
}
```

### 输出格式

```json
{
  "status": "completed",
  "project_state": {
    "version": "1.0.0",
    "stages": {
      "spec": "completed",
      "design": "completed",
      "code": "completed",
      "test": "completed",
      "review": "completed",
      "doc": "completed",
      "deploy": "completed"
    }
  },
  "artifacts": {
    "spec": "path/to/spec.md",
    "code": "path/to/src/",
    "tests": "path/to/tests/",
    "docs": "path/to/docs/",
    "deploy_url": "https://..."
  }
}
```

## 调用方式

```bash
# Claude Code中
/skill orchestrator

# 或通过API
POST /skills/orchestrator
{
  "input": "开发一个博客系统"
}
```

---

**Skill类型**: Coordinator & Decision Maker
**版本**: 1.0.0
**作者**: AI原生开发工具链团队
**核心理念**: Claude主导，Gemini辅佐，统筹全局
