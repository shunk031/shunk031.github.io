# My website

[![Actions Status](https://github.com/shunk031/shunk031.github.io/workflows/Page%20Build/badge.svg)](https://github.com/shunk031/shunk031.github.io/actions?query=workflow%3A%22Page+Build%22)

[Hugo Academic](https://github.com/gcushen/hugo-academic) + GitHub Pages based on [Starter Hugo Academic](https://github.com/wowchemy/starter-hugo-academic).

[![Website Thumbnail](.github/README/thumbnail.png)](http://www.shunk031.me)

## Running locally

- Install `hugo` to build page

### MacOS

```sh
$ brew install hugo
```

## Check contents

```sh
$ make run
```

## Update hugo modules

```sh
$ make update
```

## Create a content
### Create a post for some news

```sh
$ hugo new --kind post post/my-news
```

### Create a publication page

```sh
$ hugo new --kind publication publication/name2020conf
```

- Create for thumbnail image.

```sh
$ convert paper.pdf[0] -resize 640x640^ -crop 640x480+0+0 -alpha remove featured.png
```

### Available Icons

- See https://wowchemy.com/docs/page-builder/#icons for more details

## License

The code and styles are licensed under the MIT license. [See project license.](LICENSE) Obviously you should not use the content of this demo repo in your own resume. :wink:

Disclaimer: Use of Homer J. Simpson image and name used under [Fair Use](https://en.wikipedia.org/wiki/Fair_use) for educational purposes. Project license does not apply to use of this material.
