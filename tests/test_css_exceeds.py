"""
For the Win: students should pass the tests for this file.
It should be weighted at 1 point for each type of test (2 is recommended)
"""
import pytest
from webcode_tk import css_tools as css

project_dir = "project/"

advanced_properties_goals = {
        "figure": {
            "properties": ("box-shadow", "border-radius", "animation"),
            "min_required": 2,
        }
    }
advanced_properties_report = css.get_properties_applied_report(project_dir,
                                                               advanced_properties_goals)

@pytest.mark.parametrize("results", advanced_properties_report)
def test_for_advanced_properties_applied(results):
    assert "pass:" in results[:5]
