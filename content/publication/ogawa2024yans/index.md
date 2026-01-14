---
# Documentation: https://docs.hugoblox.com/managing-content/

title: "大規模言語モデルを用いたオノマトペ付与による日本語音声データセットの拡張"
authors: ["小川 剛毅", "根本 颯汰", "北田 俊輔", "彌冨 仁"]
date: 2024-09-05T17:50:00+09:00
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: 2024-09-01T00:00:00+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["presentation"]

# Publication name and optional abbreviated publication name.
publication: "NLP 若手の会 (YANS) 第 19 回シンポジウム，2024."
publication_short: "YANS 2024"

abstract: "現在、大規模言語モデル(LLM)を活用した音声認識合成技術が注目を集めている。日本語を対象とした研究も行われているが、モデル構築のための学習データ不足などの理由から、英語に比べると精度が低い。このため翻訳を介した手法が検討されているが、日本語特有の表現など課題があり精度向上の余地が残されている。本研究では日本語の特徴に着目し日本語データセットの作成方法を提案する。具体的にはLLMを用いて既存の日本語データセットのテキストに日本語表現として適切なオノマトペを付与する。我々はこの作成したデータセットを用いてキャプションから環境音を検索するtext-to-audioにおけるretrievalタスクで評価を行い、我々のデータセットと英語のデータセットを用いたモデルの性能を比較した"

# Summary. An optional shortened abstract.
summary: "NLP 若手の会 (YANS) 第 19 回シンポジウム，2024."

tags: ["Text-to-Audio Retrieval", "LLM", "ChatGPT", "Domestic Conference", "Non-refereed", "YANS", "YANS2024"]
categories: ["Natural Language Processing", "Audio Processing"]
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
url_poster: publication/ogawa2024yans/poster.pdf
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
