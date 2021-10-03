---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Skin lesion classification with ensemble of squeeze-and-excitation networks and semi-supervised learning"
authors: ["Shunsuke Kitada", "Hitoshi Iyatomi"]
date: 2018-09-07T00:00:00+09:00
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: 2020-03-29T03:03:35+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["3"]

# Publication name and optional abbreviated publication name.
publication: "Manuscript for the International Skin Imaging Collaboration 2018"
publication_short: "ISIC2018"

abstract: "In this report, we introduce the outline of our system in Task 3: Disease Classification of ISIC 2018: Skin Lesion Analysis Towards Melanoma Detection. We fine-tuned multiple pre-trained neural network models based on Squeeze-and-Excitation Networks (SENet) which achieved state-of-the-art results in the field of image recognition. In addition, we used the mean teachers as a semi-supervised learning framework and introduced some specially designed data augmentation strategies for skin lesion analysis. We confirmed our data augmentation strategy improved classification performance and demonstrated 87.2% in balanced accuracy on the official ISIC2018 validation dataset."

# Summary. An optional shortened abstract.
summary: "Manuscript for [the International Skin Imaging Collaboration 2018](https://challenge2018.isic-archive.com/)."

tags: ["Preprint", "Medical Image Processing"]
categories: ["Medical Image Processing", "Skin Lesion Diagnosis"]
featured: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
links:
- name: Preprint
  url: https://arxiv.org/abs/1809.02568
  icon_pack: ai
  icon: arxiv

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

{{< blogcard url="https://arxiv.org/abs/1809.02568" >}}
