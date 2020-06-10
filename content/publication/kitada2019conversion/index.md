---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Conversion Prediction Using Multi-task Conditional Attention Networks to Support the Creation of Effective Ad Creative"
authors: ["Shunsuke Kitada", "Hitoshi Iyatomi", "Yoshifumi Seki"]
date: 2019-05-27T00:00:00+09:00
doi: "10.1145/3292500.3330789"

# Schedule page publish date (NOT publication's date).
publishDate: 2019-05-27T00:00:00+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["1"]

# Publication name and optional abbreviated publication name.
publication: "Proc. of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining. 2019."
publication_short: "KDD2019"

abstract: "Accurately predicting conversions in advertisements is generally a challenging task, because such conversions do not occur frequently. In this paper, we propose a new framework to support creating high-performing ad creatives, including the accurate prediction of ad creative text conversions before delivering to the consumer. The proposed framework includes three key ideas: multi-task learning, conditional attention, and attention highlighting. Multi-task learning is an idea for improving the prediction accuracy of conversion, which predicts clicks and conversions simultaneously, to solve the difficulty of data imbalance. Furthermore, conditional attention focuses attention of each ad creative with the consideration of its genre and target gender, thus improving conversion prediction accuracy. Attention highlighting visualizes important words and/or phrases based on conditional attention. We evaluated the proposed framework with actual delivery history data (14,000 creatives displayed more than a certain number of times from Gunosy Inc.), and confirmed that these ideas improve the prediction performance of conversions, and visualize noteworthy words according to the creatives' attributes."

# Summary. An optional shortened abstract.
summary: "Proc. of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining. 2019. (**Acceptance Rate = 20%**)"

tags: ["International Conference", "Refereed", "Computational Advertising"]
categories: ["International Conference", "Refereed", "Computational Advertising"]
featured: true

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
links:
- name: Code
  url: https://github.com/shunk031/Multi-task-Conditional-Attention-Networks
  icon_pack: fab
  icon: github

url_pdf: https://dl.acm.org/doi/10.1145/3292500.3330789
url_code:
url_dataset:
url_poster:
url_project:
url_slides:
url_source:
url_video: https://www.youtube.com/watch?v=bSVJG0R5TRk
url_preprint: https://arxiv.org/abs/1905.07289

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

{{< blogcard url="https://arxiv.org/abs/1905.07289" >}}
