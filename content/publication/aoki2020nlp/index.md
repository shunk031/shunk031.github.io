---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "文字単位の解釈可能な潜在表現の data augmentation"
authors: ["青木 匠", "北田 俊輔", "彌冨 仁"]
date: 2020-03-18T00:00:00+09:00
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: 2020-03-18T00:00:00+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["9"]

# Publication name and optional abbreviated publication name.
publication: "言語処理学会第 26 回年次大会，2020."
publication_short: "NLP 2020"

abstract: " 深層学習ベースのモデルにおいて，日本語や中国語などのアジア圏の言語の解析は単語単位よりも文字単位での処理が効果を上げている.
しかし，過学習が起きやすいため，過学習抑制手法を適用する必要がある.
本研究では $\\beta$ -variational auto-encoder ( $\\beta $ -VAE) が各次元独立の低次元確率分布を獲得することを活用し，解釈可能な data augmentation である interpretable wildcard training (IWT) を提案する.
IWT は $\\beta$-VAE により得られた文字の低次元表現に対して， ガウス分布に従ったノイズを付加させることで，異なる文字の表現生成が可能であり，従来の wildcard training よりも解釈性が高い.
新聞記事の分類タスクによる評価実験において，IWT による解釈可能な文字表現の獲得ならびに，2% 程度の分類精度向上から，解釈性のある data augmentation の効果を確認した."

# Summary. An optional shortened abstract.
summary: "言語処理学会第 26 回年次大会，2020."

tags: ["Domestic Conference", "Non-refereed", "ANLP"]
categories: ["Natural Language Processing", "Image-based Character Embedding"]
featured: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
# links:
# - name: Follow
#   url: https://twitter.com
#   icon_pack: fab
#   icon: twitter

url_pdf: https://www.anlp.jp/proceedings/annual_meeting/2020/pdf_dir/P3-35.pdf
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
#   E.g. `slides:"example"`references`content/slides/example/index.md`.
#   Otherwise, set `slides:""`.
slides: ""
---
