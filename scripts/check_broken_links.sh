#!/usr/bin/env bash

set -eux

function main() {
    local SCRIPT_URL="https://raw.githubusercontent.com/ruzickap/action-my-broken-link-checker/v2/entrypoint.sh"

    export INPUT_URL="https://shunk031.github.io"
    export INPUT_PAGES_PATH="./public"
    export INPUT_CMD_PARAMS="\
            --timeout=20 \
            --buffer-size 8192 \
            --max-connections=10 \
            --max-response-body-size=70000000 \
            -e linkedin.com \
            -e twitter.com \
            -e facebook.com \
            -e gstatic.com \
            -e researchgate.net \
            -e arxiv.org \
            -e valuenex.com \
            -e challenge2018.isic-archive.com \
            -e paper-survey \
            -e publication/#\\d \
            -e index.webmanifest \
            -e honet-ict.org \
            -e jsps.go.jp \
            -e www.cikm2022.org \
            -e .*.xml \
            "

    wget -qO- "${SCRIPT_URL}" | bash
}

main
