"""
Test CSS Requirements.
"""
import pytest
import file_clerk.clerk as clerk
from webcode_tk import css_tools as css
from webcode_tk import html_tools as html

project_path = "project/"
html_files = html.get_all_html_files(project_path)
styles_by_html_files = css.get_styles_by_html_files(project_path)
global_color_rules = []
for file in html_files:
    global_color_rules.append(css.get_global_colors(file))
global_color_contrast_tests = []
no_style_attribute_tests = []


def get_all_color_rule_results(project_path):
    color_rule_results = css.get_project_color_contrast(project_path)
    return color_rule_results


def set_style_attribute_tests(path):
    results = []
    for file in html_files:
        data = html.get_style_attribute_data(file)
        if data:
            for datum in data:
                results.append(datum)
    return results


def get_unique_font_families(project_folder):
    font_rules = css.get_unique_font_rules(project_folder)
    font_families_tests = []
    for file in font_rules:
        # apply the file, unique rules, unique selectors, and unique values
        filename = file.get("file")
        unique_rules = file.get("rules")
        passes_rules = len(unique_rules) >= 2
        passes_selectors = passes_rules
        unique_values = []
        for rule in unique_rules:
            value = rule.get("family")
            if value not in unique_values:
                unique_values.append(value)
        passes_values = len(unique_values) == 2
        font_families_tests.append((filename, passes_rules, passes_selectors,
                                    passes_values))
    return font_families_tests


def get_font_rules_data(font_tests):
    rules_data = []
    for test in font_tests:
        rules_data.append(test[:2])
    return rules_data


def get_font_selector_data(font_tests):
    rules_data = []
    for test in font_tests:
        rules_data.append((test[0], test[2]))
    return rules_data


def get_font_family_data(font_tests):
    rules_data = []
    for test in font_tests:
        rules_data.append((test[0], test[3]))
    return rules_data


def prep_global_color_tests(global_color_contrast_tests,
                            global_color_rules):
    for rule in global_color_rules:
        if rule:
            path = list(rule.keys())[0]
            file = clerk.get_file_name(path)
            data = rule[path]
            if isinstance(data, list):
                if len(data) == 1:
                    data = data[0]
            selector = data.get("selector")
            ratio = data.get("contrast_ratio")
            passes = data.get("passes_normal_aaa")
            global_color_contrast_tests.append(
                (file, selector, ratio, passes)
            )


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


figure_property_data = get_figure_property_data(styles_by_html_files)
prep_global_color_tests(global_color_contrast_tests,
                        global_color_rules)
font_families_tests = get_unique_font_families(project_path)
font_rules_results = get_font_rules_data(font_families_tests)
font_selector_results = get_font_selector_data(font_families_tests)
font_family_results = get_font_family_data(font_families_tests)
all_color_rules_results = get_all_color_rule_results(project_path)
style_attributes_data = set_style_attribute_tests(project_path)
if not style_attributes_data:
    style_attributes_data = [(file, "no tag", "applies style attribute")]
link_colors = css.get_link_color_data(project_path)


@pytest.fixture
def project_folder():
    return project_path


@pytest.fixture
def all_color_data():
    return all_color_rules_results


@pytest.fixture
def html_styles():
    return styles_by_html_files


@pytest.fixture
def html_docs():
    return html_files


@pytest.fixture
def link_color_details():
    return link_colors


@pytest.mark.parametrize("file,tag,value", style_attributes_data)
def test_files_for_style_attribute_data(file, tag, value):
    if tag == "no tag" and value == "applies style attribute":
        results = f"{file} passes with no style attributes."
        expected = results
        assert results == expected
    else:
        results = f"Tag: <{tag}> from '{file}' has a style attribute"
        assert not results


def test_files_for_has_style_attributes(project_folder):
    results = "No style attributes found"
    expected = results
    html_files = html.get_all_html_files(project_folder)
    for file in html_files:
        has_style_attribute = html.has_style_attribute_data(file)
        if has_style_attribute:
            filename = clerk.get_file_name(file)
            results = f"{filename} has style attributes"
    assert expected == results


@pytest.mark.parametrize("file,selector,ratio,results",
                         global_color_contrast_tests)
def test_files_for_global_color_contrast(file, selector, ratio, results):
    result = f"Color contrast for {selector} passes with {ratio} ratio."
    expected = result
    if not results:
        results = f"Color contrast for {file} failed."
    assert result == expected


@pytest.mark.parametrize("file,passes_rules", font_selector_results)
def test_files_for_enough_font_rules(file, passes_rules):
    assert passes_rules


@pytest.mark.parametrize("file,passes_selector", font_selector_results)
def test_files_for_for_enough_font_selectors(file, passes_selector):
    assert passes_selector


@pytest.mark.parametrize("file,passes_font_families", font_selector_results)
def test_files_for_2_font_families_max(file, passes_font_families):
    assert passes_font_families


def test_link_color_details_for_links_targeted(link_color_details):
    assert link_color_details


@pytest.mark.parametrize("file,sel,goal,col,bg,ratio,passes",
                         link_colors)
def test_link_color_details_for_passing_color_contrast(file, sel, goal,
                                                       col, bg, ratio,
                                                       passes):
    filename = file.split("/")[-1]
    if passes:
        results = f"Color contrast for {sel} in {filename} passes at {ratio}"
        expected = results
        assert results == expected
    else:
        results = f"Color contrast for {sel} in {filename} fails at {ratio}"
        expected = f"Color contrast for {sel} in {filename} passes."
        assert results == expected


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


@pytest.mark.parametrize("file,num_missing", figure_property_data)
def test_figure_styles_applied(file, num_missing):
    filename = clerk.get_file_name(file)
    expected = f"{filename} has all figure properties applied."
    if num_missing == 0:
        results = expected
    else:
        results = f"{filename} has {num_missing} figure properties missing"
    assert expected == results
