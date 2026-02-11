<div align="center">

[![Website Thumbnail](.github/README/banner-image.png)](https://shunk031.me)

# [`shunk031.me`](https://shunk031.me/)

[![Actions Status](https://github.com/shunk031/shunk031.github.io/workflows/Page%20Build/badge.svg)](https://github.com/shunk031/shunk031.github.io/actions?query=workflow%3A%22Page+Build%22)
[![Check Broken Links](https://github.com/shunk031/shunk031.github.io/actions/workflows/lychee-prune.yml/badge.svg)](https://github.com/shunk031/shunk031.github.io/actions/workflows/lychee-prune.yml)

[![gohugoio/hugo](https://img.shields.io/github/v/tag/gohugoio/hugo?color=FF4088&display_name=release&label=gohugoio/hugo&logo=hugo&logoColor=FF4088&sort=semver)](https://github.com/gohugoio/hugo)
[![HugoBlox/hugo-blox-builder](https://img.shields.io/github/v/tag/HugoBlox/hugo-blox-builder?color=0694cb&display_name=release&label=HugoBlox&logo=hugo&logoColor=0694cb&sort=semver)](https://github.com/HugoBlox/hugo-blox-builder)

[Hugo Academic](https://github.com/gcushen/hugo-academic) + GitHub Pages based on [Starter Hugo Academic](https://github.com/wowchemy/starter-hugo-academic).

</div>

## 🏃 Running locally

This repository uses `mise` for tool management (see `mise.toml`).

```shell
make setup
```

## 🔍️ Check contents

```sh
make run
```

## 🛠️ Update hugo modules

```sh
make update
```

## 🚀 Create a content

- Create a post

```sh
make post name="my-post-article"
```

- Create a post for some news

```sh
make news name="my-news"
```

- Creat a talk/event page

```sh
make event name="my-talk"
```

- Create a publication page

```sh
make publication name="author20xxconf"
```

- Create for thumbnail image

```sh
make publication-thumbnail pdf=/path/to/paper.pdf name='author20xxconf'
```

- Generate OGP image for the publication

```sh
make ogp-image name="kitada20XXconf"

# Load fonts from "assets/fonts/"
# Load template from "assets/ogp/tcardgen-template.png" directory
# Success to generate twitter card into content/publication/kitada20XXconf/featured.png
```

## 🏷️ Manage publication tags

Add conference name and year tags to publications automatically:

- Preview changes (dry-run mode)

```sh
make add-conference-tags-dry-run
```

- Apply tag additions

```sh
make add-conference-tags
```

This script will:

- Add conference name tags (e.g., `YANS`, `ANLP`, `MIRU`) to all conference publications
- Add conference+year tags (e.g., `YANS2019`, `ANLP2025`) for easier filtering
- Automatically map `NLP` → `ANLP` for 言語処理学会年次大会
- Preserve formatting and comments in YAML frontmatter
- Skip journal articles and dissertations

### 😀 Available Icons/Emojis

- See the following for more details:
  - Icons: https://docs.hugoblox.com/reference/markdown/#inline-image
  - Emojis: https://docs.hugoblox.com/reference/markdown/#emojis

## 📝 License

The code and styles are licensed under the MIT license. [See project license.](LICENSE) Obviously you should not use the content of this demo repo in your own resume. :wink:

Disclaimer: Use of Homer J. Simpson image and name used under [Fair Use](https://en.wikipedia.org/wiki/Fair_use) for educational purposes. Project license does not apply to use of this material.
