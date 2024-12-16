"""
Test CSS Requirements.
"""
import pytest
import file_clerk.clerk as clerk
from webcode_tk import css_tools as css
from webcode_tk import html_tools as html
from webcode_tk import validator_tools as validator

project_dir = "project/"

css_validation_results = validator.get_project_validation(
    project_dir, "css"
)


style_attributes_in_project = css.no_style_attributes_allowed_report(
    project_dir)
css_validation_results = validator.get_project_validation(
    project_dir, "css"
)

color_contrast_results = []
color_contrast_results = css.get_project_color_contrast_report(project_dir)

applying_styles_results = css.styles_applied_report(project_dir)
font_data = css.fonts_applied_report(project_dir)
header_color_rule_data = css.get_heading_color_report(project_dir)


@pytest.mark.parametrize("results", style_attributes_in_project)
def test_css_for_no_style_attributes(results):
    assert "pass" == results[:4]


@pytest.mark.parametrize("results", css_validation_results)
def test_css_validation(results):
    assert "pass" == results[:4]


@pytest.mark.parametrize("results", applying_styles_results)
def test_if_file_applies_styles(results):
    assert "pass" == results[:4]


@pytest.mark.parametrize("results",
                         color_contrast_results)
def test_global_colors(results):
    assert "pass" == results[:4]


@pytest.mark.parametrize("results", font_data)
def test_font_requirements(results):
    assert "pass" == results[:4]


@pytest.mark.parametrize("results", header_color_rule_data)
def test_for_colors_applied_to_headings(results):
    assert "pass" == results[:4]


# Figure property prep
html_files = html.get_all_html_files(project_dir)
styles_by_html_files = css.get_styles_by_html_files(project_dir)


def get_required_properties(required_properties, has_required_properties,
                            dec_block):
    for declaration in dec_block.declarations:
        prop = declaration.property
        if prop in required_properties:
            has_required_properties[prop] = True
        elif "background" in prop:
            # using shorthand?
            split_values = declaration.value.split()
            for value in split_values:
                if css.color_tools.is_hex(value):
                    has_required_properties["background-color"] = True


def get_figure_property_data(html_styles):
    figure_property_data = []
    required_properties = ["border", "padding", "background-color"]
    has_required_properties = {}
    for prop in required_properties:
        has_required_properties[prop] = False
    for styles in html_styles:
        file = styles.get("file")
        selectors = html.get_possible_selectors_by_tag(file, "figure")
        for selector in selectors:
            sheets = styles.get("stylesheets")
            for sheet in sheets:
                block = css.get_declaration_block_from_selector(selector,
                                                                sheet)
                dec_block = css.DeclarationBlock(block)
                get_required_properties(required_properties,
                                        has_required_properties, dec_block)
        # Loop through required properties and all must pass
        missing = []
        for key in has_required_properties:
            uses_prop = has_required_properties.get(key)
            if not uses_prop:
                missing.append(key)
        num_missing = len(missing)
        figure_property_data.append((file, num_missing))
    return figure_property_data


figure_property_data = get_figure_property_data(styles_by_html_files)


def test_container_uses_flex_properties_for_layout(html_styles):
    # get all container permutations and look for flex property
    containers = []

    # assume True until proven otherwise
    applies_flex = True
    for styles in html_styles:
        file = styles.get("file")
        div_selectors = html.get_possible_selectors_by_tag(file, "div")
        section_selectors = html.get_possible_selectors_by_tag(file, "section")
        article_selectors = html.get_possible_selectors_by_tag(file, "article")
        containers += div_selectors
        containers += section_selectors
        containers += article_selectors
    for styles in html_styles:
        has_flex = False
        for selector in containers:
            sheets = styles.get("stylesheets")
            for sheet in sheets:
                declaration_block = css.get_declaration_block_from_selector(
                    selector, sheet
                )
                if declaration_block:
                    if ("display:flex" in declaration_block or
                            "display: flex" in declaration_block):
                        has_flex = True
        applies_flex = applies_flex and has_flex
    assert applies_flex


# Figure Property Tests
css.has_required_property("")

@pytest.mark.parametrize("file,num_missing", figure_property_data)
def test_figure_styles_applied(file, num_missing):
    filename = clerk.get_file_name(file)
    expected = f"{filename} has all figure properties applied."
    if num_missing == 0:
        results = expected
    else:
        results = f"{filename} has {num_missing} figure properties missing"
    assert expected == results
