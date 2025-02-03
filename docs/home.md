# Welcome

This is the documentation for **miniHTML**, a lightweight markup language.

## Syntax

MiniHTML uses a very simple syntax:
```
tag[children]{text}(attributes)
```
This makes it easy to pick up for beginners.

### Tags

- **d** : a container, similar to a `<div>` in HTML
- **p** : a paragraph of text
- **br** : line break
- **i** : image
- **l** : link, equivalent to an anchor (`<a>`) in HTML
- **hl-hsss** : varying header sizes, from `hl` (largest) to `hsss` (smallest)
- **hline** : horizontal line

### Examples

Here are some examples of miniHTML syntax:

- **Container**:
  ```
  d[]{}
  ```

- **Paragraph**:
  ```
  p[]{This is a paragraph.}
  ```

- **Image**:
  ```
  i[]{src="image.jpg" alt="An image"}
  ```

- **Link**:
  ```
  l[]{Click here}(href="https://example.com")
  ```

- **Header**:
  ```
  hl[]{This is a header}
  ```

- **Horizontal Line**:
  ```
  hline()
  ```

### Styles

MiniHTML supports various styles to enhance the appearance of your content. Below are the available styles and their corresponding CSS properties:

- **bold**: `font-weight: bold`
- **italic**: `font-style: italic`
- **underline**: `text-decoration: underline`
- **strike**: `text-decoration: line-through`
- **text-center**: `text-align: center`
- **text-right**: `text-align: right`
- **card**: `border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin: 10px 0`
- **color**: `color: {value}`
- **size**: `font-size: {value}`
- **font**: `font-family: {value}`
- **background**: `background-color: {value}`
- **padding**: `padding: {value}`
- **margin**: `margin: {value}`
- **m**: `margin: {value}`
- **p**: `padding: {value}`
- **codeblock**: `background-color: #f4f4f4; padding: 10px; border-left: 3px solid #ccc`
- **width**: `width: {value}`
- **height**: `height: {value}`
- **width-height**: `width: {value}; height: {value}`

### Example Usage of Styles

Here are some examples of how to use styles in miniHTML:

- **Bold Text**:
  ```
  p[bold]{This is bold text.}
  ```

- **Centered Text**:
  ```
  p[text-center]{This text is centered.}
  ```

- **Card Container**:
  ```
  d[card]{This is a card container.}
  ```

### Classes

Classes can be applied to any element using the `class=""` attribute within the parentheses. Global styles for a class can be assigned using the `s-classname` tag.

#### Example Usage of Classes

- **Applying a Class**:
  ```
  p[class="myClass"]{This paragraph has a class.}
  ```

- **Defining a Global Style for a Class**:
  ```
  s-myClass(style="bold")
  ```

## Examples

Here are some example miniHTML files demonstrating various features:

- [Classes Example](https://github.com/meepstertron/miniHTML/blob/main/examples/get_some_class.mhtml): Demonstrates how to use classes.
- [Hello World Example](https://github.com/meepstertron/miniHTML/blob/main/examples/helloworld.mhtml): A simple "Hello World" example.
- [Images Example](https://github.com/meepstertron/miniHTML/blob/main/examples/hows_my_image.mhtml): Shows how to include images.
- [Horizontal Lines Example](https://github.com/meepstertron/miniHTML/blob/main/examples/lining.mhtml): Demonstrates the use of horizontal lines.
- [Inline Styles Example](https://github.com/meepstertron/miniHTML/blob/main/examples/you_got_some_style.mhtml): Shows how to apply inline styles.

I recommend starting with the Hello World example.

## Installing the Web Server

To install the web server, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/meepstertron/miniHTML.git
   ```

2. Navigate to the `docker-webserver` directory:
   ```
   cd docker-webserver
   ```

3. Build the Docker image:
   ```
   docker build -t minihtml-webserver .
   ```

4. Run the Docker container:
   ```
   docker run -d -p 80:80 -v /path/to/your/minihtml/files:/app/minihtml minihtml-webserver
   ```

The web server will run on port 80. Place your `.mhtml` or `.minihtml` files in the `/app/minihtml` directory.

## Help, I'm Stuck

If you get stuck or have questions, feel free to contact me on the Hack Club Slack or via email:

- [Hack Club Slack](https://hackclub.slack.com/team/U087PR1B2HX)
- Email: meepstertron@gmail.com
