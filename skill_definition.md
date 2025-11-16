# __TOOL_NAME__ Skill Definition

> Claude Code Skill for __TOOL_DESCRIPTION_SIMPLE__

## 核心能力

__TOOL_DESCRIPTION_FULL__

## Skill职责

作为AI原生开发工具链的第 __TOOL_NUMBER__ 个环节，本Skill负责：

1. 接收上游输入
2. 执行专业任务
3. 输出标准化结果
4. 与其他Skills协同

## 技术实现

### Claude Code集成

利用Claude Code生态的完整能力：
- Task工具（并行处理）
- MCP服务器（跨应用自动化）
- Bash/PowerShell（系统操作）
- Read/Write/Edit（文件操作）

### AI协同

- **主导**: Claude Sonnet 4.5（权重70%）
- **验证**: Gemini CLI（权重20%）
- **辅助**: 其他AI模型（权重10%）

## 使用方式

```bash
# 在Claude Code中调用
/skill __SKILL_NAME__

# 或通过API调用
```

## 输入输出

### 输入格式
```json
{
  "source": "upstream_tool",
  "data": {},
  "context": {}
}
```

### 输出格式
```json
{
  "status": "success",
  "result": {},
  "next_step": "downstream_tool"
}
```

## 依赖项

- anthropic>=0.40.0
- Claude Code环境
- rube MCP（可选）

---

**Skill类型**: __TOOL_TYPE__
**版本**: 1.0.0
**作者**: AI原生开发工具链团队
