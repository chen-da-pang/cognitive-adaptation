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
    assert "完整读取 `cognitive-adaptation` skill" in context
    assert "按当前问题选择合适的解释组件" in context


def test_router_requires_reading_skill_without_forcing_a_template(tmp_path: Path):
    """router 必须强制读取 skill，但不能把 skill 重新硬化成固定模板。"""
    output = run_hook("解释一下这个概念", tmp_path)
    context = output["hookSpecificOutput"]["additionalContext"]

    assert "必须" in context
    assert "读取" in context
    assert "逐条执行" not in context
    assert "输出合约" not in context
    assert "固定总结" in context


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


def test_skill_does_not_force_visible_activation_phrase():
    skill_text = SKILL.read_text()
    assert "回答的**第一行**必须原样输出" not in skill_text
    assert "我会用最通俗易懂的方式解释给你听" not in skill_text


def test_skill_is_an_enforceable_adaptive_contract():
    """skill 必须强制认知适配，但不能强制机械栏目。

    防止以后又退回两种坏状态：软到模型不照做，或硬到每轮都模板填空。
    """
    skill_text = SKILL.read_text()

    assert "认知适配规则" in skill_text
    assert "必做" in skill_text
    assert "按需组件" in skill_text
    # fail-closed 自检
    assert "自检" in skill_text
    assert "先重写" in skill_text
    # 红旗清单
    assert "红旗" in skill_text
    assert "不要输出固定的总结栏目" in skill_text
