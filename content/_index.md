---
# Leave the homepage title empty to use the site title
title: ''
date: 2022-10-24
type: landing

sections:
  - block: about.biography
    id: about
    content:
      title: Biography
      # Choose a user profile to display (a folder name within `content/authors/`)
      username: shunsuke-kitada

  - block: collection
    id: recent-news
    content:
      title: 📢 Recent News
      subtitle: '[All news >>](/tag/news/)'
      filters:
        folders:
          - news
        tag: 'News'
    design:
      columns: '2'
      view: community/news_list

  - block: collection
    id: journal-articles
    content:
      title: 📝 Journal Article
      subtitle: '[All Journal Articles >>](/publication/#article-journal)'
      filters:
        folders:
          - publication
        publication_type: 'article-journal'
    design:
      columns: '2'
  
  - block: collection
    id: conference-papers
    content:
      title: 📝 Conference Paper (Refereed)
      subtitle: '[All Conference Papers >>](/publication/#paper-conference)'
      filters:
        folders:
          - publication
        publication_type: 'paper-conference'
    design:
      columns: '2'

  - block: collection
    id: preprints
    content:
      title: 📝 Preprint
      subtitle: '[All Preprints >>](/tag/preprint/)'
      filters:
        folders:
          - publication
        publication_type: 'article'
        tag: 'Preprint'

    design:
      columns: '2'
  
  - block: collection
    id: dissertation
    content:
      title: 🎓 Dissertation
      filters:
        folders:
          - publication
        publication_type: 'thesis'
    design:
      columns: '2'
  
  - block: collection
    id: domestic-conferences
    content:
      title: 🇯🇵 Domestic Conference / Presentation in Japan
      subtitle: '[All domestic conference >>](/tag/domestic-conference/)'
      count: 10
      filters:
        folders:
          - publication
        tag: 'Domestic Conference'
    design:
      view: citation
      columns: '2'
    
  - block: collection
    id: talks
    content:
      title: 🎙️ Recent & Upcoming Talks
      subtitle: '[All recent and upcoming talks >>](/event)'
      filters:
        folders:
          - event
    design:
      columns: '2'

  - block: collection
    id: awards-and-grants
    content:
      title: 🏆 Awards & Grants
      filters:
        folders:
          - news
        tag: "Awards and Grants"
    design:
      columns: '2'
      view: community/news_list

  - block: collection
    id: featured-posts
    content:
      title: 📌 Featured Post
      subtitle: '[All posts >>](/post)'
      filters:
        folders:
          - post
        featured_only: true
    design:
      columns: '2'
      view: card
  
  - block: collection
    id: posts
    content:
      title: 📝 Posts & Articles
      subtitle: 'About Awards and Interviews (Almost In 🇯🇵)'
      filters:
        folders:
          - post
    design:
      columns: '2'

  - block: experience
    id: experience
    design:
      columns: '2'
    content:
      title: 👨‍💻 Selected Experiences
      subtitle: 'All experiences can be found on my [LinkedIn](https://www.linkedin.com/in/shunk031/).'
      # Date format for experience
      #   Refer to https://docs.hugoblox.com/customization/#date-format
      date_format: Jan 2006
      # Experiences.
      #   Add/remove as many `experience` items below as you like.
      #   Required fields are `title`, `company`, and `date_start`.
      #   Leave `date_end` empty if it's your current employer.
      #   Begin multi-line descriptions with YAML's `|2-` multi-line prefix.
      items:
        - title: Research Scientist
          company: LY Corporation
          company_url: 'https://www.lycorp.co.jp/en/'
        #   company_logo: org-gc
          location: Kioi Tower 1-3 Kioicho, Chiyoda-ku, Tokyo, 102-8282, Japan
          date_start: '2023-10-01'
          date_end: ''
          description: |2-
            Transferred due to merge between LINE Corp. and Yahoo! Japan Corp.

        - title: Research Scientist
          company: LINE Corporation
          company_url: 'https://linecorp.com/en/'
          location: Yotsuya Tower 23rd FL., 1-6-1 Yotsuya, Shinjuku-ku, Tokyo, 160-0004, Japan
          date_start: '2023-04-01'
          date_end: '2023-09-30'
        
        - title: Lecturer
          company: DAY1 COMPANY Inc.
          company_url: https://coloso.jp/
          location: Teheran-ro, Gangnam-gu, Seoul, Korea
          date_start: '2023-06-26'
          date_end: '2026-06-25'
          description: |2-
            - Taught lectures on image-generating AI at Coloso, an online education service
            - The lectures can be found at the following URL: https://bit.ly/KitadaXColosoJP1

        - title: Teaching Assistant / Mentor
          company: NVIDIA Japan
          company_url: 'https://www.nvidia.com/ja-jp/'
          date_start: '2016-01-01'
          date_end: '2021-04-12'
          description: |2-
            Assisted in several workshops in Tokyo relating to deep learning and CUDA:
            - [GTC Japan 2016 DLI in Hilton Tokyo Odaiba](https://nvidia.connpass.com/event/39743/)
            - [NVIDIA Deep Learning Institute 2017 in Tokyo Midtown and Takada-no-baba](https://nvidia.connpass.com/event/54780/)
            - [GTC Japan 2017 DLI in Hilton Tokyo Odaiba](https://nvidia.connpass.com/event/68912/)
            - [NVIDIA GTC 2020 DLI in Online](https://nvidia.connpass.com/event/189637/)
            - [NVIDIA GTC 2021 DLI in Online](https://nvidia.connpass.com/event/208506/)

            Served as a mentor, providing guidance on large-scale GPU distributed training using HPC:
            - [TSUBAME4.0 deep learning minicamp](https://www.t4.gsic.titech.ac.jp/minicamp-dl-202406)
            - [The 1st Large-scale Distributed Training Hackathon for Large Language Models](https://abci.ai/event/2023/06/13/ja_event.html)

        - title: Fundamental Information Technology Engineer
          company: Information-technology Promotion Agency, Japan
          company_url: 'https://www.ipa.go.jp/en/index.html'
          date_start: '2016-06-01'
          date_end: ''
          description: |2-
            Fundamental Information Technology Engineer Examination is a yardstick for measuring IT knowledge and skills as a team member by asking a range of questions about algorithm, network, database, information security, practical programming, etc.

  - block: portfolio
    id: projects
    content:
      title: 📂 Projects
      filters:
        folders:
          - project
      # Default filter index (e.g. 0 corresponds to the first `filter_button` instance below).
      default_button_index: 0
      # Filter toolbar (optional).
      # Add or remove as many filters (`filter_button` instances) as you like.
      # To show all items, set `tag` to "*".
      # To filter by a specific tag, set `tag` to an existing tag name.
      # To remove the toolbar, delete the entire `filter_button` block.
      buttons:
        - name: 'All'
          tag:  '*'
        - name: 'Official Implementation'
          tag:  'Official Implementation'
        - name: 'PyTorch'
          tag:  'PyTorch'
        - name: 'Chainer'
          tag:  'Chainer'
        - name: 'Tool'
          tag:  'Tool'
    design:
      # Choose how many columns the section has. Valid values: '1' or '2'.
      columns: '1'
      view: masonry
      # For Showcase view, flip alternate rows?
      flip_alt_rows: false

  - block: tag_cloud
    content:
      title: 📚 Popular Topics
    design:
      columns: '2'
      background:
          image:
            filename: chatgpt.webp
            filters:
              brightness: 0.2

  - block: markdown
    design:
      columns: '2'
      
    content:
      title: 🌏 Visitors
      subtitle: Powerd by [clustrmaps.com](https://clustrmaps.com/)
      text: |-
        <script type="text/javascript" id="clustrmaps" src="//clustrmaps.com/map_v2.js?d=SEDymVEFJHTaCJ9iGcuU4QJ4WF7CE1nY1E2_w9UVgm4&cl=ffffff&w=a"></script>
---
