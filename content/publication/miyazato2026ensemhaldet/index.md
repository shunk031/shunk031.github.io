---
# Documentation: https://docs.hugoblox.com/managing-content/

title: "EnsemHalDet: Robust VLM Hallucination Detection via Ensemble of Internal State Detectors"
authors: ["Ryuhei Miyazato", "Shunsuke Kitada", "Kei Harada"]
date: 2026-04-03T00:00:00+09:00
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: 2026-04-03T00:00:00+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["paper-conference"]

# Publication name and optional abbreviated publication name.
publication: "Proc. of the 64th Annual Meeting of the Association for Computational Linguistics: Student Research Workshop"
publication_short: "ACL2026 SRW"

abstract: "Vision-Language Models (VLMs) excel at multimodal tasks, but they remain vulnerable to hallucinations that are factually incorrect or ungrounded in the input image. Recent work suggests that hallucination detection using internal representations is more efficient and accurate than approaches that rely solely on model outputs. However, existing internal-representation-based methods typically rely on a single representation or detector, limiting their ability to capture diverse hallucination signals. In this paper, we propose EnsemHalDet, an ensemble-based hallucination detection framework that leverages multiple internal representations of VLMs, including attention outputs and hidden states. EnsemHalDet trains independent detectors for each representation and combines them through ensemble learning. Experimental results across multiple VQA datasets and VLMs show that EnsemHalDet consistently outperforms prior methods and single-detector models in terms of AUC. These results demonstrate that ensembling diverse internal signals significantly improves robustness in multimodal hallucination detection."

# Summary. An optional shortened abstract.
summary: "Accepted to ACL SRW 2026"

tags:
- "International Conference"
- "Refereed"
- "International Publication"
- "Natural Language Processing"
- "Vision & Language"
- "Hallucination Detection"
- ACL
- ACL2026
categories:
- "Vision & Language"
- "Hallucination Detection"
- "Multimodal Large Language Models"
featured: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
links:
- name: Preprint
  url: https://arxiv.org/abs/2604.02784
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
