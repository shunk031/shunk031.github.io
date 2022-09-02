#!/usr/bin/env bash

set -eu

function check_tcardgen() {
    if ! command -v tcardgen &>/dev/null; then
        echo "The \`tcardgen\` command could not be found."
        echo "Please install the command: \`go install github.com/shunk031/tcardgen@latest\`"
        exit
    fi
}

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
    check_tcardgen
    generate_ogp_image "$1"
}

main "$1"
