---
# Documentation: https://docs.hugoblox.com/managing-content/

title: "潜在拡散モデルにおける生成対象の個別配置と生成による画質改善の試み"
authors: ["永井 大地", "守田 竜梧", "北田 俊輔", "彌冨 仁"]
date: 2025-03-09T00:00:00+09:00
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: 2025-03-09T00:00:00+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["article"]

# Publication name and optional abbreviated publication name.
publication: "情報処理学第 87 回全国大会，2025."
publication_short: "IPSJ 2025"

abstract: "潜在拡散モデル（LDM）は、プロンプトから高品質な画像を生成するが、複数物体を含むプロンプトについては物体の欠落や属性の混同が課題となる。本研究では、逆拡散過程で物体の存在が確定するステップに着目した新たな枠組TAUE(Training-free trAnsplant cUltivation diffusion modEl) を提案する。TAUEでは各物体と背景を個別に生成し、苗を畑に植えるように、物体の存在が確定したノイズで背景上の対象領域を上書きすることで物体の欠落を防ぎ、配置に忠実な画像の生成を実現する。TAUEは様々なLDMの関連技術への応用が期待され、直感的な生成プロセスを提供する。"

# Summary. An optional shortened abstract.
summary: "情報処理学第 87 回全国大会，2025."

tags: ["Domestic Conference", "Non-refereed", "Image Generation", "Diffusion Model", "IPSJ"]
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
