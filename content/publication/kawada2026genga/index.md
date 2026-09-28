---
# Documentation: https://docs.hugoblox.com/managing-content/

title: "GenGA: Editable and Data-Grounded Graphical Abstract Generation for Academic Papers"
authors: ["Takuro Kawada", "Shunsuke Kitada", "Hitoshi Iyatomi"]
date: 2026-08-06T08:53:02+09:00
doi: "https://doi.org/10.48550/arXiv.2608.05478"

# Schedule page publish date (NOT publication's date).
publishDate: 2026-08-06T08:53:02+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["article"]

# Publication name and optional abbreviated publication name.
publication: ""
publication_short: ""

abstract: "Graphical Abstracts (GAs) visually summarize the key findings of academic papers, playing a crucial role in facilitating the understanding of research content. Recently, advancements in vision-language models and image generation models have enabled the automatic generation of scientific figures based on paper content. However, most conventional methods output the generated results as raster graphics, making post-editing (e.g., text modification and layout changes) highly difficult. This poses a significant challenge, as they are unsuitable for the iterative figure revision process inherent in paper writing and peer review. To tackle these challenges, we define the novel task of generating editable GAs from paper content and propose GenGA, a new GA generation framework that directly produces figures in vector format. By generating figures as a collection of vector elements with a hierarchical structure, GenGA produces outputs that can be seamlessly imported into existing drawing tools for intuitive, element-level editing. Furthermore, we introduce the Structural Independence Coefficient (SIC), a metric that quantifies the editing simplicity of a figure based on the degree to which local modifications propagate to other elements. Experimental results show that GenGA achieves superior editing simplicity compared to conventional methods, and even surpasses human-authored GAs in conciseness and semantic alignment. We also validate SIC as an effective metric correlated with manual editing costs. This study fundamentally redefines GA generation as an editable vector graphic generation problem grounded in the practical workflows of researchers, significantly promoting effective scientific communication."

# Summary. An optional shortened abstract.
summary: "arXiv preprint"

tags:
  [
    "Preprint",
    "AI for Science",
    "Computer Vision",
    "Vision & Language",
    "Creative Graphic Design",
  ]
categories: ["Vision & Language", "AI for Science", "Creative Graphic Design"]
featured: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
links:
  - name: Preprint
    url: https://arxiv.org/abs/2608.05478
    icon_pack: ai
    icon: arxiv

url_pdf: https://arxiv.org/pdf/2608.05478
url_code:
url_dataset:
url_poster:
url_project:
url_slides:
url_source:
url_video:

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: true

# Associated Projects (optional).
#   Associate this publication with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `internal-project` references `content/project/internal-project/index.md`.
#   Otherwise, set `projects: []`.
projects: []

# Slides (optional).
#   Associate this publication with Markdown slides.
#   Simply enter your slide deck's filename without extension.
#   E.g. `slides: "example"` references `content/slides/example/index.md`.
#   Otherwise, set `slides: ""`.
slides: ""
---
