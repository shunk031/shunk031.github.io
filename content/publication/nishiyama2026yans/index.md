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
- "Posters"
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
url_poster: publication/nishiyama2026yans/poster.pdf
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

本発表は、YANS 2026のスポンサー賞の選考候補となりました。以下は、フューチャー株式会社の参加報告からの引用です。

> [S2-P30] Activation Steeringにおける文章崩壊の抑制に向けた初期検討
>
> 西山 天、川田 拓朗、北田 俊輔、永井 大地、彌冨 仁（法政大学）
>
> この研究では、LLMの内部状態にベクトルを足し込んで出力を制御するActivation Steeringについて、生成される文章の崩壊を抑える手法を検討しています。
>
> 従来手法は1トークンを出力するたびに同じ強さでベクトルを足すため、目的の概念以外の表現にまで影響が及んでしまったり、介入が不要な箇所にまで作用し、無用な反復や意味の破綻した文章を招いてしまいます。この研究では、介入する位置と強度をトークンごとに決める機構と、元の内部状態を極力保ったまま、目的の概念へ変換する機構を組み合わせた手法を提案しており、2つの機構の適用順を誤ると出力が崩壊することも報告されていました。介入の「どこに・どれだけ」と「どう」を分けて整理した枠組みが明快で、参考になる発表だと感じました。

詳細は、[フューチャー株式会社の参加報告](https://future-architect.github.io/articles/20260916a/#S2-P30-Activation-Steering%E3%81%AB%E3%81%8A%E3%81%91%E3%82%8B%E6%96%87%E7%AB%A0%E5%B4%A9%E5%A3%8A%E3%81%AE%E6%8A%91%E5%88%B6%E3%81%AB%E5%90%91%E3%81%91%E3%81%9F%E5%88%9D%E6%9C%9F%E6%A4%9C%E8%A8%8E:~:text=%5BS2%2DP30%5D%20Activation,%E6%84%9F%E3%81%98%E3%81%BE%E3%81%97%E3%81%9F%E3%80%82)をご覧ください。
