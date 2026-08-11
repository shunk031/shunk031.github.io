---
# Documentation: https://docs.hugoblox.com/managing-content/

title: "Activation Steeringにおける文章崩壊の抑制に向けた初期検討"
authors: ["西山 天", "川田 拓朗", "北田 俊輔", "永井 大地", "彌冨 仁"]
date: 2026-08-17T00:00:00+09:00
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: 2026-07-26T00:00:00+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["presentation"]

# Publication name and optional abbreviated publication name.
publication: "NLP 若手の会 (YANS) 第 21 回シンポジウム，2026."
publication_short: "YANS 2026"

abstract: "近年、大規模言語モデル（LLM）の出力を望ましい属性へと誘導する手法として、推論時の内部状態に直接介入するActivation Steeringが注目を集めている。既存のASで用いられるステアリングベクトルには、様々な概念が交絡していることが多く、単純なベクトル加算では目的外の内部表現まで過度に改変されてしまい、制御強度を強めると生成文の流暢性が著しく損なわれる課題がある。本研究では、無関係な特徴への干渉を最小化しつつ、トークン位置ごとの強度最適化を組み合わせることで、制御強度を高めても生成文が破綻しない新たな出力制御手法を提案する。本手法を広く利用されている一般的なローカルLLMに適用し、ステアリングの方向と強度の両面を制御することで、強い制御下でも生成文の自然さ・流暢性が維持されることを検証する。"

# Summary. An optional shortened abstract.
summary: "NLP 若手の会 (YANS) 第 21 回シンポジウム，2026."

tags:
- "Natural Language Processing"
- "LLM"
- "Interpretability"
- "Domestic Conference"
- "Non-refereed"
- "YANS"
- YANS2026
categories: ["Natural Language Processing", "Interpretability"]
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
