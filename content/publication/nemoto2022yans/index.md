---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "固有表現認識タスクにおけるデータセットの偏りに着目した動的重み付け損失関数の提案"
authors: ["根本 颯汰","北田 俊輔", "彌冨 仁"]
date: 2022-08-30T00:00:00+09:00
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: 2022-08-30T10:10:53+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["0"]

# Publication name and optional abbreviated publication name.
publication: "NLP 若手の会 (YANS) 第 17 回シンポジウム，2022."
publication_short: "YANS 2022"

abstract: "固有表現認識（Named Entity Recognition; NER）は自然言語で記述されたテキスト中から人名や地名、日付などの固有表現を取り出す、情報抽出タスクの一つである。本タスクを各語に対する分類問題とみなしたとき、分類すべきクラスの数は多い反面、大部分の語が「その他」に分類される、非常に不均衡なデータを元にしたタスクである。このようなデータを機械学習モデルでそのまま学習すると、本来識別が必要なサンプル数の少ないクラスの認識精度は非常に低くなってしまう。本研究では、NER タスクにおけるデータセットの不均衡性に着目した、新たな損失関数を導入する学習手法を提案する。我々の提案する損失関数は、大部分を占めるその他クラスと少数のそれ以外のクラスを区別できるように学習しつつ、少数のクラスにおいても粒度の細かい区別ができるように訓練する。複数の日本語 NER データセットを用いて提案手法の有効性を確認した。
"

# Summary. An optional shortened abstract.
summary: "NLP 若手の会 (YANS) 第 17 回シンポジウム，2022."

tags: ["Named Entity Recognition", "Domestic Conference", "Non-refereed", "YANS"]
categories: ["Natural Language Processing", "Imbalanced Dataset", "Named Entity Recognition"]
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
