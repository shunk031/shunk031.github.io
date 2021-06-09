---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "広告クリエイティブ評価のための深層確率埋め込みの学習"
authors: ["北田 俊輔", "彌冨 仁", "関 喜史"]
date: 2021-06-09T16:47:22+09:00
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: 2021-06-09T00:00:00+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["9"]

# Publication name and optional abbreviated publication name.
publication: "人工知能学会第 35 回全国大会，2021."
publication_short: "JSAI 2021"

abstract: "
オンライン広告における広告クリエイティブの良し悪しは、一般的にユーザーがクリエイティブをクリックし、商品が購入される等の行動が起きる割合で評価できると考えられる。一方、そのようなユーザー行動は非常にノイズが多く不確実性が高い。また広告キャンペーンや広告大賞の潜在的な魅力等に左右される。本論文では、広告クリエイティブの評価のために、確率的広告クリエイティブ埋め込みを学習し、キャンペーン内の各広告クリエイティブを潜在空間のガウス分布として表現する新たな方法を提案する。我々の確率的埋め込みは、不確実性の高いユーザーの行動やキャンペーンに関連する複数の広告クリエイティブから適切な評価を実現する特徴を捉えることが可能である。 我々は株式会社 Gunosy が提供した実際の 20 万件の広告クリエイティブを使用して評価を実施した。確率的埋め込みにより、テキストエンコーダー（LSTM、BERT など）に関係なく、広告クリエイティブの配信パフォーマンスを正確にキャプチャできることを確認した。さらに、我々の提案は最先端モデルである BERT を使用することにより、小さな不確実性で予測を実現することを確認した。
"

# Summary. An optional shortened abstract.
summary: "人工知能学会第 35 回全国大会，2021."

tags: ["Domestic Conference", "Non-refereed", "Computational Advertising"]
categories: ["Computational Advertising"]
featured: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
links:
- name: JSAI
  url: https://confit.atlas.jp/guide/event/jsai2021/subject/2D4-OS-7b-02/tables
  
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
