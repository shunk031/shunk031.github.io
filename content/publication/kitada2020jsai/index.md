---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "生存時間分析を用いた広告クリエイティブの停止予測"
authors: ["北田 俊輔", "彌冨 仁", "関 喜史"]
date: 2020-06-17T14:06:57+09:00
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: 2020-06-09T00:00:00+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["9"]

# Publication name and optional abbreviated publication name.
publication: "人工知能学会第 34 回全国大会，2020."
publication_short: "JSAI 2020"

abstract: '
本研究では，広告クリエイティブの停止予測に対して生存時間予測を利用した枠組みを提案する．広告クリエイティブの停止は配信効果の高いクリエイティブを選択するために重要なプロセスであるが支援する研究は未だ少ない．そこで深層学習を元にした広告クリエイティブを構成するさまざまな特徴量を考慮した生存時間予測の枠組みを提案する．この枠組みは "売上を元にした損失項の導入" と，"長期と短期をそれぞれを分割する 2 期間推定法の導入" という 2 つの大変効果の高い技術から構成される．提案する枠組みは株式会社 Gunosy から提供された 1,000,000 件の実世界における広告クリエイティブデータセットを用いて評価した．提案するマルチモーダルな DNN を元にした枠組みは従来手法よりも高い予測精度を実現した．2 期間推定法では短期モデルおよび長期モデル共に 20pt 程度の大幅な予測精度の改善を確認した．売上を元にした損失項を導入することで，さらに 3pt 程度の予測精度の向上を確認した．
'

# Summary. An optional shortened abstract.
summary: "人工知能学会第 34 回年次大会，2020."

tags: ["Domestic Conference", "Non-refereed", "Computational Advertising"]
categories: ["Computational Advertising"]
featured: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
links:
- name: JSAI
  url: https://confit.atlas.jp/guide/event/jsai2020/subject/1H3-OS-12a-02/tables

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
#   E.g. `slides:"example"`references`content/slides/example/index.md`.
#   Otherwise, set `slides:""`.
slides: ""
---
