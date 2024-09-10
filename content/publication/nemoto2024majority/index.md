---
# Documentation: https://hugoblox.com/docs/managing-content/

title: "Majority or Minority: Data Imbalance Learning Method for Named Entity Recognition"
authors: ["Sota Nemoto", "Shunsuke Kitada", "Hitoshi Iyatomi"]
date: 2024-01-25T23:20:23+09:00
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: 2024-01-25T23:20:23+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["paper-conference"]

# Publication name and optional abbreviated publication name.
publication: "Practical ML for Low Resource Settings Workshop @ ICLR 2024"
publication_short: "PML4LRS@ICLR 2024"

abstract: "Data imbalance presents a significant challenge in various machine learning (ML) tasks, particularly named entity recognition (NER) within natural language processing (NLP). NER exhibits a data imbalance with a long-tail distribution, featuring numerous minority classes (i.e., entity classes) and a single majority class (i.e., O-class). The imbalance leads to the misclassifications of the entity classes as the O-class. To tackle the imbalance, we propose a simple and effective learning method, named majority or minority (MoM) learning. MoM learning incorporates the loss computed only for samples whose ground truth is the majority class (i.e., the O-class) into the loss of the conventional ML model. Evaluation experiments on four NER datasets (Japanese and English) showed that MoM learning improves prediction performance of the minority classes, without sacrificing the performance of the majority class and is more effective than widely known and state-of-the-art methods. We also evaluated MoM learning using frameworks as sequential labeling and machine reading comprehension, which are commonly used in NER. Furthermore, MoM learning has achieved consistent performance improvements regardless of language, model, or framework.
"

# Summary. An optional shortened abstract.
summary: "[Practical ML for Low Resource Settings Workshop @ ICLR 2024](https://pml4dc.github.io/iclr2024/); Rating: 9: Top 15% of accepted papers, strong accept; Oral presentation"

tags: ["International Conference", "Referred", "Oral Presentation"]
categories: ["Natural Language Processing", "Named Entity Recognition", "Imbalanced Dataset"]
featured: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
links:
- name: Preprint
  url: https://arxiv.org/abs/2401.11431
  icon_pack: ai
  icon: arxiv
- name: PML4LRS@ICLR 2024 Program
  url: https://pml4dc.github.io/iclr2024/program.html#:~:text=Contributed%20Talk9%3A,SOTA%20NEMOTO

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

{{< blogcard url="https://arxiv.org/abs/2401.11431" >}}
