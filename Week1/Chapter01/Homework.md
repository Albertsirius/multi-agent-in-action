# Week1 - Chapter01

---

## 任务1

### 验证结果

**版本号：**

```bash
[~]$ opencode --version
1.14.30
```

**首次对话截图：**

![截图](img.png)

## 任务2

Python直接调用模型的代码件`code_analyzer.py`，分析一段opencode的源代码，使用了DeepSeek-V4。Opencode通过CLI分析同一段代码。观察分别的输出结果，opencode更多能够考虑该源代码外面的代码与它的关系，而用Python直接调起大模型，由于缺少context，结果显得孤立。

另一方面，“有状态”和“无状态”，这个实验没有做，因为估计能想到，Python程序每次的调用，如果不带有上次问大模型的上下问，调用都是独立的，可看做无状态。而opencode能带有context，属于“有状态”，每次回答都是有关联。

## 任务3
直接通过OpenCode进行分析：

```
The Core Loop: runLoop() (prompt.ts:1400-1628)
while (true) {
  // 1. Read messages, find last user/assistant, collect pending tasks
  let msgs = yield* MessageV2.filterCompactedEffect(sessionID)
  // 2. Exit condition: last assistant finished (non-"tool-calls") & no pending provider tools
  //    & last user is older than last assistant
  if (shouldExit) break
  // 3. Handle pending subtasks (subagents) or compaction
  // 4. Auto-create compaction if overflow detected
  // 5. Resolve agent from user message, enforce step limits
  // 6. Create assistant message with running state
  // 7. SessionProcessor.create() → resolve tools → build prompts → call LLM
  const result = yield* handle.process(streamInput)
  // 8. Handle result:
  //    "stop"    → break (blocked/error)
  //    "compact" → create compaction, continue
  //    "continue" → next iteration
}
Exit Condition (prompt.ts:1440-1448)
The loop exits when the last assistant finished with a reason that is not "tool-calls". This is the standard termination: LLM chose not to call any tools, so the conversation is complete.
```

