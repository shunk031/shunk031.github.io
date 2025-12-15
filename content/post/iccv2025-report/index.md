---
# Documentation: https://docs.hugoblox.com/managing-content/

title: "ICCV2025 Conference Participation Report"
subtitle: ""
summary: "At ICCV 2025, our team from LY Corp. successfully organised and participated in a workshop and paper presentation, gaining deep insights into the shift of computer‐vision research toward structured, controllable design generation and fast, reliable foundation-model technologies."
authors: ["Shunsuke Kitada"]
tags: ["ICCV2025", "Conference Report", "Computer Vision", "Design Generation", "Foundation Models"]
categories: ["Tech Blog", "Conference Report"]
date: 2025-11-25T00:00:00Z
lastmod: 2025-11-25T00:00:00Z
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: false

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["internal-project"]` references `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
projects: []
---

# Our Paper and Workshop Accepted at ICCV 2025, the Top International Conference on Computer Vision (Participation Report)

Hello, I’m [Shunsuke Kitada](https://shunk031.me/) ([@shunk031](https://x.com/shunk031)), and I work at LY Corporation on research and development for image generation and design generation.  
From October 19 to 23, 2025, I attended and presented at the [International Conference on Computer Vision, ICCV 2025](https://iccv.thecvf.com/Conferences/2025), held in Hawaii, USA.

In this article, I’ll share insights gained from ICCV workshops and the main conference. First, I’ll report on the workshop we organized, where I and other LY employees led international discussions, and introduce the insights gained from a workshop specialized in advertising and design generation. Then, I’ll analyze the latest trends at the main conference—such as acceleration and controllability of diffusion models, and hierarchical / structured design generation—alongside an overview of our own research team’s presentation.

{{< figure src="iccv2025_aloha.jpg" alt="Entrance of the venue" caption="Entrance of the venue" >}}

This article is an English translation of the following Japanese article:
{{< blogcard url="https://techblog.lycorp.co.jp/ja/20251125b" >}}

## Report on the FOUND Workshop

### Workshop Overview and Activities as Organizers

Our workshop, titled [Foundation Data for Vision: Challenges and Opportunities (FOUND)](https://iccv2025-found-workshop.limitlab.xyz/), was organized by LY employees including myself (Kitada) and [Dr. Komatsu](https://scholar.google.com/citations?user=o2lMlxMAAAAJ), and was accepted at ICCV 2025.

{{< figure src="iccv2025_found-workshop_accepted.png" alt="Our company’s news page about the workshop acceptance" caption="Our company’s news page about the workshop acceptance" link="https://research.lycorp.co.jp/jp/news/329" >}}

{{< figure src="iccv2025_found-workshop.png" alt="FOUND workshop homepage" caption="FOUND workshop homepage" link="https://iccv2025-found-workshop.limitlab.xyz/" >}}

The theme centers on “data,” which is indispensable for recent advances in foundation models, and the workshop aimed to provide an international forum to discuss the challenges and opportunities around it.

This acceptance represents one of the rare cases where a workshop at ICCV, one of the world’s top-tier conferences, is led by Japanese researchers. It demonstrates that research and industrial efforts originating in Japan are being recognized on a global stage.

### LY’s Contribution and On-Site Highlights

LY Corporation took the lead in organizing this workshop. Through this, we were able to demonstrate, at least to some extent, that we are in a position to drive international discussions on *foundation data*, an urgent topic that will shape the future of the computer vision field.

{{< figure src="iccv2025_found-workshop_opening.jpg" alt="FOUND workshop opening." caption="FOUND workshop opening. Opening session by lead organizer [Yoshihiro Fukuhara](https://gatheluck.net/home/)." >}}

{{< figure src="iccv2025_found-workshop_sponsors.jpg" alt="FOUND workshop sponsors." caption="FOUND workshop sponsors. LY Corporation (LINEヤフー) was also listed as a sponsor." >}}

The workshop attracted many researchers and practitioners from both academia and industry, leading to lively technical exchanges. In particular, the joint social event we held together with the [LIMIT Workshop](https://iccv2025-limit-workshop.limitlab.xyz/), also at ICCV 2025, was extremely successful. It served as a valuable opportunity to foster deeper networking among participants and to expand the possibilities for future international collaborations.

{{< figure src="iccv2025_limit-found-workshop_banquet.jpg" alt="LIMIT & FOUND workshop banquet" caption="LIMIT & FOUND workshop banquet. . Researchers from Google, OpenAI, Salesforce Research, who gave invited talks at the workshops, as well as many members from universities and research institutions joined us." >}}

Based on this experience as organizers, if you are considering hosting a workshop at an international conference, or if you feel uncertain about how to write a proposal or how to manage operations, please feel free to reach out. In particular, [Mr. Fukuhara](https://gatheluck.net/home/), who served as the lead organizer, and [Dr. Kataoka](https://hirokatsukataoka.net/) from AIST, who led the co-hosted LIMIT Workshop, both have extensive experience and can provide concrete advice. I ([Kitada](https://shunk031.me)) would also be happy to support where I can. I sincerely hope that more researchers and engineers from Japan will take the lead in discussions at international conferences.

## Insights from Attended Workshops

From the perspective of my domain of responsibility and expertise—image generation, design generation, and business impact (especially in advertising and marketing), I attended and will report on two workshops.

### Report on “Computer Vision in Advertising and Marketing (CVAM)”

The [CVAM Workshop](https://cvam-workshop.github.io/) focused on the latest applications of computer vision (CV) in the fields of digital advertising and marketing.

{{< figure src="iccv2025_cvam-workshop.png" alt="CVAM workshop page" caption="CVAM workshop page" link="https://cvam-workshop.github.io/" >}}

From a business impact standpoint, the workshop’s theme, applications of CV technologies in advertising and marketing, specifically covered creative generation, optimization of marketing systems, brand intelligence, and more.

In our business, which aims to maximize advertising effectiveness, understanding and generating visual content is an urgent challenge. By participating in CVAM, I was able to reconfirm the importance of discussions on how to connect the latest image generation technologies not only to creative production, but also to ad effectiveness measurement and prediction of consumer behavior.

### Report on “Workshop on Graphic Design Understanding and Generation 2025 (GDUG)”

The [GDUG Workshop](https://sites.google.com/view/gdug-workshop) aimed to discuss key concepts, technical constraints, and ethical aspects in the recognition and generation of graphic design and documents.

{{< figure src="iccv2025_gdug-workshop.png" alt="GDUG workshop page" caption="GDUG workshop page" link="https://sites.google.com/view/gdug-workshop" >}}

From the perspective of design generation, a shared concern was that, while many research efforts focus on pixel-based image generation, real-world design workflows—such as creating posters, online ads, and websites—are based on structured documents (e.g., layered object representations, style attributes, typography) rather than raw pixels. This gap between research and practice was repeatedly highlighted.

In the invited talks, cutting-edge methods for layer decomposition were introduced, where existing designs are decomposed into native layers such as text, foreground elements, and background (e.g., the [Accordion pipeline](https://arxiv.org/abs/2507.05601)).  
This clearly showed that design generation is evolving from simply producing a “flat, single-layer output” toward handling layered structures similar to those used in real-world design processes. It also provided important hints for rethinking the direction of our own design generation technology development.

## Main Conference Report and Key Trend Analysis

### Overall Statistics and Scale of ICCV 2025

ICCV 2025 was held at the [Hawaii Convention Center](https://jp.hawaiiconvention.com/), with nearly 7,000 participants. Over 11,000 papers were submitted, of which around 2,600 were accepted (an acceptance rate of about 24%).

The top three research trends were: generative AI (images and videos), 3D processing from multi-view / multi-sensor data, and multimodal learning. In particular, in the generative model area, I felt that a major trend is the shift from *diffusion* models to *flow* models.  
For a more detailed overview and analysis of trends, I recommend the [ICCV 2025 Report](https://hirokatsukataoka.net/temp/presen/251031ICCV2025Report_FinalizedVer.pdf) compiled by volunteers from [cvpaper.challenge](https://xpaperchallenge.org/cv/).

{{< figure src="iccv2025_hawaiiconvention.jpg" alt="ICCV 2025 venue guide posted inside the Hawaii Convention Center" caption="ICCV 2025 venue guide posted inside the Hawaii Convention Center" >}}

### Introduction of Our Research Team’s Presentation “PINO”

Our research presentation [PINO (Person-Interaction Noise Optimization)](https://arxiv.org/abs/2507.19292) is a technique that enables long-duration, customizable, arbitrary-size group motion generation.
This research is the result of our summer internship program, led primarily by [Mr. Ota](https://sinc865.github.io/) from Tokyo Institute of Technology.

{{< figure src="iccv2025_pino.jpg" alt="PINO poster session" caption="Our research scientists [Dr. Yu](https://yu1ut.com/) (left) and [Dr. Fujiwara](https://kfworks.com/) (right) presenting the poster. Yu was also selected as an Outstanding Reviewer for the main conference." >}}

In terms of the overview and contributions of PINO, the method employs a unique approach that optimizes the noise input when denoising motion sequences using a base diffusion model (e.g., [InterGen](https://arxiv.org/abs/2304.05684)).

{{< figure src="https://arxiv.org/html/2507.19292v1/x1.png" alt="PINO 1" caption="Figure from PINO [Ota+ ICCV’25]" >}}

By this optimization, the generated motions are not only aligned with the text prompts, but also enforced to be physically plausible through cost terms that reduce physical artifacts such as body intersections and penetrations.

{{< figure src="https://arxiv.org/html/2507.19292v1/x2.png" alt="PINO 2" caption="Figure from PINO [Ota+ ICCV’25]" >}}

Furthermore, users can control root positions, regions, and directions via penalty terms, enabling customizable motion generation.

### Notable Technical Trends in Image & Design Generation

From the standpoint of my work in image and design generation, I’ll analyze the key trends observed at the main conference, including their potential for business impact.

#### Efficiency and Reliability of Diffusion Models: The Superiority of Flow Models

The evolution of diffusion models (DMs) is shifting focus from mere realism to speed, controllability, and reliability.

Regarding flow-based generation and fast sampling, Flow Matching models are gaining prominence as a training paradigm for generative models. In particular, [Contrastive Flow Matching](https://arxiv.org/abs/2506.05350) maximizes the dissimilarity between the estimated flow and an independently sampled flow, thereby consistently outperforming previous Flow Matching methods (better FID scores) and enabling high-quality, fast generation.

{{< figure src="https://arxiv.org/html/2506.05350v1/extracted/6514412/figures/imgs/flows.png" alt="Figure from [Stoica+ ICCV’25]" caption="Figure from Contrastive Flow Matching [Stoica+ ICCV’25]" >}}

For inversion-free editing, [FlowEdit](https://arxiv.org/abs/2412.08629) utilizes pretrained flow models (SD3, FLUX.1, etc.) and removes the need for an “inversion” step during editing, instead tracing a shorter, more direct path from the source image distribution to the target distribution. This achieves high text alignment and strong structural preservation (excellent LPIPS), and FlowEdit received the Best Student Paper Award.

{{< figure src="https://arxiv.org/html/2412.08629v2/x2.png" alt="Figure from FlowEdit [Kulikov+ ICCV’25]" caption="Figure from FlowEdit [Kulikov+ ICCV’25]" >}}

In controllable generation ([FlowChef](https://arxiv.org/abs/2412.00100)), Rectified Flow Models (RFMs) are leveraged, where sampling trajectories become nearly straight and the nonlinear error term approaches zero. By skipping gradient computation (Gradient Skipping), FlowChef achieves deterministic and efficient controllable generation for tasks such as inpainting and super-resolution—without additional training or large-scale backpropagation.

{{< figure src="https://arxiv.org/html/2412.00100v1/x2.png" alt="Figure from FlowChef [Patel+ ICCV’25]" caption="Figure from FlowChef [Patel+ ICCV’25]" >}}

#### Evaluating and Improving Generation Quality (Human-Centered Approaches)

As a method for optimizing image generation based on human preferences, an evaluation model (HPSv3) was proposed and built using a large and diverse dataset ([HPDv3](https://arxiv.org/abs/2508.03789): 1.08 million text–image pairs) combined with an uncertainty-aware ranking loss. This enables Model-wise Preference (selecting the optimal model for a given prompt) and Sample-wise Preference (selecting the best sample among multiple generations).

{{< figure src="https://arxiv.org/html/2508.03789v2/x1.png" alt="Figure from HPSv3 [Ma+ ICCV’25]" caption="Figure from HPSv3 [Ma+ ICCV’25]" >}}

The self-reflection–driven iterative improvement approach ([Reflection Tuning](https://arxiv.org/abs/2504.16080)) proposes a paradigm in which a reward model or multimodal LLM (MLLM) generates “reflection” prompts that describe the shortcomings of a generated image in text, and the image is then iteratively improved according to these instructions. This allows targeted corrections such as “remove the sunlight” or “change the clothes.”

{{< figure src="https://arxiv.org/html/2504.16080v1/x1.png" alt="Figure from Reflection Tuning [Zhou+ ICCV’25]" caption="Figure from Reflection Tuning [Zhou+ ICCV’25]" >}}

#### Structured Generation to Accelerate Design and Advertising Applications

For layer-based structured generation, [DreamLayer](https://arxiv.org/abs/2503.12838) addresses the long-standing challenge of “layer consistency” in design generation by generating multiple transparent image layers simultaneously in a coherent manner. It uses mechanisms such as Layer-Shared Self-Attention to resolve inconsistencies in occlusion relationships and spatial layout between foreground and background.

{{< figure src="https://arxiv.org/html/2503.12838v1/x1.png" alt="Figure from DreamLayer [Huang+ ICCV’25]" caption="Figure from DreamLayer [Huang+ ICCV’25]" >}}

Regarding advances in layout control, [CreatiLayout](https://arxiv.org/abs/2412.03859) (SiamLayout) is a Transformer-based model that generates images from layout (placement information) and demonstrates high performance in spatial consistency, color, shape, and more. Its LayoutDesigner component achieves state-of-the-art accuracy in layout planning tasks, surpassing GPT-4 Turbo.

{{< figure src="https://arxiv.org/html/2412.03859v3/x2.png" alt="Figure from CreatiLayout [Zhang+ ICCV’25]" caption="Figure from CreatiLayout [Zhang+ ICCV’25]" >}}

For high-fidelity image compositing, [DreamFuse](https://arxiv.org/abs/2504.08291) proposes a new method called Localized DPO (Localized Direct Preference Optimization) to better fuse foreground and background images in a way that humans prefer. By learning to avoid trivial “copy-and-paste” images (negative samples), the model more appropriately handles fusion-related transformations—such as perspective and affine transformations—leading to improved background consistency and harmony with the foreground.

{{< figure src="https://arxiv.org/html/2504.08291v1/x1.png" alt="Figure from DreamFuse [Huang+ ICCV’25]" caption="Figure from DreamFuse [Huang+ ICCV’25]" >}}

For accurate visual text synthesis, [UniGlyph](https://arxiv.org/abs/2507.00992) uses segmentation masks at the pixel level as conditions in a diffusion-based framework, addressing problems such as blurry glyphs and style inconsistencies. It shows strong performance especially for rendering small text and complex layouts.

{{< figure src="https://arxiv.org/html/2507.00992v2/x1.png" alt="Figure from UniGlyph [Wang+ ICCV’25]" caption="Figure from UniGlyph [Wang+ ICCV’25]" >}}

[TextMaster](https://arxiv.org/abs/2410.09879) is a unified framework that controls both text glyphs and styles. By integrating OCR techniques to compute L2 losses on character features, it enables realistic text editing.

{{< figure src="https://arxiv.org/html/2410.09879v2/x3.png" alt="Figure from TextMaster [Yan+ ICCV’25]" caption="Figure from TextMaster [Yan+ ICCV’25]" >}}

For deployment in advertising and marketing, the gaze prediction method [ScanDiff](https://arxiv.org/abs/2507.23021) proposes using diffusion models to predict scanpaths (gaze trajectories) in response to visual stimuli such as ads. It achieves high performance on datasets like COCO-Search18. This is an important technology for modeling human attention, crucial to optimizing the visibility and effectiveness of ad creatives.

{{< figure src="https://arxiv.org/html/2507.23021v1/x2.png" alt="Figure from ScanDiff [Cartella+ ICCV’25]" caption="Figure from ScanDiff [Cartella+ ICCV’25]" >}}

A new research theme, understanding advertising videos, has also been proposed with [AdsQA](https://arxiv.org/abs/2509.08621), a QA benchmark for video understanding that incorporates challenges unique to ad videos. In this area, issues such as the sensitivity of reinforcement learning methods to data quality and the effects of prompt templates on performance are also analyzed.

{{< figure src="https://arxiv.org/html/2509.08621v1/x1.png" alt="Figure from AdsQA [Long+ ICCV’25]" caption="Figure from AdsQA [Long+ ICCV’25]" >}}

## Conclusion

Through my participation in ICCV 2025, I strongly realized that the computer vision field, especially image and design generation, has entered a phase where the focus has shifted from merely pursuing realism to emphasizing the “practicality and controllability” of the technology.

The trends observed in the workshops and main conference clearly show that generative AI is evolving from pixel-based outputs to the generation of hierarchical and structured design elements that align closely with real design workflows. At the same time, advances in flow models are enabling fast and accurate generation and editing. This will be a key driver in revolutionizing the PDCA cycle for creatives in advertising and marketing applications.

LY Corporation will continue to fulfill its responsibility in governing foundation data and leading international discussions, while proactively applying these cutting-edge generation and control technologies to our business. Through this, we aim to establish a strong technological competitive advantage and contribute to society.
