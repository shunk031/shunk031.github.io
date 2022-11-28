---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "Making Attention Mechanisms More Robust and Interpretable with Virtual Adversarial Training"
authors: ["Shunsuke Kitada", "Hitoshi Iyatomi"]
date: 2022-10-27T21:33:00+09:00
doi: "10.1007/s10489-022-04301-w"

# Schedule page publish date (NOT publication's date).
publishDate: 2022-10-27T21:33:00+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["2"]

# Publication name and optional abbreviated publication name.
publication: "Applied Intelligence"
publication_short: "APIN"

abstract: "Although attention mechanisms have become fundamental components of deep learning models, they are vulnerable to perturbations, which may degrade the prediction performance and model interpretability. Adversarial training (AT) for attention mechanisms has successfully reduced such drawbacks by considering adversarial perturbations. However, this technique requires label information, and thus, its use is limited to supervised settings. In this study, we explore the concept of incorporating virtual AT (VAT) into the attention mechanisms, by which adversarial perturbations can be computed even from unlabeled data. To realize this approach, we propose two general training techniques, namely VAT for attention mechanisms (Attention VAT) and ``interpretable'' VAT for attention mechanisms (Attention iVAT), which extend AT for attention mechanisms to a semi-supervised setting. In particular, Attention iVAT focuses on the differences in attention; thus, it can efficiently learn clearer attention and improve model interpretability, even with unlabeled data. Empirical experiments based on six public datasets revealed that our techniques provide better prediction performance than conventional AT-based as well as VAT-based techniques, and stronger agreement with evidence that is provided by humans in detecting important words in sentences. Moreover, our proposal offers these advantages without needing to add the careful selection of unlabeled data. That is, even if the model using our VAT-based technique is trained on unlabeled data from a source other than the target task, both the prediction performance and model interpretability can be improved."

# Summary. An optional shortened abstract.
summary: "Springer Applied Intelligence (**Impact Factor: 5.019** in 2021)"

tags: ["Journal", "International Publication", "Natural Language Processing", "Referred", "Springer"]
categories: ["Natural Language Processing", "Attention Mechanisms", "Virtual Adversarial Training", "Text Classification", "Question Answering", "Natural Language Inference"]
featured: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
links:
- name: Preprint
  url: https://arxiv.org/abs/2104.08763
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

| arXiv | Springer | SCImago |
|-------|----------|---------|
| {{< blogcard url="https://arxiv.org/abs/2104.08763" >}} | {{< blogcard url="https://link.springer.com/article/10.1007/s10489-022-04301-w" >}} | <a href="https://www.scimagojr.com/journalsearch.php?q=23674&amp;tip=sid&amp;exact=no" title="SCImago Journal &amp; Country Rank"><img border="0" src="https://www.scimagojr.com/journal_img.php?id=23674" alt="SCImago Journal &amp; Country Rank"  /></a> |
