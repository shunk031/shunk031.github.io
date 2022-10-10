---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "Expressions Causing Differences in Emotion Recognition in Social Networking Service Documents"
authors: ["Tsubasa Nakagawa", "Shunsuke Kitada", "Hitoshi Iyatomi"]
date: 2022-08-02T14:18:12+09:00
doi: ""
# doi: "10.1145/3511808.3557599"

# Schedule page publish date (NOT publication's date).
publishDate: 2022-08-02T14:18:12+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["1"]

# Publication name and optional abbreviated publication name.
publication: "Proc. of the 31st ACM International Conference on Information & Knowledge Management"
publication_short: "CIKM2022"

abstract: 
  It is often difficult to correctly infer a writer's emotion from text exchanged online, and differences in recognition between writers and readers can be problematic.
  In this paper, we propose a new framework for detecting sentences that create differences in emotion recognition between the writer and the reader and for detecting the kinds of expressions that cause such differences.
  The proposed framework consists of a bidirectional encoder representations from transformers (BERT)-based detector that detects sentences causing differences in emotion recognition and an analysis that acquires expressions that characteristically appear in such sentences.
  The detector, based on a Japanese SNS-document dataset with emotion labels annotated by both the writer and three readers of the social networking service (SNS) documents, detected "hidden-anger sentences" with AUC = 0.772; these sentences gave rise to differences in the recognition of anger.
  Because SNS documents contain many sentences whose meaning is extremely difficult to interpret, by analyzing the sentences detected by this detector, we obtained several expressions that appear characteristically in hidden-anger sentences.
  The detected sentences and expressions do not convey anger explicitly, and it is difficult to infer the writer's anger, but if the implicit anger is pointed out, it becomes possible to guess why the writer is angry.
  Put into practical use, this framework would likely have the ability to mitigate problems based on misunderstandings.

# Summary. An optional shortened abstract.
summary: "Proc. of the 31st ACM International Conference on Information & Knowledge Management (CIKM2022)"

tags: ["International Conference", "Refereed", "Natural Language Processing", "International Publication"]
categories: ["Natural Language Processing", "Sentiment Analysis"]
featured: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
links:
- name: Preprint
  url: http://arxiv.org/abs/2208.14244
  icon_pack: ai
  icon: arxiv

# url_pdf: https://dl.acm.org/doi/10.1145/3511808.3557599
url_code:
url_dataset:
url_poster: publication/nakagawa2022expressions/poster.pdf
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

{{< blogcard url="http://arxiv.org/abs/2208.14244" >}}
