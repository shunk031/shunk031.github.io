---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Attention Meets Perturbations: Robust and Interpretable Attention with Adversarial Training"
authors: ["Shunsuke Kitada", "Hitoshi Iyatomi"]
date: 2020-10-01T23:42:38+09:00
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: 2020-10-01T23:42:38+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["3"]

# Publication name and optional abbreviated publication name.
publication: ""
publication_short: ""

abstract: "In recent years, deep learning models have placed more emphasis on the interpretability and robustness of models. The attention mechanism is an important technique that contributes to these elements and is widely used, especially in the natural language processing (NLP) field. Adversarial training (AT) is a powerful regularization technique for enhancing the robustness of neural networks and has been successful in many applications. The application of AT to the attention mechanism is expected to be highly effective, but there is little research on this. In this paper, we propose a new general training technique for NLP tasks, using AT for attention (Attention AT) and more interpretable adversarial training for attention (Attention iAT). Our proposals improved both the prediction performance and interpretability of the model by applying AT to the attention mechanisms. In particular, Attention iAT enhances those advantages by introducing adversarial perturbation, which differentiates the attention of sentences where it is unclear which words are important. We performed various NLP tasks on ten open datasets and compared the performance of our techniques to a recent model using attention mechanisms. Our experiments revealed that AT for attention mechanisms, especially Attention iAT, demonstrated (1) the best prediction performance in nine out of ten tasks and (2) more interpretable attention (i.e., the resulting attention correlated more strongly with gradient-based word importance) for all tasks. Additionally, our techniques are (3) much less dependent on perturbation size in AT. Our code and more results are available at [this https URL](https://github.com/shunk031/attention-meets-perturbation)"

# Summary. An optional shortened abstract.
summary: ""

tags: ["Natural Language Processing"]
categories: ["Preprint"]
featured: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
links:
- name: Preprint
  url: https://arxiv.org/abs/2009.12064
  icon_pack: ai
  icon: arxiv
- name: Code
  url: https://github.com/shunk031/attention-meets-perturbation
  icon_pack: fab
  icon: github

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
