# Welcome to Mini HTML

Mini HTML is a lightweight markup language designed for environments with slow connections, where minimizing data size is crucial. It aims to provide a simple and efficient way to create web pages with minimal overhead. Made for low power devices

More to come in the future!

## Features

- **Lightweight**: Minimal syntax and small file sizes.
- **Fast**: Optimized for quick parsing and rendering.
- **Easy to Learn**: Simple and intuitive syntax.
- **Flexible**: Can be used for a variety of web content.

## Getting Started

To start using Mini HTML, follow these steps:

1. **Download**: Clone using git.
2. **Build**: Build the docker container
3. **Create**: Start creating your web pages using Mini HTML syntax.

## Syntax Overview

Here is a brief overview of the Mini HTML syntax:

- **hl**: Header large
- **hm**: Header medium
- **hs**: Header small
- **hss**: Header smaller
- **hsss**: Header smallest
- **p**: Paragraph
- **d**: Div (container)
- **i**: Image
- **l**: Link
- **br**: Line break
- **hline**: Horizontal line


## Example

```minihtml
[
    // Title Section
    hl{MiniHTML Feature Showcase}(style="text-center color(#2c3e50)")
    p{A comprehensive demonstration of MiniHTML capabilities}(style="text-center italic")
    hline{}

    // Text Styling Section
    hm{Text Styles}
    d(style="card")[
        p{Normal text}
        p{Bold text}(style="bold")
        p{Italic text}(style="italic")
        p{Underlined text}(style="underline")
        p{Strikethrough text}(style="strike")
        p{Colored text}(style="color(#e74c3c)")
        p{Custom font}(style="font(Arial)")
        p{Large text}(style="size(24px)")
    ]

    // Layout Section
    hm{Layout Features}
    d(style="card")[
        d(style="text-center")[
            p{Centered text block}
        ]
        d(style="text-right")[
            p{Right-aligned text}
        ]
        d(style="background(#f0f0f0) padding(20px)")[
            p{Padded container with background}
        ]
    ]

    // Media Section
    hm{Media Elements}
    d(style="card")[
        i(src="https://picsum.photos/300/200" style="width(300px)")
        br{}
        l{Visit Example}(href="https://example.com" style="color(#3498db)")
    ]

    // Headings Section
    hm{Heading Levels}
    d(style="card")[
        hl{Heading 1}
        hm{Heading 2}
        hs{Heading 3}
        hss{Heading 4}
        hsss{Heading 5}
    ]

    // Special Components
    hm{Special Components}
    d(style="card background(#f8f9fa) margin(20px) padding(15px)")[
        p{Card with custom styling}(style="bold")
        hline{}
        p{Multiple styles combined}(style="color(#9b59b6) size(18px) italic")
    ]

    d(style="card background(#f8f9fa) margin(20px) padding(5px)")[
        p{can you guess how big the file is?}
        p{1.73 KB!}(style="italic")
        br()
        p{In normal html this would be about:}
        p{4KB!}(style="bold color(red)")
    ]

    // Deployment Section
    hm{Deployment Features}
    d(style="card background(#e8f5e9) margin(20px) padding(15px)")[
        p{MiniHTML includes a webserver with auto deployment!}(style="bold color(#2e7d32)")
        p{Changes are automatically deployed whenever you save the file.}(style="italic")
    ]
]
```

## Contributing

We welcome contributions! This is opensource afterall!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.

## Disclaimer

Some bugs were fixed, and commit messages were generated with the assistance of GitHub Copilot.

## Contact

For any questions or feedback, please contact me at [jan.koch@hexagonical.ch](mailto:jan.koch@hexagonical.ch).

Thank you for using Mini HTML!