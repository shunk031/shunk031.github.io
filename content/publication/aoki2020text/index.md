---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "Text Classification through Glyph-aware Disentangled Character Embedding and Semantic Sub-character Augmentation"
authors: ["Takumi Aoki", "Shunsuke Kitada", "Hitoshi Iyatomi"]
date: 2020-10-25T15:15:41+09:00
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: 2020-10-25T15:15:41+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["1"]

# Publication name and optional abbreviated publication name.
publication: "Proc. of the 1st Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics and the 10th International Joint Conference on Natural Language Processing: Student Research Workshop"
publication_short: "AACL-IJCNLP2020 SRW"

abstract: "
We propose a new character-based text classification framework for non-alphabetic languages, such as Chinese and Japanese. Our framework consists of a variational character encoder (VCE) and character-level text classifier. The VCE is composed of a $\\beta$-variational auto-encoder ($\\beta$-VAE) that learns the proposed glyph-aware disentangled character embedding (GDCE). Since our GDCE provides zero-mean unit-variance character embeddings that are dimensionally independent, it is applicable for our interpretable data augmentation, namely, semantic sub-character augmentation (SSA). In this paper, we evaluated our framework using Japanese text classification tasks at the document- and sentence-level. We confirmed that our GDCE and SSA not only provided embedding interpretability but also improved the classification performance. Our proposal achieved a competitive result to the state-of-the-art model while also providing model interpretability.
"

# Summary. An optional shortened abstract.
summary: "Proc. of the 1st Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics and the 10th International Joint Conference on Natural Language Processing: Student Research Workshop"

tags: ["International Conference", "Refereed", "Natural Language Processing", International Publication]
categories: ["Natural Language Processing", "Glyph-aware NLP", "NLP for Asian Languages"]
featured: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
links:
- name: Preprint
  url: https://arxiv.org/abs/2011.04184
  icon_pack: ai
  icon: arxiv
- name: Code
  url: https://github.com/IyatomiLab/GDCE-SSA
  icon_pack: fab
  icon: github
- name: Video
  url: https://www.youtube.com/watch?v=EWo5yKSJah0
  icon_pack: fab
  icon: youtube

url_pdf: https://www.aclweb.org/anthology/2020.aacl-srw.1/
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

{{< blogcard url="https://www.aclweb.org/anthology/2020.aacl-srw.1/" >}}
