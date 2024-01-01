---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "Document AI タスクに向けた大規模事前学習済みモデルを活用した Layout-aware Prompting"
authors: ["北田 俊輔", "井上 直人", "大谷 まゆ", "彌冨 仁"]
author_notes: ["株式会社 CyberAgent でのリサーチインターンの成果"]
date: 2022-08-29T00:00:00+09:00
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: 2022-08-29T00:00:00+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["presentation"]

# Publication name and optional abbreviated publication name.
publication: "NLP 若手の会 (YANS) 第 17 回シンポジウム，2022."
publication_short: "YANS 2022"

abstract: "テキストや画像を始め、イラストやグラフといったオブジェクトを含む視覚的に豊かな文書を自動的に読み取り、理解・分析を目指す document AI タスクが近年注目されている。
文書を理解する上で中心となるのが文書内のテキスト理解であり、昨今注目されている大規模事前学習済み言語モデルの prompting 技術の活用が期待できる。
視覚的に豊かな document AI タスクでは、上記理解に加えて文書中に存在するテキストのレイアウト情報が文書理解をする上で重要な役割を担っている。
本研究ではテキストのレイアウト情報を考慮した prompting 技術である、layout-aware prompting (LAP) を提案する。
LAP は広く公開されている GPT に対して、テキストのレイアウト情報を埋め込んだ layout embedding を加えるだけの非常にシンプルかつ効果的な手法である。
評価実験では、インフォグラフィックに対する視覚質問応答タスクを利用し、document AI に関する事前学習に大きく依存する既存研究と同程度の解答性能を実現した。
"

# Summary. An optional shortened abstract.
summary: "NLP 若手の会 (YANS) 第 17 回シンポジウム，2022."

tags: ["Vision & Language", "Domestic Conference", "Non-refereed", "CyberAgent", "YANS"]
categories: ["Vision & Language", "Multi-modal Model", "Document AI"]
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
