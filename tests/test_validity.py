"""
Test for HTML and CSS validity
"""
from file_clerk import clerk
import pytest
from webcode_tk import validator_tools as validator


html_results = []
html_files = clerk.get_all_files_of_type("project/", "html")
for file in html_files:
    report = validator.get_markup_validity(file)
    expected = f"{file}: No Errors Found."
    if not report:
        result = expected
        html_results.append((result, expected))
    else:
        for error in report:
            error_message = error.get("message")
            result = f"{file}: {error_message}"
            html_results.append((result, expected))


css_results = []
css_files = clerk.get_all_files_of_type("single_html_page/", "css")
for file in css_files:
    # Get code
    code = clerk.file_to_string(file)

    # validate code
    css_validation_results = validator.validate_css(code)
    is_valid = validator.is_css_valid(css_validation_results)
    expected = f"{file}: No Errors Found."
    if is_valid:
        css_results.append((expected, expected))
    else:
        errors = validator.get_css_errors_list(css_validation_results)
        for error in errors:
            result = f"{file}: {error_message}"
            css_results.append((result, expected))


@pytest.mark.parametrize("result,expected", html_results)
def test_html_validity(result, expected):
    assert result == expected


@pytest.mark.parametrize("result,expected", css_results)
def test_css_validity(result, expected):
    print(file)
    assert result == expected
