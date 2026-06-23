from __future__ import annotations

from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_INSTALL_ROOT = PLUGIN_ROOT.parent
SKILL = PLUGIN_INSTALL_ROOT / "skills" / "cognitive-adaptation" / "SKILL.md"
ROUTER = PLUGIN_ROOT / "prompts" / "router-context.md"
REFERENCE_PROMPT = PLUGIN_ROOT / "prompts" / "cognitive-adaptation.md"


def test_skill_keeps_step_by_step_as_required_backbone():
    skill_text = SKILL.read_text()

    assert "逐步拆解" in skill_text
    assert "默认主干" in skill_text or "必做" in skill_text
    assert "不跳步" in skill_text


def test_skill_makes_term_breakdown_conditional_not_global():
    skill_text = SKILL.read_text()

    assert "按需" in skill_text
    assert "术语拆解" in skill_text
    assert "每个术语/缩写/框架名/英文命名" not in skill_text
    assert "代码里的英文变量名、函数名、布尔字段名同样算术语，必须给" not in skill_text


def test_skill_makes_examples_conditional_not_mandatory():
    skill_text = SKILL.read_text()

    assert "例子 / 类比" in skill_text
    assert "只有" in skill_text or "按需" in skill_text
    assert "每个核心概念给 1 个具体例子" not in skill_text


def test_skill_exposes_progressive_disclosure_component_selector():
    skill_text = SKILL.read_text()

    assert "先判断用户当前卡在哪里，只启用相关组件" in skill_text
    assert "卡在词上 -> 术语拆解" in skill_text
    assert "卡在抽象概念上 -> 例子 / 类比" in skill_text
    assert "卡在流程上 -> 强化逐步拆解" in skill_text
    assert "卡在证据可信度上 -> 证据分层" in skill_text
    assert "卡在下一步操作上 -> 行动项" in skill_text
    assert "没有明确卡点 -> 不启用额外组件" in skill_text
    assert "组件是工具箱，不是输出清单" in skill_text


def test_required_section_stays_short_without_explanation_levels():
    skill_text = SKILL.read_text()
    router_text = ROUTER.read_text()
    combined_text = f"{skill_text}\n{router_text}"

    assert "一句话大白话结论" in skill_text
    assert "逐步拆解" in skill_text
    assert "短段落" in skill_text
    assert "解释强度" not in combined_text
    assert "Lite" not in combined_text
    assert "Normal" not in combined_text
    assert "Deep" not in combined_text


def test_evidence_guidance_is_an_on_demand_component():
    skill_text = SKILL.read_text()

    assert "### 证据分层" in skill_text
    assert "启用条件" in skill_text
    assert "禁用条件" in skill_text
    assert "最小写法" in skill_text
    assert "事实、推断、建议、社区经验" in skill_text


def test_skill_removes_remember_section_as_output_requirement():
    skill_text = SKILL.read_text()

    assert "你现在该记住什么" not in skill_text
    assert "节末可以补一句" not in skill_text


def test_router_activates_skill_without_forcing_every_component():
    router_text = ROUTER.read_text()

    assert "先完整读取" in router_text
    assert "逐条执行" not in router_text
    assert "输出合约" not in router_text
    assert "按当前问题选择合适的解释组件" in router_text
    assert "不要以泛泛邀约收尾" in router_text


def test_reference_prompt_matches_adaptive_rules():
    prompt_text = REFERENCE_PROMPT.read_text()

    assert "不要为了完成格式而硬凑例子" in prompt_text
    assert "不要为了整齐而机械套模板" in prompt_text
    assert "节末可以补一句" not in prompt_text


def test_reference_prompt_removes_old_forced_research_and_example_rules():
    prompt_text = REFERENCE_PROMPT.read_text()

    assert "先判断用户当前卡在哪里，只启用相关组件" in prompt_text
    assert "组件是工具箱，不是输出清单" in prompt_text
    assert "复杂概念至少给一个具体例子" not in prompt_text
    assert "官方资料和社区资料同等重要" not in prompt_text
    assert "我有没有把官方信息和社区反馈都查到并讲清楚" not in prompt_text
    assert "减少 2 到 3 轮追问" not in prompt_text


def test_skill_discourages_depth_mode_rewrites():
    skill_text = SKILL.read_text()

    assert "不要把按需组件改写成深浅档位" in skill_text
    assert "表达深度" not in skill_text


def test_skill_discourages_template_followup_offers():
    skill_text = SKILL.read_text()
    prompt_text = REFERENCE_PROMPT.read_text()

    assert "不要固定追加" in skill_text
    assert "如果你愿意" in skill_text
    assert "最终回答中不要出现\"如果你愿意\"" in skill_text
    assert "除非用户明确要求下一步" in skill_text
    assert "写示例回复时也不要把禁用短语放进示例" in skill_text
    assert "写示例回复时也不要把禁用短语放进示例" in prompt_text


def test_single_concept_explanations_stay_bounded():
    skill_text = SKILL.read_text()
    prompt_text = REFERENCE_PROMPT.read_text()

    assert "单一陌生概念" in skill_text
    assert "不要展开成完整背景教程" in skill_text
    assert "单一陌生概念" in prompt_text
    assert "不要展开成完整背景教程" in prompt_text


def test_skill_discourages_old_hardening_terms_in_rewrites():
    skill_text = SKILL.read_text()

    assert "逐条执行" in skill_text
    assert "输出合约" in skill_text
    assert "推荐改写" in skill_text
