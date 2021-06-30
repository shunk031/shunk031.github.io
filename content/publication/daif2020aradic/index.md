---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "AraDIC: Arabic Document Classification using Image-Based Character Embeddings and Class-Balanced Loss"
authors: ["Mahmoud Daif", "Shunsuke Kitada", "Hitoshi Iyatomi"]
date: 2020-06-21T21:38:33+09:00
doi: "10.18653/v1/2020.acl-srw.29"

# Schedule page publish date (NOT publication's date).
publishDate: 2020-06-21T21:38:33+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["1"]

# Publication name and optional abbreviated publication name.
publication: "Proc. of the 58th Annual Meeting of the Association for Computational Linguistics: Student Research Workshop"
publication_short: "ACL2020 SRW"

abstract: "
Classical and some deep learning techniques for Arabic text classification often depend on complex morphological analysis, word segmentation, and hand-crafted feature engineering.
These could be eliminated by using character-level features.
We propose a novel end-to-end Arabic document classification framework, Arabic document image-based classifier (AraDIC), inspired by the work on image-based character embeddings.
AraDIC consists of an image-based character encoder and a classifier.
They are trained in an end-to-end fashion using the class balanced loss to deal with the long-tailed data distribution problem.
To evaluate the effectiveness of AraDIC, we created and published two datasets, the Arabic Wikipedia title (AWT) dataset and the Arabic poetry (AraP) dataset.
To the best of our knowledge, this is the first image-based character embedding framework addressing the problem of Arabic text classification. 
We also present the first deep learning-based text classifier widely evaluated on modern standard Arabic, colloquial Arabic and classical Arabic.
AraDIC shows performance improvement over classical and deep learning baselines  by 12.29% and 23.05% for the micro and macro F-score, respectively.
"

# Summary. An optional shortened abstract.
summary: "Proc. of the 58th Annual Meeting of the Association for Computational Linguistics: Student Research Workshop"

tags: ["International Conference", "Refereed", "Natural Language Processing"]
categories: ["International Publication", "Refereed", "Natural Language Processing"]
featured: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
links:
- name: Preprint
  url: https://arxiv.org/abs/2006.11586
  icon_pack: ai
  icon: arxiv
- name: Code
  url: https://github.com/mahmouddaif/AraDIC
  icon_pack: fab
  icon: github

url_pdf: https://www.aclweb.org/anthology/2020.acl-srw.29/
url_code:
url_dataset:
url_poster:
url_project:
url_slides:
url_source:
url_video: https://slideslive.com/38928662/aradic-arabic-document-classification-using-imagebased-character-embeddings-and-classbalanced-loss
url_preprint: 

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

{{< blogcard url="https://www.aclweb.org/anthology/2020.acl-srw.29/" >}}
