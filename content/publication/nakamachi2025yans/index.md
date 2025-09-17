---
# Documentation: https://docs.hugoblox.com/managing-content/

title: "日本語の広告画像向けタイポグラフィ属性の生成型解析：小規模 VLM の LoRA 微調整による検証"
authors: ["中町 礼文", "浦宗 龍生", "吉橋 亮太", "和田 有輝也", "北田 俊輔", "牧田 光晴"]
date: 2025-09-19T11:40:00+09:00
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: 2025-09-16T00:00:00+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["presentation"]

# Publication name and optional abbreviated publication name.
publication: "NLP 若手の会 (YANS) 第 20 回シンポジウム，2025."
publication_short: "YANS 2025"

abstract: "本研究では、日本語のバナー広告画像におけるタイポグラフィ属性解析を生成形式で定式化し、小規模 VLM の LoRA チューニングによるタイポグラフィ属性解析の性能を検証する。広告バナー風のテキストや広告の設定、それらに基づく装飾パラメタなどの擬似データを LLM で生成し、擬似データから日本語テキスト画像を合成することで学習データを作成した。合成画像を入力としてフォント種・太さ・揃え・配色・字間・行間などのタイポグラフィ属性を構造化テキストとして生成するタスクを提案した。QwenVL2.5、Phi-4-Multimodal、Gemma3 といった 7B 以下の小規模 VLM に対し、合成データで LoRA チューニングを行い、日本語広告特有のタイポグラフィ表現に対する小規模 VLM の生成出力の傾向を調査した。"

# Summary. An optional shortened abstract.
summary: "NLP 若手の会 (YANS) 第 20 回シンポジウム，2025."

tags: ["Computational Advertising", "Typography Analysis", "Domestic Conference", "Non-refereed", "YANS"]
categories: ["Vision & Language", "Computational Advertising"]
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
url_poster: publication/nakamachi2025yans/poster.pdf
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
