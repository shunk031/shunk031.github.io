---
# Documentation: https://docs.hugoblox.com/managing-content/

title: "text-to-image 拡散モデルにおける誘導 attention map を用いた画像生成手法の提案"
authors: ["水口 徳人", "北田 俊輔", "守田 竜梧", "彌冨 仁"]
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

abstract: "拡散モデルによる画像生成技術であるLatent diffusion model(LDM)はノイズを付加させる拡散過程とノイズから画像を復元する逆拡散過程、cross attention(CA)機構により、テキストプロンプトの指示に応じた精細な画像を生成する技術として注目を集めている。 CA機構はテキストの埋め込みを潜在表現に組み込む役割を持ち、物体の要素や位置の決定に深くかかわっている。しかし複数の対象物を異なる色や位置に指定したときに、指示通りの画像が生成されない問題が存在し、現実にない組み合わせのときに顕著になる。本研究ではLDMに対する指示により忠実な画像生成のため、CAと特定の座標に物体を生成するためのattention mapを掛け合わせることで、対象物の色や位置を誘導する手法を提案する。
"

# Summary. An optional shortened abstract.
summary: "NLP 若手の会 (YANS) 第 19 回シンポジウム，2024."

tags: ["Image Generation", "Domestic Conference", "Non-refereed", "YANS"]
categories: ["Computer Vision", "Vision & Language", "Image Generation"]
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
url_poster: publication/mizuguchi2024yans/poster.pdf
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
