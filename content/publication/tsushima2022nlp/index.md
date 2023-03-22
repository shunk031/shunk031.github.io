---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "ViT-CLT: パッチ分割した文字画像から偏旁冠脚を考慮した文書分類"
authors: ["津嶋 祐介", "青木 匠", "北田 俊輔", "彌冨 仁"]
date: 2022-03-17T10:40:00+09:00
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: 2022-03-17T10:40:00+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["9"]

# Publication name and optional abbreviated publication name.
publication: "言語処理学会第 28 回年次大会，2022."
publication_short: "NLP 2022"

abstract: "日本語や中国語における自然言語処理では，漢字の部首を考慮した文字単位による自然言語処理が文書解析能力の向上に寄与している．文字形状を考慮するために，従来は convolutional neural network (CNN) を元にした文字符号化器および文書分類器の end-to-end モデルが多く提案されている．本研究では，漢字の偏や旁といった構成要素の関係性を考慮した高性能な文書分類を実現するために，文字符号化器に Vision Transformer (ViT)，文書分類器に character-level Transformer (CLT) で構成された ViT-CLT を提案する．我々の ViT-CLT は漢字の構成要素とその関係性を捉えるために ViT を用いて文字画像から文字の埋め込みを獲得し，文書分類器ではその文字埋め込みを使用して文書分類タスクを解けるよう学習を行う．評価実験では日本語のニュース記事を用いたカテゴリ分類タスクにおいて，CNN を用いた従来の文字符号化器・文書分類器モデルと比較し，ViT-CLT が 18% の予測性能の向上を確認した．更に ViT-CLT の文字符号化器における attention の可視化結果から，従来モデルよりも漢字の構成要素を十分に考慮できていることを確認した．
"

# Summary. An optional shortened abstract.
summary: "言語処理学会第 28 回年次大会，2022."

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

url_pdf: https://www.anlp.jp/proceedings/annual_meeting/2022/pdf_dir/PH4-13.pdf
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
