---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "解釈性向上のための注意機構と損失勾配に対する関連損失の導入"
authors: ["北田 俊輔", "彌冨 仁"]
date: 2019-08-27T00:00:00+09:00
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: 2019-08-27T00:00:00+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["presentation"]

# Publication name and optional abbreviated publication name.
publication: "NLP 若手の会 (YANS) 第 14 回シンポジウム，2019."
publication_short: "YANS 2019"

abstract: "注意機構は自然言語処理における深層学習モデルに幅広く応用されており、予測性能の向上に大きく寄与している。また注意機構はモデルの予測時に根拠を提示する際にも利用される。こうした予測の根拠提示手法の文脈では損失計算時の勾配を元にした手法も同様に利用されており、尤もらしい予測根拠を提示していることが知られている。しかしながら注意機構と勾配の間には関連性が見られない場合が多く、予測根拠として注意機構を用いるのは疑問視されている。本研究ではモデルの解釈性の向上のために、注意機構と勾配が関連するような損失関数を新たに導入する。注意機構持つベースラインモデルに対して提案する関連損失を導入し、複数の文書分類タスクを用いて評価を行った。また注意機構と勾配の双方が関連することを確認した。"

# Summary. An optional shortened abstract.
summary: "NLP 若手の会 (YANS) 第 14 回シンポジウム，2019. ** 奨励賞 ** 受賞"

tags: ["Domestic Conference", "Non-refereed", "Award"]
categories: ["Natural Language Processing", "Interpretability", "Text Classification", "YANS"]
featured: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
links:
- name: Booster Session
  url: publication/kitada2019yans/booster-session.pdf

url_pdf:
url_code:
url_dataset:
url_poster: publication/kitada2019yans/poster.pdf
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
#   E.g. `slides:"example"`references`content/slides/example/index.md`.
#   Otherwise, set `slides:""`.
slides: ""
---
