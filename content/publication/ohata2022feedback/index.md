---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "Feedback is Needed for Retakes: An Explainable Poor Image Notification Framework for the Visually Impaired"
authors: ["Ohata Kazuya", "Shunsuke Kitada", "Hitoshi Iyatomi"]
date: 2022-10-18T14:09:09-04:00
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: 2022-10-18T14:09:09-04:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["1"]

# Publication name and optional abbreviated publication name.
publication: "Proc. IEEE 19th International Conference on Smart Communities: Improving Quality of Life Using ICT, IoT and AI (HONET)"
publication_short: "HONET2022"

abstract: "We propose a simple yet effective image captioning framework that can determine the quality of an image and notify the user of the reasons for any flaws in the image. Our framework first determines the quality of images and then generates captions using only those images that are determined to be of high quality. The user is notified by the flaws feature to retake if image quality is low, and this cycle is repeated until the input image is deemed to be of high quality. As a component of the framework, we trained and evaluated a low-quality image detection model that simultaneously learns difficulty in recognizing images and individual flaws, and we demonstrated that our proposal can explain the reasons for flaws with a sufficient score. We also evaluated a dataset with low-quality images removed by our framework and found improved values for all four common metrics (e.g., BLEU-4, METEOR, ROUGE-L, CIDEr), confirming an improvement in general-purpose image captioning capability. Our framework would assist the visually impaired, who have difficulty judging image quality."

# Summary. An optional shortened abstract.
summary: "Proc. IEEE 19th International Conference on Smart Communities: Improving Quality of Life Using ICT, IoT and AI (HONET)."

tags: ["International Conference", "Refereed", "Natural Language Processing", "Image Captioning", "International Publication"]
categories: ["Natural Language Processing", "Image Captioning"]
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
