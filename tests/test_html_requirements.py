"""
Test for HTML requirements
"""
from file_clerk import clerk
import pytest
from webcode_tk import html_tools as html

required_elements = [("doctype", 1),
                     ("html", 1),
                     ("head", 1),
                     ("title", 1),
                     ("h1", 1),
                     ("container (div, section, or article)", 1),
                     ("figure", 9),
                     ("img", 9),
                     ("a", 9),
                     ("figcaption", 9)]


@pytest.fixture
def files():
    files = clerk.get_all_files_of_type("project/", "html")
    return files


@pytest.mark.parametrize("element,num", required_elements)
def test_files_for_required_elements(element, num, files):
    if not files:
        assert False
    for file in files:
        if "container" in element:
            actual = html.get_num_elements_in_file("div", file)
            actual += html.get_num_elements_in_file("section", file)
            actual += html.get_num_elements_in_file("article", file)
        else:
            actual = html.get_num_elements_in_file(element, file)
        assert actual >= num


def test_for_presence_of_html_files(files):
    assert len(files) > 0
