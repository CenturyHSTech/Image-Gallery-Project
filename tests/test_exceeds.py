"""
For the Win: students should pass the tests for this file.
It should be weighted at 1 point for each type of test (2 is recommended)
"""
import pytest
import file_clerk.clerk as clerk
from webcode_tk import css_tools as css
from webcode_tk import html as html

project_dir = "project/"

min_required_elements = [
    ("figure", 12),
    ("img", 12),
    ("a", 12),
    ("figcaption", 12)]

min_number_of_elements = html.get_number_of_elements_per_file(
    project_dir, min_required_elements
)


@pytest.fixture
def html_files():
    html_files = html.get_all_html_files(project_dir)
    return html_files

@pytest.mark.parametrize("file,element,num", min_number_of_elements)
def test_files_for_minimum_number_of_elements(file, element, num):
    if not html_files:
        assert False
    if "or" in element.lower():
        elements = element.split()
        actual = 0
        for el in elements:
            el = el.strip()
            actual += html.get_num_elements_in_file(el, file)
    else:
        actual = html.get_num_elements_in_file(element, file)
    assert actual >= num