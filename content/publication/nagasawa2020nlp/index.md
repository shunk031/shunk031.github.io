---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Script-aware embedding を用いた文字表現の獲得"
authors: ["長澤 駿太", "北田 俊輔", "彌冨 仁"]
date: 2020-03-17T00:00:00+09:00
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: 2020-03-17T00:00:00+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["article"]

# Publication name and optional abbreviated publication name.
publication: "言語処理学会第 26 回年次大会，2020."
publication_short: "NLP 2020"

abstract: " 日本語の漢字や中国語などはそれぞれの文字が表意性を持つため，この性質を捉えることはこれら言語の意味理解において重要な手かがりとなる．
文字を画像として扱い CNN 等を用いて，形状情報を低次元ベクトルに埋め込むモデルは，こうした特徴を捉えることで文書分類タスクにおいて成果を上げている．
しかしながら日本語では平仮名や片仮名等の表音文字が多く使われる文書に対しては適切な文字表現を得ることが難しい．
本研究では文字形状を学習した visual feature と文脈情報を学習した context feature の２つの文字表現手法を用いることで，表意文字および表音文字を考慮した文字表現の学習手法である script-aware embedding を提案する．
本報告では文書分類のタスクにおいて，提案手法の評価を行った．"

# Summary. An optional shortened abstract.
summary: "言語処理学会第 26 回年次大会，2020."

tags: ["Domestic Conference", "Non-refereed", "Natural Language Processing", "ANLP"]
categories: ["Natural Language Processing", "Glyph-aware NLP", "NLP for Asian Languages"]
featured: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
# links:
# - name: Follow
#   url: https://twitter.com
#   icon_pack: fab
#   icon: twitter

url_pdf: https://www.anlp.jp/proceedings/annual_meeting/2020/pdf_dir/P1-14.pdf
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
#   E.g. `slides:"example"`references`content/slides/example/index.md`.
#   Otherwise, set `slides:""`.
slides: ""
---
