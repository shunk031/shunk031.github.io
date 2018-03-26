# resume-template

[![Build Status](https://travis-ci.org/shunk031/shunk031.github.io.svg?branch=master)](https://travis-ci.org/shunk031/shunk031.github.io)

*A simple Jekyll + GitHub Pages powered resume template.*

## Docs

### Running locally

#### Setup rbenv for this repo

``` shell
$ ruby-build 2.4.0 ~/.rbenv/versions/2.4.0-resume-template
$ cd this-resume-template-repo
$ rbenv local 2.4.0-resume-template
$ gem install bundle
```

To test locally, run the following in your terminal:

1. Clone repo locally
2. `bundle install`
3. `bundle exec jekyll serve`
4. Open your browser to `localhost:4000`

### Customizing

First you'll want to fork the repo to your own account. Then clone it locally and customize, or use the GitHub web editor to customize.

#### Options/configuration

Most of the basic customization will take place in the `/_config.yml` file. Here is a list of customizations available via `/_config.yml`:

[...write these out...]

#### Editing content

Most of the content configuration will take place in the `/_layouts/resume.html` file. Simply edit the markup there accordingly

### Publishing to GitHub Pages for free

[GitHub Pages](https://pages.github.com/) will host this for free with your GitHub account. Just make sure you're using a `gh-pages` branch, and the site will automatically be available at `yourusername.github.io/resume-template` (you can rename the repo to resume for your own use if you want it to be available at `yourusername.github.io/resume`). You can also add a CNAME if you want it to be available at a custom domain...

### Configuring with your own domain name

To setup your GH Pages site with a custom domain, [follow the instructions](https://help.github.com/articles/setting-up-a-custom-domain-with-github-pages/) on the GitHub Help site for that topic.

## License

The code and styles are licensed under the MIT license. [See project license.](LICENSE) Obviously you should not use the content of this demo repo in your own resume. :wink:

Disclaimer: Use of Homer J. Simpson image and name used under [Fair Use](https://en.wikipedia.org/wiki/Fair_use) for educational purposes. Project license does not apply to use of this material.
