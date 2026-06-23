# Cognitive Adaptation Plugin

这个插件只做一件事：在 `UserPromptSubmit` 阶段固定注入一小段 router context。

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

- **hook / router 负责强制路由**：每轮固定注入 router。router 是强指令——命中解释/调研/教学/代码讲解/review 解释/debug 解释类任务时，模型必须先完整读取 skill 再作答；纯实现且用户没要求解释时忽略。
- **skill 负责适配方式**：真正的"怎么答"放在 `SKILL.md`。它强制保留大白话判断和逐步拆解，但术语拆解、例子/类比、行动项按当前问题选择，避免机械模板。

为什么这样设计：Codex 每轮只保证注入 router（最可靠通道），skill 正文是模型按需读取（自愿）。所以 router 用强指令保证"会去读 skill"，skill 再把硬性要求限制在真正有价值的部分：不跳步、讲清楚、按需解释。判断本身仍交给模型，但判断为命中后，必须进行认知适配。

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

`prompts/router-context.md` 保持精简，但用**强指令**措辞（"必须先完整读取 skill"），不是软建议（"请使用"）。完整的认知适配规则仍放在 skill 里，不要整段塞进 router；router 只负责强制"命中就去读 skill"，不要在 router 里重新硬化输出模板。

## 验证

```bash
python -m pytest /Users/wycm/plugins/cognitive-adaptation/.codex-plugin/tests -q
printf '{"prompt":"调研一下 UserPromptSubmit 是什么"}' | /Users/wycm/plugins/cognitive-adaptation/hooks/user-prompt-submit
```

`plugin-creator` 的 validator 当前会拒绝 `plugin.json` 里的 `hooks` 字段；这个插件本身就是 hook 插件，所以该字段必须保留。不要为了通过这个 validator 删除 `hooks`。
