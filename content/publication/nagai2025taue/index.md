---
# Documentation: https://docs.hugoblox.com/managing-content/

title: "TAUE: Training-free Noise Transplant and Cultivation Diffusion Model"
authors: ["Daichi Nagai", "Ryugo Morita", "Shunsuke Kitada", "Hitoshi Iyatomi"]
date: 2025-11-04T17:50:00+09:00
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: 2025-11-04T17:50:00+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["article"]

# Publication name and optional abbreviated publication name.
publication: ""
publication_short: ""

abstract: "Despite the remarkable success of text-to-image diffusion models, their output of a single, flattened image remains a critical bottleneck for professional applications requiring layer-wise control. Existing solutions either rely on fine-tuning with large, inaccessible datasets or are training-free yet limited to generating isolated foreground elements, failing to produce a complete and coherent scene. To address this, we introduce the Training-free Noise Transplantation and Cultivation Diffusion Model (TAUE), a novel framework for zero-shot, layer-wise image generation. Our core technique, Noise Transplantation and Cultivation (NTC), extracts intermediate latent representations from both foreground and composite generation processes, transplanting them into the initial noise for subsequent layers. This ensures semantic and structural coherence across foreground, background, and composite layers, enabling consistent, multi-layered outputs without requiring fine-tuning or auxiliary datasets. Extensive experiments show that our training-free method achieves performance comparable to fine-tuned methods, enhancing layer-wise consistency while maintaining high image quality and fidelity. TAUE not only eliminates costly training and dataset requirements but also unlocks novel downstream applications, such as complex compositional editing, paving the way for more accessible and controllable generative workflows."

# Summary. An optional shortened abstract.
summary: ""

tags: ["Preprint", "Non-Refereed", "Layer-wise Image Generation", "Diffusion Model", "International Publication"]
categories: []
featured: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
links:
- name: Preprint
  url: https://arxiv.org/abs/2511.02580
  icon_pack: ai
  icon: arxiv

url_pdf:
url_code:
url_dataset:
url_poster:
url_project: https://iyatomilab.github.io/TAUE
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
