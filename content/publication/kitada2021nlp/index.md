---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "半教師あり文書分類のための仮想敵対的学習による注意機構の頑健性および解釈性の向上"
authors: ["北田 俊輔", "彌冨 仁"]
date: 2021-01-15T17:28:40+09:00
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: 2021-03-15T00:00:00+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["article"]

# Publication name and optional abbreviated publication name.
publication: "言語処理学会第 27 回年次大会，2021."
publication_short: "NLP 2021"

abstract: " 本研究では、仮想敵対的学習 (virtual adversarial training: VAT) に基づいた中期項に対する新しい学習手法を提案する。 これまでの研究で摂動に対して脆弱であると報告されている注意機構に対して、VAT は半教師ありの設定で、教師なしデータから敵対的摂動を計算することが可能である。 提案法に対する実証実験の結果、 (1) 従来の敵対的摂動に基づく手法だけでなく、最新の VAT に基づく手法と比較して、半教師あり設定で有意に優れた予測性能が得られること、(2) 学習された注意の重みが購買を元にした単語の重要度との相関がより強く、人手による予測根拠とより良い一致を示すこと、さらに (3) 教師なしデータの増加に伴って性能が向上することを示した。 "

# Summary. An optional shortened abstract.
summary: "言語処理学会第 27 回年次大会，2021."

tags:
- "Domestic Conference"
- "Non-refereed"
- "Natural Language Processing"
- "ANLP"
- "NLP2021"
- ANLP2021
categories: ["Natural Language Processing", "Virtual Adversarial Training"]
featured: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
# links:
# - name: Follow
#   url: https://twitter.com
#   icon_pack: fab
#   icon: twitter

url_pdf: https://www.anlp.jp/proceedings/annual_meeting/2021/pdf_dir/P6-14.pdf
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

本発表は、NLP2021のスポンサー賞の一次選考候補に挙がりました。以下は、デンソーアイティーラボラトリの選考報告からの引用です。

> P6-14 半教師あり文書分類のための仮想敵対的学習による注意機構の頑健性および解釈性の向上: 北田俊輔, 彌冨仁 (法政大)

詳細は、[デンソーアイティーラボラトリの選考報告](https://d-itlab.co.jp/blog/20210326/#:~:text=P6%2D14%20%E5%8D%8A%E6%95%99%E5%B8%AB%E3%81%82%E3%82%8A%E6%96%87%E6%9B%B8%E5%88%86%E9%A1%9E%E3%81%AE%E3%81%9F%E3%82%81%E3%81%AE%E4%BB%AE%E6%83%B3%E6%95%B5%E5%AF%BE%E7%9A%84%E5%AD%A6%E7%BF%92%E3%81%AB%E3%82%88%E3%82%8B%E6%B3%A8%E6%84%8F%E6%A9%9F%E6%A7%8B%E3%81%AE%E9%A0%91%E5%81%A5%E6%80%A7%E3%81%8A%E3%82%88%E3%81%B3%E8%A7%A3%E9%87%88%E6%80%A7%E3%81%AE%E5%90%91%E4%B8%8A%3A%20%E5%8C%97%E7%94%B0%E4%BF%8A%E8%BC%94%2C%20%E5%BD%8C%E5%86%A8%E4%BB%81%20(%E6%B3%95%E6%94%BF%E5%A4%A7))をご覧ください。
