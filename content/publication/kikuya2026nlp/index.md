---
# Documentation: https://docs.hugoblox.com/managing-content/

title: "MLP の重みを反映した Sparse Autoencoder の初期化手法の提案"
authors: ["菊谷 幹", "北田 俊輔", "原 聡"]
date: 2026-03-09T00:00:00+09:00
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: 2026-01-09T00:00:00+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["article"]

# Publication name and optional abbreviated publication name.
publication: "言語処理学会第 32 回年次大会，2026."
publication_short: "NLP 2026"

abstract: "Sparse Autoencoder (SAE) は LLM 内部の処理を解釈するためのツールとして広く用いられている。しかし、異なる初期値で訓練したSAEでは異なる``特徴''が学習されることが報告されている。この問題を解決してSAEの学習を安定化させるためには、SAEの良い初期値を設定する必要がある。本研究ではSAEの初期値としてTransformer層のMLPのデコーダを用いる手法としてSAE-MDを提案する。実験の結果、SAE-MDは既存のSAEと同等の性能を有し、学習の安定性を向上できることを確認した。"

# Summary. An optional shortened abstract.
summary: "言語処理学会第 32 回年次大会，2026."

tags:
  [
    "Domestic Conference",
    "Non-refereed",
    "Interpretability",
    "Mechanistic Interpretability",
    "ANLP",
    "ANLP2026",
  ]
categories: []
featured: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
# links:
# - name: Follow
#   url: https://twitter.com
#   icon_pack: fab
#   icon: twitter

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
  preview_only: false

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
