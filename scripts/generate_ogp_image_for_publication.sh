#!/usr/bin/env bash

set -eu

function check_tcardgen() {
    if ! command -v tcardgen &>/dev/null; then
        echo "The \`tcardgen\` command could not be found."
        echo "Please install the command: \`go install github.com/shunk031/tcardgen@latest\`"
        exit
    fi
}

function ensure_fonts() {
    # KintoSans (SIL OFL-1.1): https://github.com/ookamiinc/kinto
    local font_dir="assets/fonts"
    local kinto_release_url="https://github.com/ookamiinc/kinto/releases/download/v1.0.1/KintoSans.zip"
    local required_fonts=("KintoSans-Regular.ttf" "KintoSans-Light.ttf" "KintoSans-Bold.ttf")
    local font
    local missing=0

    for font in "${required_fonts[@]}"; do
        if [ ! -f "$font_dir/$font" ]; then
            missing=1
        fi
    done

    if [ "$missing" -eq 0 ]; then
        return
    fi

    echo "Fonts not found in \`$font_dir/\`. Downloading KintoSans from ookamiinc/kinto (OFL-1.1)..."
    mkdir -p "$font_dir"

    local tmp_dir
    tmp_dir="$(mktemp -d)"
    curl -sSL -o "$tmp_dir/KintoSans.zip" "$kinto_release_url"
    unzip -o -j "$tmp_dir/KintoSans.zip" \
        "Kinto Sans/KintoSans-Regular.ttf" \
        "Kinto Sans/KintoSans-Light.ttf" \
        "Kinto Sans/KintoSans-Bold.ttf" \
        "LICENSE.txt" \
        -d "$font_dir"
    rm -rf "$tmp_dir"
}

function generate_ogp_image() {
    local publication="$1"
    local fond_dir="assets/fonts/"
    local output_dir="content/publication/$publication/featured.png"
    local template_path="assets/ogp/tcardgen-template.png"
    local config_path="scripts/tcardgen/template.config.yaml"
    local index_file_path="content/publication/$publication/index.md"

    tcardgen --fontDir "$fond_dir" \
        --output "$output_dir" \
        --template "$template_path" \
        --config "$config_path" \
        "$index_file_path"
}

function main() {
    check_tcardgen
    ensure_fonts
    generate_ogp_image "$1"
}

main "$1"
