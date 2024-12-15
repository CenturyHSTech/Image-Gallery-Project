"""
Test for HTML requirements
"""
import pytest
from webcode_tk import html
from webcode_tk import validator_tools as validator

project_dir = "project/"
all_html_files = html.get_all_html_files(project_dir)

# List of required elements (per web page)
required_elements = [("doctype", 1),
                     ("html", 1),
                     ("head", 1),
                     ("title", 1),
                     ("h1", 1)]
min_required_elements = [
    ("div or section or article or main", 1),
    ("figure", 9),
    ("img", 9),
    ("a", 9),
    ("figcaption", 9)]


exact_number_of_elements = html.get_number_of_elements_per_file(
    project_dir, required_elements
)
min_number_of_elements = html.get_number_of_elements_per_file(
    project_dir, min_required_elements
)
html_validation_results = validator.get_project_validation(project_dir)


@pytest.fixture
def html_files():
    html_files = html.get_all_html_files(project_dir)
    return html_files


def test_has_index_file(html_files):
    assert "project/index.html" in html_files


@pytest.mark.parametrize("file,element,num", exact_number_of_elements)
def test_files_for_exact_number_of_elements(file, element, num):
    if not html_files:
        assert False
    actual = html.get_num_elements_in_file(element, file)
    assert actual == num


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


def test_passes_html_validation(html_files):
    errors = []
    if not html_files:
        assert "html files" in html_files
    for file in html_files:
        results = validator.get_markup_validity(file)
        for result in results:
            errors.append(result.get("message"))
    assert not errors
