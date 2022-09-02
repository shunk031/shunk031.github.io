#!/usr/bin/env bash

set -eu

function generate_ogp_image() {
    local publication="$1"
    local fond_dir="assets/fonts/"
    local output_dir="content/publication/$publication/featured.png"
    local template_path="assets/ogp/tcardgen-template.png"
    local config_path="config/tcardgen/template.config.yaml"
    local index_file_path="content/publication/$publication/index.md"

    tcardgen --fontDir "$fond_dir" \
        --output "$output_dir" \
        --template "$template_path" \
        --config "$config_path" \
        "$index_file_path"
}

function main() {
    generate_ogp_image "$1"
}

main "$1"
