# Cognitive Adaptation

我会用最通俗易懂的方式解释给你听

## 一句话大白话结论

这个插件的作用很简单：当你问的是“解释、调研、教学、代码讲解、review 解释、debug 解释”这类问题时，它会提醒模型先切换成更耐心、更不跳步、更少术语压缩的回答方式。

它不替你回答问题。它只是把一张“回答前必须遵守的说明卡”塞进 Codex 当前这一轮对话里。

## 先说它解决什么问题

很多技术回答默认读者已经懂一堆前提：

- 默认你知道 `hook` 是什么；
- 默认你知道 `router` 是什么；
- 默认你知道为什么一个 `SKILL.md` 会影响模型回答；
- 默认你能自己补上中间推理。

这个插件反过来做：默认读者不懂。先用大白话讲，再拆术语，再一步一步展开。

## 术语拆解

### Codex

字面意思：OpenAI 的代码协作环境。

在这里具体指：你正在使用的 Codex 桌面或 CLI 环境，它支持插件、技能和 hook。

为什么叫这个：Codex 是平台名，插件是挂在 Codex 这个平台里的。

### Plugin

字面意思：插件。

在这里具体指：一个可以被 Codex 加载的小功能包。这个仓库就是一个 Codex plugin。

为什么叫这个：它不是单独运行的大程序，而是插到 Codex 运行流程里的小模块。

### UserPromptSubmit

字面意思：用户提交提示词。

在这里具体指：你在 Codex 里发出一条消息的那个时刻。

为什么叫这个：`User` 是用户，`Prompt` 是你输入的话，`Submit` 是提交。

### Hook

字面意思：钩子。

在这里具体指：Codex 在某个时刻自动调用的一段脚本。这个插件的 hook 会在 `UserPromptSubmit` 时运行。

为什么叫这个：它像一个挂钩，挂在 Codex 的某个流程节点上。流程走到这里，脚本就被叫醒。

### Router

字面意思：路由器、分流器。

在这里具体指：一小段判断规则。它告诉模型：如果当前任务是解释类，就必须去读 `cognitive-adaptation` skill；如果是纯实现、纯测试、纯部署，就忽略这段规则。

为什么叫这个：它不亲自回答问题，只决定“这类问题应该走哪条回答路线”。

### Skill

字面意思：技能。

在这里具体指：`skills/cognitive-adaptation/SKILL.md` 这份文件。它规定模型应该怎么解释：先大白话结论，再拆术语，再逐步展开，再给例子，最后总结该记住什么。

为什么叫这个：它不是普通文档，而是给模型执行的一套能力说明。

### Output Contract

字面意思：输出合约。

在这里具体指：skill 里写死的回答格式要求。只要命中解释类任务，回答就必须按那几节来，不能只给一句压缩结论。

为什么叫这个：它像合同一样，规定输出必须长什么样。

### additionalContext

字面意思：额外上下文。

在这里具体指：hook 返回给 Codex 的一段额外说明。Codex 会把它加入当前这一轮模型能看到的内容里。

为什么叫这个：它不是用户原本输入的话，而是插件额外加进去的背景指令。

### plugin.json

字面意思：插件的 JSON 配置文件。

在这里具体指：`.codex-plugin/plugin.json`。它告诉 Codex 这个插件叫什么、有什么能力、hook 在哪里、技能在哪里、展示链接是什么。

为什么叫这个：它用 JSON 格式描述插件。

## 逐步展开：它到底怎么工作

### 1. 用户发出一条消息

比如用户说：

```text
调研一下 UserPromptSubmit 是什么，并讲清楚。
```

这一步只是普通对话。插件还没有回答任何东西。

### 2. Codex 触发 `UserPromptSubmit` hook

Codex 看到用户提交了消息，于是调用这个文件：

```text
hooks/user-prompt-submit
```

这个脚本就是本插件真正会被执行的代码。

### 3. Hook 读入用户消息，但不解析它

脚本会消费标准输入，避免 Codex 的 hook 流程卡住。

但它不会做这些事：

