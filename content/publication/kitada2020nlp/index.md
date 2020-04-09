---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "解釈可能な敵対的摂動を用いた頑健な注意機構の学習"
authors: ["北田 俊輔", "彌冨 仁"]
date: 2020-03-19T00:00:00+09:00
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: 2020-03-19T00:00:00+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["9"]

# Publication name and optional abbreviated publication name.
publication: "言語処理学会第 26 回年次大会, 2020."
publication_short: "NLP 2020"

abstract: "注意機構や損失勾配は入力に対する予測の説明に使われてきたが，これらの手法は摂動に頑健ではないと示唆されている．
またこの2つの関係性の評価はこれまで順位相関が用いられてきたが，その意義にも議論の余地がある．
このように，摂動に頑健な注意機構の学習方法や，注意機構と損失勾配の関係を適切に評価する方法について課題が残されている．
本研究では摂動に頑健な注意機構の学習のために，interpretable adversarial training (iAdvT) をもとにしたAttention iAdvTの提案を行うとともに，これらの説明手法の評価基準としてピアソン相関を用いることを主張する．
4つのオープンデータセットからなる，様々なテキスト分類タスクを用いた評価実験において，Attention iAdvTがほぼすべてのタスクで最高性能を達成した．
また，注意機構と損失勾配は高く相関することを示し，すべてのタスクにおいて提案手法が一番高い相関を示すことを確認した．"

# Summary. An optional shortened abstract.
summary: "言語処理学会第 26 回年次大会, 2020."

tags: ["Domestic Conference", "Non-refereed"]
categories: ["Natural Language Processing"]
featured: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
# links:
# - name: Follow
#   url: https://twitter.com
#   icon_pack: fab
#   icon: twitter

url_pdf: https://www.anlp.jp/proceedings/annual_meeting/2020/pdf_dir/P5-29.pdf
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
#   E.g. `slides: "example"` references `content/slides/example/index.md`.
#   Otherwise, set `slides: ""`.
slides: ""
---
