from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_INSTALL_ROOT = PLUGIN_ROOT.parent
HOOK = PLUGIN_INSTALL_ROOT / "hooks" / "user-prompt-submit"
HOOKS_JSON = PLUGIN_INSTALL_ROOT / "hooks" / "hooks.json"
SKILL = PLUGIN_INSTALL_ROOT / "skills" / "cognitive-adaptation" / "SKILL.md"


def run_hook(prompt: str, tmp_path: Path) -> dict:
    env = os.environ.copy()
    env["PLUGIN_ROOT"] = str(PLUGIN_INSTALL_ROOT)

    result = subprocess.run(
        [str(HOOK)],
        input=json.dumps({"prompt": prompt}, ensure_ascii=False),
        text=True,
        capture_output=True,
        check=True,
        env=env,
    )
    assert result.stderr == ""
    return json.loads(result.stdout)


def test_any_prompt_returns_router_context(tmp_path: Path):
    output = run_hook("调研一下 agent team是什么 有什么功能 官方怎么定义的", tmp_path)

    context = output["hookSpecificOutput"]["additionalContext"]
    assert output["hookSpecificOutput"]["hookEventName"] == "UserPromptSubmit"
    assert "<cognitive_adaptation_router>" in context
    assert "请使用 `cognitive-adaptation` skill" in context


def test_router_is_imperative_not_a_soft_suggestion(tmp_path: Path):
    """router 必须用强指令措辞，强制模型先读取并执行 skill，而不是软性'请使用'。"""
    output = run_hook("解释一下这个概念", tmp_path)
    context = output["hookSpecificOutput"]["additionalContext"]

    assert "必须" in context
    assert "读取" in context and "执行" in context


def test_implementation_prompt_also_returns_router_context(tmp_path: Path):
    output = run_hook("修复 pytest 失败并提交", tmp_path)

    context = output["hookSpecificOutput"]["additionalContext"]
    assert "否则忽略本条上下文" in context


def test_hook_ignores_payload_shape(tmp_path: Path):
    env = os.environ.copy()
    env["PLUGIN_ROOT"] = str(PLUGIN_INSTALL_ROOT)

    result = subprocess.run(
        [str(HOOK)],
        input="not-json and ignored",
        text=True,
        capture_output=True,
        check=True,
        env=env,
    )
    output = json.loads(result.stdout)
    assert output["hookSpecificOutput"]["hookEventName"] == "UserPromptSubmit"


def test_hook_config_does_not_run_classifier():
    config = json.loads(HOOKS_JSON.read_text())
    command = config["hooks"]["UserPromptSubmit"][0]["hooks"][0]["command"]

    assert "run-hook.cmd" in command
    assert "user-prompt-submit" in command
    assert "COGNITIVE_ADAPTATION_CLASSIFIER_MODE" not in command
    assert "COGNITIVE_ADAPTATION_LLM" not in command


def test_skill_has_visible_activation_phrase():
    skill_text = SKILL.read_text()
    assert "我会用最通俗易懂的方式解释给你听" in skill_text


def test_skill_is_an_enforceable_contract():
    """skill 必须是可执行的输出合约，而不是软性原则集合。

    防止以后又退回'建议/尽量'式的软规则——那正是模型不照做的根因。
    """
    skill_text = SKILL.read_text()

    # 输出合约 + 强制结构
    assert "输出合约" in skill_text
    # fail-closed 自检
    assert "自检" in skill_text
    assert "先重写" in skill_text
    # 红旗清单
    assert "红旗" in skill_text
