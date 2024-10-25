---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "DM$^2$S$^2$: Deep Multi-Modal Sequence Sets with Hierarchical Modality Attention"
authors: ["Shunsuke Kitada", "Yuki Iwazaki", "Riku Togashi", "Hitoshi Iyatomi"]
author_notes: ["This work was conducted during the first author's internship at CyberAgent Inc."]
date: 2022-11-14T00:00:00+09:00
doi: "10.1109/ACCESS.2022.3221812"

# Schedule page publish date (NOT publication's date).
publishDate: 2022-11-14T00:00:00+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["article-journal"]

# Publication name and optional abbreviated publication name.
publication: "IEEE Access"
publication_short: "IEEE Access"

abstract: "
There is increasing interest in the use of multimodal data in various web applications, such as digital advertising and e-commerce. Typical methods for extracting important information from multimodal data rely on a mid-fusion architecture that combines the feature representations from multiple encoders. However, as the number of modalities increases, several potential problems with the mid-fusion model structure arise, such as an increase in the dimensionality of the concatenated multimodal features and missing modalities. To address these problems, we propose a new concept that considers multimodal inputs as a set of sequences, namely, deep multimodal sequence sets (DM$^2$S$^2$). Our set-aware concept consists of three components that capture the relationships among multiple modalities: (a) a BERT-based encoder to handle the inter- and intra-order of elements in the sequences, (b) intra-modality residual attention (IntraMRA) to capture the importance of the elements in a modality, and (c) inter-modality residual attention (InterMRA) to enhance the importance of elements with modality-level granularity further. Our concept exhibits performance that is comparable to or better than the previous set-aware models. Furthermore, we demonstrate that the visualization of the learned InterMRA and IntraMRA weights can provide an interpretation of the prediction results.
"

# Summary. An optional shortened abstract.
summary: "IEEE Access (**Impact Factor: 3.476** in 2021; [1st place in Engineering & Computer Science (general) at Google Scholar Metrics](https://scholar.google.com/citations?view_op=top_venues&hl=en&vq=eng_enggeneral))"

tags: ["Journal", "International Publication", "Multi-modal model", "Vision & Language", "Refereed", "Open Access", "CyberAgent", "IEEE"]
categories: ["Multi-modal model", "Vision & Language", "Natural Language Processing", "Attention Mechanisms"]
featured: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
links:
- name: Preprint
  url: https://arxiv.org/abs/2209.03126
  icon_pack: ai
  icon: arxiv

url_pdf: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9947020
url_code:
url_dataset: https://doi.org/10.5281/zenodo.7050923
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

<a href="https://www.scimagojr.com/journalsearch.php?q=21100374601&amp;tip=sid&amp;exact=no" title="SCImago Journal &amp; Country Rank"><img border="0" src="https://www.scimagojr.com/journal_img.php?id=21100374601" alt="SCImago Journal &amp; Country Rank"  /></a>
