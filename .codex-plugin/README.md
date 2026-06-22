# Cognitive Adaptation Plugin

这个插件只做一件事：在 `UserPromptSubmit` 阶段固定注入一小段 router context。

## 设计对象

这个插件明确面向有 ADHD 和自闭症相关信息处理困难的人，也面向任何被术语密度、抽象概念、跳步推理、默认前提、英文命名卡住的人。

这不是需要藏起来的背景。它是这个插件的设计原因：如果模型默认“用户应该懂这个”，回答就会变得过度压缩；如果模型默认“用户可能需要一步一步接住信息”，回答就会更容易跟上。

所以插件里的 `SKILL.md` 会直接写出 ADHD 和自闭症相关信息处理困难，README 也直接说明这一点。公开说明和执行规则应该一致。

hook 脚本不会解析用户输入，不会分类，不会调用 DeepSeek/GPT，也不会决定是否启用认知适配。它只是读取并丢弃 stdin，随后通过 stdout 返回合法 JSON：

```json
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "<cognitive_adaptation_router>...</cognitive_adaptation_router>"
  }
}
```

两层分工：

- **hook / router 负责强制路由**：每轮固定注入 router。router 是强指令——命中解释/调研/教学/代码讲解/review 解释/debug 解释类任务时，模型必须先完整读取并逐条执行 skill 再作答；纯实现且用户没要求解释时忽略。
- **skill 负责强制执行方式**：真正的"怎么答"放在 `SKILL.md`，它是一份**输出合约**（固定标记句 + 5 节固定结构 + 红旗清单 + fail-closed 自检），不是软建议。

为什么这样设计：Codex 每轮只保证注入 router（最可靠通道），skill 正文是模型按需读取（自愿）。所以 router 用强指令保证"会去读 skill"，skill 用可观察的输出合约保证"读了就照做"。判断本身仍交给模型，但判断为命中后，执行方式是硬性的。

## 运行结构

```text
cognitive-adaptation/
  .codex-plugin/
    plugin.json
    prompts/router-context.md
  hooks/
    hooks.json
    run-hook.cmd
    user-prompt-submit
  skills/
    cognitive-adaptation/
      SKILL.md
```

## 当前 router

`prompts/router-context.md` 保持精简，但用**强指令**措辞（"必须先完整读取并逐条执行 skill"），不是软建议（"请使用"）。完整的认知适配规则仍放在 skill 里，不要整段塞进 router；router 只负责强制"命中就去读并执行 skill"。

## 验证

```bash
python -m pytest /Users/wycm/plugins/cognitive-adaptation/.codex-plugin/tests -q
printf '{"prompt":"调研一下 UserPromptSubmit 是什么"}' | /Users/wycm/plugins/cognitive-adaptation/hooks/user-prompt-submit
```

`plugin-creator` 的 validator 当前会拒绝 `plugin.json` 里的 `hooks` 字段；这个插件本身就是 hook 插件，所以该字段必须保留。不要为了通过这个 validator 删除 `hooks`。
