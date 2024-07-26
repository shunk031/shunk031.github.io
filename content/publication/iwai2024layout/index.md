---
# Documentation: https://docs.hugoblox.com/managing-content/

title: "Layout-Corrector: Alleviating Layout Sticking Phenomenon in Discrete Diffusion Model"
authors: ["Shoma Iwai", "Atsuki Osanai", "Shunsuke Kitada", "Shinichiro Omachi"]
author_notes: ["This work was conducted during the first author's internship at LY Corporation."]
date: 2024-07-01T08:00:00+00:00
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: 2024-07-01T08:00:00+00:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["paper-conference"]

# Publication name and optional abbreviated publication name.
publication: "Proc. of the European Conference on Computer Vision. 2024."
publication_short: "ECCV2024"

abstract: "Layout generation is a task to synthesize a harmonious layout with elements characterized by attributes such as category, position, and size. Human designers experiment with the placement and modification of elements to create aesthetic layouts, however, we observed that current discrete diffusion models (DDMs) struggle to correct inharmonious layouts after they have been generated. In this paper, we first provide novel insights into layout sticking phenomenon in DDMs and then propose a simple yet effective layout-assessment module Layout-Corrector, which works in conjunction with existing DDMs to address the layout sticking problem. We present a learning-based module capable of identifying inharmonious elements within layouts, considering overall layout harmony characterized by complex composition. During the generation process, Layout-Corrector evaluates the correctness of each token in the generated layout, reinitializing those with low scores to the ungenerated state. The DDM then uses the high-scored tokens as clues to regenerate the harmonized tokens. Layout-Corrector, tested on common benchmarks, consistently boosts layout-generation performance when in conjunction with various state-of-the-art DDMs. Furthermore, our extensive analysis demonstrates that the Layout-Corrector (1) successfully identifies erroneous tokens, (2) acilitates control over the fidelity-diversity trade-off, and (3) significantly mitigates the performance drop associated with fast sampling"

# Summary. An optional shortened abstract.
summary: "Proc. of the European Conference on Computer Vision (ECCV2024). (**Acceptance rate = ??%**)"

tags: ["International Conference", "Refereed", "Layout Generation", "Discrete Diffusion Model", "LYCorp", "International Publication", "Springer"]
categories: ["Layout Generation", "Creative Graphic Design"]
featured: true

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
# links:
# - name: Follow
#   url: https://twitter.com
#   icon_pack: fab
#   icon: twitter

url_pdf:
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
  preview_only: false

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
