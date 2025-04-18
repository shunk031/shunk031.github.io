---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "Majority or Minority: 固有表現抽出におけるデータの不均衡性に着目した損失関数の提案"
authors: ["根本 颯汰","北田 俊輔", "彌冨 仁"]
date: 2023-03-15T09:40:00+09:00
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: 2023-03-06T00:00:00+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["article"]

# Publication name and optional abbreviated publication name.
publication: "言語処理学会第 29 回年次大会，2023."
publication_short: "NLP 2023"

abstract: "
多くの自然言語処理タスクはデータの不均衡の問題に直面しており、実用的な応用がなされている固有表現抽出もその一つである。固有表現抽出は抽出対象の固有表現以外のトークンすべてが O クラスとなるため、O クラスが大多数を占める不均衡なデータとなっている。本論文では、固有表現抽出における不均衡性に着目した新たな損失関数 majorityor minority loss (MoM loss) を提案する。提案手法の核となるアイディアは多数派のクラスである O クラスのトークンのみを計算対象した loss を従来のモデルの損失関数に追加するものである。実験を通じて MoM loss がマルチクラス、2 クラス分類問わず、言語非依存で性能向上に寄与することを確認した。
"

# Summary. An optional shortened abstract.
summary: "言語処理学会第 29 回年次大会，2023."

tags: ["Domestic Conference", "Non-refereed", "Natural Language Processing", "ANLP"]
categories: ["Natural Language Processing", "Named Entity Recognition"]
featured: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
# links:
# - name: Follow
#   url: https://twitter.com
#   icon_pack: fab
#   icon: twitter

url_pdf: https://www.anlp.jp/proceedings/annual_meeting/2023/pdf_dir/Q6-9.pdf
url_code:
url_dataset:
url_poster: publication/nemoto2023nlp/poster.pdf
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
