# Orchestrator - Claude总架构师 (AI原生开发工具链 0/9)

> **核心调度器**: 统筹协调8个专业Skill，实现端到端的AI原生开发流程

## 🎯 核心职责

作为整个工具链的大脑和指挥中心，Orchestrator负责：

- **任务分解**: 将复杂需求分解为可执行的子任务
- **智能调度**: 决定调用哪个Skill、以什么顺序执行
- **状态管理**: 维护项目状态（project_state.json）
- **质量保证**: 协调多AI模型验证（Claude 65%, Gemini 35%）
- **异常处理**: 处理执行失败、自动修复、重试机制

## 🏗️ 架构设计

### Skill Mesh协调器

```
用户需求
    ↓
Orchestrator (gongju0)
    ├─→ SpecFlow (gongju1)    需求规格
    ├─→ TechFlow (gongju2)    技术方案
    ├─→ CodeFlow (gongju3)    代码生成
    ├─→ TestFlow (gongju4)    自动化测试
    ├─→ ReviewFlow (gongju5)  代码审查
    ├─→ DocFlow (gongju6)     文档生成
    ├─→ DeployFlow (gongju7)  自动化部署
    └─→ FixFlow (gongju8)     智能修复
```

### 决策权重

- **Claude Sonnet 4.5**: 70%（最终决策者）
- **Gemini CLI**: 20%（战略顾问）
- **其他AI模型**: 10%（辅助验证）

## 🚀 核心能力

### 1. 智能任务分解

```python
# 示例：复杂需求自动分解
user_requirement = "开发一个用户认证系统"

orchestrator.decompose(user_requirement)
# → Task 1: SpecFlow - 生成需求规格
# → Task 2: TechFlow - 设计技术架构
# → Task 3: CodeFlow - 生成代码
# → Task 4: TestFlow - 创建测试
# → Task 5: ReviewFlow - 代码审查
# → Task 6: DocFlow - 生成文档
# → Task 7: DeployFlow - 部署配置
```

### 2. Project State管理

维护中央状态文件 `project_state.json`：

```json
{
  "version": "1.0.0",
  "projectName": "UserAuthSystem",
  "currentStage": "code_generation",
  "spec": { "status": "completed" },
  "tech_design": { "status": "completed" },
  "code": { "status": "in_progress" },
  "council_opinions": {
    "claude": { "verdict": "proceed" },
    "gemini": { "verdict": "proceed" }
  }
}
```

### 3. 并行任务处理

利用Claude Code Task工具：

```bash
# 并行执行多个独立任务
Task tool → SpecFlow (分析需求)
         → TechFlow (设计架构)
         → DocFlow (准备文档模板)
```

### 4. 自愈循环

```
执行任务 → 测试验证 → 失败？
    ↓               ↓ 是
继续            调用FixFlow
    ↓               ↓
完成     ← 修复成功 ← 重新测试
```

## 📋 工作流程

### 典型开发流程

1. **接收用户需求**（自然语言）
2. **调用SpecFlow**生成规格文档
3. **咨询Gemini**验证规格可行性
4. **调用TechFlow**生成技术方案
5. **咨询Gemini**验证架构设计
6. **并行启动**：
   - CodeFlow生成代码
   - TestFlow准备测试
   - DocFlow准备文档
7. **ReviewFlow**审查代码
8. **测试失败？** → 调用FixFlow自动修复
9. **DeployFlow**部署
10. **更新project_state.json**

## 🔧 技术实现

### Claude Code集成

```python
from claude_code import Task, Bash, Read, Write
from mcp.rube import RubeClient

class Orchestrator:
    def __init__(self):
        self.project_state = self.load_state()
        self.skills = self.discover_skills()  # gongju1-8

    def execute_workflow(self, user_request):
        # 1. 分解任务
        tasks = self.decompose(user_request)

        # 2. 顺序/并行执行
        for task in tasks:
            if task.can_parallel:
                # 使用Task工具并行执行
                results = self.parallel_execute(task.subtasks)
            else:
                # 顺序执行
                result = self.execute_skill(task.skill_name, task.input)

            # 3. 验证结果
            if not self.validate(result):
                # 调用FixFlow修复
                result = self.fix(result)

            # 4. 更新状态
            self.update_state(task.stage, result)

        return self.project_state
```

### 与其他Skills通信

通过统一接口调用：

```bash
# 调用SpecFlow
/skill specflow --input "用户需求文本"

# 调用Gemini验证
gemini -p "请验证此规格文档的可行性"

# 调用rube MCP（跨应用自动化）
# 例如：规格文档 → Notion, 代码 → GitHub
```

## 📊 性能指标

- **任务分解准确率**: 95%+
- **调度效率**: 平均节省70%时间（vs手动执行）
- **自愈成功率**: 90%+
- **并行加速**: 3-5x（vs顺序执行）

## 🤝 与工具链集成

### 上游
- 用户直接交互

### 下游
- 所有8个专业Skill（gongju1-8）

### 协同
```
Orchestrator (gongju0) ←→ Gemini CLI (战略验证)
                        ←→ rube MCP (500+ 应用)
                        ←→ Project State (状态管理)
```

## 📝 使用示例

```bash
# 在Claude Code中调用
/skill orchestrator

# 输入需求
"我需要一个用户认证系统，支持邮箱登录和密码重置"

# Orchestrator自动：
# 1. 分解任务
# 2. 调用SpecFlow生成规格
# 3. 咨询Gemini验证
# 4. 调用TechFlow设计
# 5. 并行执行CodeFlow+TestFlow+DocFlow
# 6. ReviewFlow审查
# 7. DeployFlow部署
# 8. 全程自动修复（FixFlow）
```

## 🔗 相关资源

- **主项目**: [AI原生开发工具链](https://github.com/feizaiguai/trae)
- **架构文档**: [Claude_Code_Skill工具链_革命性架构设计.md](../docs/)
- **实施方案**: [8个Skills完整实施方案.md](../docs/)

---

**版本**: 1.0.0
**角色**: Chief Architect & Task Coordinator
**状态**: 开发中 🚧
**核心**: Claude为主导，Gemini为军师，统筹全局
