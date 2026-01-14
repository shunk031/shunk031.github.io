---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "CE-CLCNN: Character Encoder を用いた Character-level Convolutional Neural Networks によるテキスト分類"
authors: ["北田 俊輔", "彌冨 仁"]
date: 2018-03-15T00:00:00+09:00
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: 2018-03-15T00:00:00+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["article"]

# Publication name and optional abbreviated publication name.
publication: "言語処理学会第 24 回年次大会，2018."
publication_short: "NLP 2018"

abstract: "日本語などの単語ごとに明確な区切りがない言語の解析には，一般的に困難な形態素解析を実施した後，それらに対する適切な埋め込みが必要である．また，過学習を抑えるための data augmentation を自然言語処理に適用する場合，意味の解析を要するため通常簡単ではない．本研究ではこれらの問題を低減させ，文書分類を行える end-to-end モデルである character encoder character-levelconvolutional neural networks (CE-CLCNN) を提案する．CE-CLCNN は，解析する文の各文字を画像として扱うことで，文字の形態に着目した優れた埋め込みを実現するだけでなく，画像認識分野の data augmentation が適用可能となる．また，CNN の持つ卓越した学習能力を文書解析に活かせるため，優良な文書解析能力が実現できる．本報告では，CE-CLCNN が公開されているデータセットに対して state-of-the-art の認識精度を実現した．加えて本稿では CE-CLCNN が文書分類を行う際，解析対象のどの部分に着目しているかについても可視化を行って考察した．"

# Summary. An optional shortened abstract.
summary: "言語処理学会第 24 回年次大会，2018."

tags: ["Domestic Conference", "Non-refereed", "Natural Language Processing", "ANLP", "NLP2018"]
categories: ["Natural Language Processing", "Glyph-aware NLP", "NLP for Asian Languages"]
featured: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
# links:
# - name: Follow
#   url: https://twitter.com
#   icon_pack: fab
#   icon: twitter

url_pdf: https://anlp.jp/proceedings/annual_meeting/2018/pdf_dir/B6-5.pdf
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
