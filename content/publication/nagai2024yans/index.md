---
# Documentation: https://docs.hugoblox.com/managing-content/

title: "潜在拡散モデルにおけるプロンプトを用いた配色制御の試み"
authors: ["永井 大地", "根本 颯汰", "北田 俊輔", "彌冨 仁"]
date: 2024-09-05T17:50:00+09:00
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: 2024-09-01T00:00:00+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["presentation"]

# Publication name and optional abbreviated publication name.
publication: "NLP 若手の会 (YANS) 第 19 回シンポジウム，2024."
publication_short: "YANS 2024"

abstract: "潜在拡散モデル（LDM）はユーザーが指定したプロンプトテキストに応じた高品質な画像生成を可能にする。しかし、プロンプトで指定した描画対象とその色や材質などの属性の組み合わせが非現実的な場合、プロンプトに不忠実な画像が生成される問題がある。我々は、逆拡散過程において色、形の順に生成されると仮定し、配色制御用のプロンプトによるガイダンスを行うことで問題解決を目指す。具体的には、初めに目標の色を持つが対象ではない物体をプロンプトとして生成を開始し、ある程度デノイズが進んだ段階でプロンプトを目標の対象に変更する。これにより物体間での色の引継ぎを行う。本稿では拡散モデルの配色原理について議論し、最先端のLDMのStable Diffusion 3 モデルでも適切な画像生成が困難なプロンプトに対し、適切に色を反映できたことを報告する。"

# Summary. An optional shortened abstract.
summary: "NLP 若手の会 (YANS) 第 19 回シンポジウム，2024."

tags: ["Image Generation", "Diffusion Model", "Domestic Conference", "Non-refereed", "YANS"]
categories: ["Computer Vision", "Image Generation"]
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
url_poster: publication/nagai2024yans/poster.pdf
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