- 不分析你的问题；
- 不保存你的问题；
- 不上传你的问题；
- 不调用外部模型；
- 不调用 DeepSeek、GPT、Claude 或任何第三方 API。

它只是把输入吃掉，然后继续下一步。

### 4. Hook 读取 router 文本

脚本会读取这个文件：

```text
.codex-plugin/prompts/router-context.md
```

这个文件里写的是路由规则：什么时候应该启用 `cognitive-adaptation` skill，什么时候应该忽略。

### 5. Hook 把 router 包成 JSON 返回给 Codex

hook 输出的结构大概是这样：

```json
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "<cognitive_adaptation_router>...</cognitive_adaptation_router>"
  }
}
```

这表示：请把 `additionalContext` 里的内容加入当前这一轮模型上下文。

### 6. 模型看到 router

模型现在会看到一段额外说明：

```text
如果当前用户请求属于解释、调研、教学、代码讲解、review 解释、debug 解释类任务：
你必须先完整读取并逐条执行 cognitive-adaptation skill 再作答。
否则忽略本条上下文。
```

这就是“路由”的关键。

### 7. 如果任务命中，模型加载 skill

如果用户问的是解释类问题，模型应该读取：

```text
skills/cognitive-adaptation/SKILL.md
```

然后按照里面的输出合约回答。

### 8. 如果任务不命中，模型忽略它

比如用户只是说：

```text
跑一下测试。
```

这不是解释任务。模型应该直接跑测试，不需要把回答变成长教程。

## 例子：命中和不命中

### 会命中的例子

```text
解释一下这个报错为什么发生。
```

原因：这是 debug 解释。插件希望模型把原因讲清楚，而不是只说“改这里”。

### 不会命中的例子

```text
把 README.md 里的错别字改掉。
```

原因：这是纯改文件。用户没有要求解释原理，所以不应该强行套长格式。

## 它不是什么

它不是聊天机器人。它不会自己生成最终答案。

它不是分类模型。它不会调用另一个模型来判断用户问题。

它不是监控程序。它不会记录你的 prompt。

它不是云服务。它不需要服务器，不需要 API key。

它不是万能规则。模型仍然可能不完美，所以测试里会检查 router 和 skill 的关键约束有没有保留。

## 文件结构

```text
cognitive-adaptation/
  .codex-plugin/
    plugin.json
    prompts/
      router-context.md
    tests/
      test_user_prompt_submit_hook.py
  hooks/
    hooks.json
    run-hook.cmd
    user-prompt-submit
  skills/
    cognitive-adaptation/
      SKILL.md
```

每个部分做什么：

- `.codex-plugin/plugin.json`：告诉 Codex 插件基本信息。
- `.codex-plugin/prompts/router-context.md`：保存 router 文本。
- `.codex-plugin/tests/test_user_prompt_submit_hook.py`：测试 hook 和 skill 的关键行为。
- `hooks/user-prompt-submit`：真正被 Codex 调用的 hook 脚本。
- `skills/cognitive-adaptation/SKILL.md`：真正规定回答方式的 skill。

## 怎么验证它有没有工作

运行测试：

```bash
python -m pytest .codex-plugin/tests -q
```

手动看 hook 输出：

```bash
printf '{"prompt":"调研一下 UserPromptSubmit 是什么"}' | ./hooks/user-prompt-submit
```

如果输出里能看到 `<cognitive_adaptation_router>`，说明 hook 正在把 router context 注入给 Codex。

## 隐私和安全

这个插件不需要 API key。

这个插件不调用外部网络服务。

这个插件的 hook 不保存用户输入。

如果以后有人改了这个插件，让它开始记录日志、联网、调用模型或保存数据，就应该先更新隐私说明。

更多细节见：

- [PRIVACY.md](PRIVACY.md)
- [TERMS.md](TERMS.md)

## 你现在该记住什么

1. Hook 负责把 router context 塞进当前对话。
2. Router 负责判断什么时候应该加载 skill。
3. Skill 负责规定模型应该怎样解释清楚。

一句话复述：这个插件不是替模型回答，而是在合适的时候提醒模型“先别压缩，按认知适配的方式讲明白”。
