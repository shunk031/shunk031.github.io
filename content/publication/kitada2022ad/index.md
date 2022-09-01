---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "Ad Creative Discontinuation Prediction with Multi-Modal Multi-Task Neural Survival Networks"
authors: ["Shunsuke Kitada", "Hitoshi Iyatomi", "Yoshifumi Seki"]
author_notes: ["This work was conducted during the first author's internship at Gunosy Inc."]
date: 2022-04-04T00:35:42+09:00
doi: "10.3390/app12073594"

# Schedule page publish date (NOT publication's date).
publishDate: 2022-04-01T00:00:00+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["2"]

# Publication name and optional abbreviated publication name.
publication: "Applied Sciences"
publication_short: "Appl. Sci."

abstract: "Discontinuing ad creatives at an appropriate time is one of the most important ad operations that can have a significant impact on sales. Such operational support for ineffective ads has been less explored than that for effective ads. After pre-analyzing 1,000,000 real-world ad creatives, we found that there are two types of discontinuation: short-term (i.e., cut-out) and long-term (i.e., wear-out). In this paper, we propose a practical prediction framework for the discontinuation of ad creatives with a hazard function-based loss function inspired by survival analysis. Our framework predicts the discontinuations with a multi-modal deep neural network that takes as input the ad creative (e.g., text, categorical, image, numerical features). To improve the prediction performance for the two different types of discontinuations and for the ad creatives that contribute to sales, we introduce two new techniques: (1) a two-term estimation technique with multi-task learning and (2) a click-through rate-weighting technique for the loss function. We evaluated our framework using the large-scale ad creative dataset, including 10 billion scale impressions. In terms of the concordance index (short: 0.896, long: 0.939, and overall: 0.792), our framework achieved significantly better performance than the conventional method (0.531). Additionally, we confirmed that our framework (i) demonstrated the same degree of discontinuation effect as manual operations for short-term cases, and (ii) accurately predicted the ad discontinuation order, which is important for long-running ad creatives for long-term cases."

# Summary. An optional shortened abstract.
summary: "Appl. Sci. (**Impact Factor: 2.838** in 2021)"

tags: ["Journal", "International Publication", "Computational Advertising", "Gunosy", "Referred", "Open Access", "MDPI"]
categories: ["Computational Advertising"]
featured: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
links:
- name: Preprint
  url: https://arxiv.org/abs/2204.11588
  icon_pack: ai
  icon: arxiv

url_pdf: https://www.mdpi.com/2076-3417/12/7/3594/pdf
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

{{< blogcard url="https://www.mdpi.com/2076-3417/12/7/3594" >}}
