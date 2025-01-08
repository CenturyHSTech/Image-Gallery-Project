"""
For the Win students should pass the tests for this file
by applying at least 2 advanced properties to the figure
tag and 2 flex-related properties to main.
"""
import pytest
from webcode_tk import css_tools as css

project_dir = "project/"

advanced_properties_goals = {
        "figure": {
            "properties": ("box-shadow", "border-radius", "animation"),
            "min_required": 2,
        },
        "main": {
            "properties": ("display", "justify-content", "align-items"),
            "min_required": 2,
        }
    }
advanced_properties_report = css.get_properties_applied_report(
    project_dir,
    advanced_properties_goals)


@pytest.mark.parametrize("results", advanced_properties_report)
def test_for_css_exceeds_advanced_properties_applied(results):
    assert "pass:" in results[:5]
