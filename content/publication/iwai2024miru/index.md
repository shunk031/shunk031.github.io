---
# Documentation: https://docs.hugoblox.com/managing-content/

title: "離散拡散モデルにおけるレイアウトの“固着”を緩和する Layout-Corrector の提案"
authors: ["岩井 翔真", "長内 淳樹", "北田 俊輔", "大町 真一郎"]
author_notes: ["LINE 株式会社でのリサーチインターンの成果"]
date: 2024-08-07T00:00:00+09:00
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: 2024-08-07T00:00:00+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["article"]

# Publication name and optional abbreviated publication name.
publication: "第 27 回 画像の認識・理解シンポジウム，2024."
publication_short: "MIRU 2024"

abstract: "レイアウト生成は，カテゴリ・位置・サイズで記述される要素の集合を生成するタスクである．人間が試行錯誤を通じてレイアウトを洗練させるのに対し，現在主流の離散拡散モデル(DDM) では一度生成された要素が固着し，修正されないことを示す．この課題に対して，本研究では不調和な要素を検出するLayout-Corrector (LC) を提案する．LC はDDM の生成結果を評価し，評価値の低い要素を初期化することで要素の固着を防ぐ．実験の結果，様々なDDM に対して提案手法は一貫した性能改善を達成した．"

# Summary. An optional shortened abstract.
summary: "第 27 回 画像の認識・理解シンポジウム，2024."

tags: ["Domestic COnference", "Non-refereed", "MIRU"]
categories: ["Computer Vision", "Layout Generation"]
featured: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
links:
- name: MIRU
  url: https://miru-committee.github.io/miru2024/program/timetable/#:~:text=%E7%BF%BC%EF%BC%88%E4%B8%AD%E9%83%A8%E5%A4%A7%EF%BC%89-,OS%2D1A%2D01%3A%20%E5%B2%A9%E4%BA%95%E7%BF%94%E7%9C%9F%20(%E6%9D%B1%E5%8C%97%E5%A4%A7)%2C%20%E9%95%B7%E5%86%85%E6%B7%B3%E6%A8%B9%2C%20%E5%8C%97%E7%94%B0%E4%BF%8A%E8%BC%94%20(LINE%E3%83%A4%E3%83%95%E3%83%BC)%2C%20%E5%A4%A7%E7%94%BA%E7%9C%9F%E4%B8%80%E9%83%8E%20(%E6%9D%B1%E5%8C%97%E5%A4%A7)%2C%20%E2%80%9CLayout%2DCorrector%3A%20Alleviating%20Layout%20Sticking%20Phenomenon%20in%20Discrete%20Diffusion%20Model%E2%80%9D,-OS%2D1A%2D02

url_pdf:
url_code:
url_dataset:
url_poster: publication/iwai2024miru/poster.pdf
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
