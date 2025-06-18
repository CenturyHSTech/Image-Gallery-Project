
# Image Gallery Project

This project involves designing and coding an image gallery that displays a minimum of 9 thumbnail images. Each thumbnail links to a full-sized version, and the layout should be responsive and visually styled.

---

<details>
<summary><strong>Project Overview</strong></summary>

Students will design an image gallery project that showcases a minimum of 9 image thumbnails related to a theme, and these thumbnails link to a full-sized image.

The design should be a grid of images styled using fonts, colors, borders, and other CSS properties.

</details>

---
<details>
<summary><strong>Setup Instructions</strong></summary>

1. Place all project files (HTML, CSS, images) into the `simple_html_page` folder.
2. Clone the project: `git clone`
3. Open in VS Code (`Image-Gallery-Project.code-workspace`)
4. Open the terminal (View > New Terminal)
5. Install the Python extension for VS Code
6. Run `poetry shell` in the terminal
7. Note your virtual environment name
8. Open the Command Palette (`Ctrl + Shift + P`)
9. Select the Python interpreter (look for the Poetry environment)
10. Run `poetry update`
11. Run `pytest` to test your code
12. If needed, configure tests via the Testing icon
13. Place your content in the `image_gallery` folder
14. Store all images (full-size and thumbnails)
15. Choose a theme for your gallery
16. Record your final product showing responsiveness
17. Commit and push changes regularly

</details>

---

<details>
<summary><strong>Project Requirements</strong></summary>

### Folder and File Structure
- Create a single web page named `index.html`
- Create a folder titled `images` (all lowercase)
- Include at least 18 images:
  - 9 full-sized images
  - 9 thumbnails (max width: 450px)

### HTML Requirements
- A single HTML file with:
  - All standard HTML5 tags (`DOCTYPE`, `html`, `head`, `title`, `body`)
  - A `header` with a `h1` title
  - A `main` section containing at least 9 `figure` elements
  - Each `figure` includes:
    - A thumbnail image with `alt` text
    - A link to the full-sized image
    - A `figcaption` with a `cite` tag for image credit (linked if not self-taken)

### CSS Requirements
- Use at least one stylesheet or a `<style>` tag
- Font pairing
- Background and text colors with proper contrast:
  - AAA rating for body text
  - AA rating acceptable for headings
- Use `flex` layout for the container
- Style `figure` elements with `margin`, `border`, `padding`, and `background-color`

### Design Requirements
- High contrast and readability
- Thematically consistent images and styling
- Responsive layout that works across all screen sizes

### Validity Requirements
- No HTML or CSS errors (validated via W3C tools)

</details>

---

<details>
<summary><strong>Submission Requirements</strong></summary>

- All changes must be committed and pushed to the repository
- Submit a recording showing the gallery at various viewport widths
- I will be looking for the following design recommendations:
    + your ***layout remains intact*** at all screen widths
    + there are ***no horizontal scrollbars*** (unless the screen is narrower than a single figure)
</details>

---
