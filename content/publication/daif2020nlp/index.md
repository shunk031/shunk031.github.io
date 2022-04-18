---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Image-based Character Embedding for Arabic Document Classification"
authors: ["Mahmoud Daif", "Shunsuke Kitada", "Hitoshi Iyatomi"]
date: 2020-03-17T00:00:00+09:00
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: 2020-03-17T00:00:00+09:00

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["9"]

# Publication name and optional abbreviated publication name.
publication: "言語処理学会第 26 回年次大会，2020."
publication_short: "NLP 2020"

abstract: "This work introduces an image-based character embdeddings model for Arabic text classification. The problem with Arabic text classification using classical techniques is its dependency on complex morphological analysis and hand crafted feature engineering. Using character-level embeddings eliminates the need for complex morphological analysis and feature engineering. We propose a new Arabic document classification model using the CE-CLCNN, where text is represented as an array of character images, and the class-balanced loss. The CE-CLCNN consists of two parts, a character autoencoder (CE) and a character-level CNN (CLCNN). The CE learns to encode image based character embeddings, and the CLCNN is then used to classify the document using those embeddings. We created two datasets to test the effectiveness of our system. The first one is the Arabic Wikipedia title dataset (AWT), and the second one is the Arabic Poetry dataset (APD). The proposed model outperforms the classical SVM by 21.23% and 13.82% for the micro and macro Fscore respectively for the ADP dataset, and by 4.02% and 3.95% for the AWT dataset. To the best of our knowledge, this is the first time an image based character embedding model was used to address the problem of Arabic text classification. Also, the first time a text classification deep learning model is tested on datasets that contain the three types of Arabic."

# Summary. An optional shortened abstract.
summary: "言語処理学会第 26 回年次大会，2020."

tags: ["Domestic Conference", "Non-refereed", "Natural Language Processing", "ANLP"]
categories: ["Natural Language Processing", "Image-based Character Embedding", "NLP for Arabic"]
featured: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
# links:
# - name: Follow
#   url: https://twitter.com
#   icon_pack: fab
#   icon: twitter

url_pdf: https://www.anlp.jp/proceedings/annual_meeting/2020/pdf_dir/P2-33.pdf
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
