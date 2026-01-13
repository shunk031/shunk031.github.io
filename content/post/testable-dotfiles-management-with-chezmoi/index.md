---
# Documentation: https://docs.hugoblox.com/managing-content/

title: "Testable Dotfiles Management With Chezmoi"
subtitle: ""
summary: "This article explains an approach to dotfiles management that emphasizes testability, using the author's dotfiles repository shunk031/dotfiles as a case study."
authors: ["Shunsuke Kitada"]
tags: ["dotfiles", "chezmoi", "Bats", "GitHub Actions"]
categories: ["tech"]
date: 2025-10-06T20:00:00+09:00
lastmod: 2025-10-06T20:00:00+09:00
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

This article explains an approach to dotfiles management that emphasizes testability, using the author's dotfiles repository [shunk031/dotfiles](https://github.com/shunk031/dotfiles) as a case study.

{{< blogcard url="https://github.com/shunk031/dotfiles" >}}

{{< toc >}}

## Introduction

### Dotfiles and Dotfiles Repositories

The *`dotfiles`* refer to configuration files that start with a "`.`" (dot) such as `.bashrc`, `.vimrc`, and `.gitconfig`. In recent years, [dotfiles repositories](https://awesomeopensource.com/projects/dotfiles) that manage these files using Git repositories have become widely popular among developers.

{{< blogcard url="https://awesomeopensource.com/projects/dotfiles" >}}
{{< blogcard url="https://github.com/webpro/awesome-dotfiles" >}}

The *`dotfiles repositories`* often function not just as configuration file management tools, but as automated development environment setup tools that include configuration files, installation scripts, and setup scripts. This enables quick and consistent setup on new machines and environments.

### The Problem of Untested Scripts

Most setup and installation scripts included in dotfiles repositories are not tested for proper functionality (which is painful). As a result, various problems can occur when setting up in new environments. Script errors, installation failures of some tools due to dependency issues, and script malfunctions due to OS updates may go unnoticed until actually executed. It's extremely stressful when you get a new computer or environment and excitedly start the setup process, only to have errors occur midway through, preventing the environment setup from completing.

This lack of quality assurance results in what should be automated environment construction consuming a lot of time on manual problem-solving and debugging.

### My Repository's Approach: Testable Configuration

To solve the above problems, my dotfiles repository builds an architecture that emphasizes testability. Setup scripts are managed as independent files to enable individual testing, quality is ensured through automated testing with [Bats](https://github.com/bats-core/bats-core), and continuous testing and code coverage measurement are performed in macOS and Ubuntu environments using GitHub Actions.

For managing dotfiles, I've adopted [chezmoi](https://www.chezmoi.io/). chezmoi is a modern dotfiles management tool with high popularity on GitHub ([10,000+⭐️](https://github.com/twpayne/chezmoi/stargazers)). Written in Go as a single, dependency-free binary, chezmoi is easy to install even on a brand-new, clean environment.

{{< blogcard url="https://github.com/twpayne/chezmoi" >}}
{{< blogcard url="https://www.chezmoi.io/" >}}

Environment setup on a new machine can be executed with the following very simple one-liner using chezmoi's official installer[^1].

```shell
sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply $GITHUB_USERNAME
```

Environment-specific settings can be dynamically generated using chezmoi's template functionality based on Go's `text/template` as follows.

```go:.gitconfig.tmpl
[user]                           # Can be dynamically specified via template functionality
    name = "{{.name}}"           # - User name
    email = "{{.email}}"         # - Email address etc.
{{- if eq .chezmoi.os "darwin"}} # macOS-specific settings
[credential]
    helper = osxkeychain
{{- end}}
```

{{< blogcard url="https://www.chezmoi.io/user-guide/templating/" >}}

In this way, we aim to achieve reliable dotfiles management by ensuring script quality through testable configuration and flexibly managing environment-specific settings through chezmoi's template functionality.

## Architecture Design: Testable Configuration

### Repository Structure

My repository is broadly divided into three directories: [`home/`](https://github.com/shunk031/dotfiles/tree/master/home), [`install/`](https://github.com/shunk031/dotfiles/tree/master/install), and [`tests/`](https://github.com/shunk031/dotfiles/tree/master/tests), managing dotfiles, environment setup scripts, and automated tests independently.

```
.
├── ...
│
├── home/                   # dotfiles under chezmoi management
│   ├── dot_bashrc          # - deployed as ~/.bashrc
│   ├── dot_vimrc           # - deployed as ~/.vimrc
│   ├── dot_config/         # - deployed as ~/.config/
│   └── .chezmoi.yaml.tmpl  # - chezmoi configuration file
│
├── install/                # setup scripts (testable)
│   ├── common/             # - common installation scripts
│   ├── macos/              # - macOS-specific scripts
│   └── ubuntu/             # - Ubuntu-specific scripts
│
├── tests/                  # automated tests with Bats
│   ├── install/            # - tests for installation scripts
│   └── files/              # - tests for files after chezmoi deployment
│
└── ...
```

### Design Philosophy

The core of this architecture lies in "separation of concerns" and "maximizing testability". Traditional dotfiles repositories mix configuration files and setup scripts, making testing difficult, but this configuration clearly separates each element.

#### The `install/` directory: Easy Unit Testing Through Script Separation

By making setup scripts independent from chezmoi, individual testing becomes possible.

- [`install/common/rust.sh`](https://github.com/shunk031/dotfiles/blob/master/install/common/rust.sh): Installation of tools used commonly across machines (e.g., Rust)
- [`install/macos/common/brew.sh`](https://github.com/shunk031/dotfiles/blob/master/install/macos/common/brew.sh): Installation of Homebrew used commonly on macOS
- [`install/ubuntu/common/misc.sh`](https://github.com/shunk031/dotfiles/blob/master/install/ubuntu/common/misc.sh): Installation of tools used commonly on Ubuntu (e.g., curl, jq)

Platform-specific configuration separates OS-specific logic, allowing each to be tested independently. Each script follows the single responsibility principle, handling only the installation of specific tools or packages.

#### The `home/` directory: chezmoi Templates and dotfiles

These are the actual dotfiles under chezmoi management. They follow chezmoi's unique file naming conventions [(`dot_` prefix etc.)](https://www.chezmoi.io/user-guide/frequently-asked-questions/design/#why-does-chezmoi-use-weird-filenames) and utilize template functionality. This repository specifies `home` as the source directory using the [.chezmoiroot](https://www.chezmoi.io/user-guide/advanced/customize-your-source-directory/) file[^2].

- [`home/dot_zshrc`](https://github.com/shunk031/dotfiles/blob/master/home/dot_zshrc): deployed as `~/.zshrc`
- [`home/dot_config/git/config.tmpl`](https://github.com/shunk031/dotfiles/blob/master/home/dot_config/git/config.tmpl): chezmoi template deployed as `~/.config/git/config`
- [`home/.chezmoi.yaml.tmpl`](https://github.com/shunk031/dotfiles/blob/master/home/.chezmoi.yaml.tmpl): chezmoi configuration file

It's independent from the scripts in the `install/` directory, separating configuration file placement and environment construction.

#### The `tests/` directory: Automated Testing with Bats

I use Bash Automated Testing System (Bats) to test scripts in the `install/` directory. The test directories and files are configured to be consistent with the script.

{{< blogcard url="https://github.com/bats-core/bats-core" >}}

- [`tests/install/common/rust.bats`](https://github.com/shunk031/dotfiles/blob/master/tests/install/common/rust.bats): Tests for Rust installation script
- [`tests/install/macos/common/brew.bats`](https://github.com/shunk031/dotfiles/blob/master/tests/install/macos/common/brew.bats): Tests for Homebrew installation script
- [`tests/files/common.bats`](https://github.com/shunk031/dotfiles/blob/master/tests/files/common.bats): Verification of file existence after chezmoi deployment

Each test file verifies the script's behavior and confirms that expected results (package installation, configuration file generation, etc.) are obtained.

## Test & CI/CD Strategy

This repository adopts a test strategy based on the fundamental policy of "continuous verification". We can verify that scripts in the `install/` directory work correctly in various environments and discover problems in advance to prevent failures during actual environment construction.

### Unit Test Implementation with Bats

My repository adopts [Bash Automated Testing System (Bats)](https://github.com/bats-core/bats-core) to verify the behavior of each installation script. Bats is a testing framework specifically for shell scripts that allows writing tests with simple syntax.

```bash:tests/install/macos/common/brew.bats
#!/usr/bin/env bats

@test "brew installation script exists" {
  [ -f "install/macos/common/brew.sh" ]
}

@test "brew installation script is executable" {
  [ -x "install/macos/common/brew.sh" ]
}

@test "brew installation script runs without errors" {
  run bash install/macos/common/brew.sh
  [ "$status" -eq 0 ]
}

@test "brew command is available after installation" {
  run command -v brew
  [ "$status" -eq 0 ]
}
```

Each test progressively verifies script existence, executable permissions, actual execution, and expected results (command availability, etc.).

### Comprehensive Verification with GitHub Actions

My repository uses GitHub Actions for multi-stage verification. In addition to unit tests, the workflow regularly executes actual end-to-end setup to achieve comprehensive quality assurance.

#### Unit Test Execution

My repository runs automated tests in macOS and Ubuntu environments to detect platform-specific issues early.

```yaml:.github/workflows/test.yaml
name: Test
on: [push, pull_request]

jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
    runs-on: ${{ matrix.os }}

    steps:
      - uses: actions/checkout@v4
      - name: Install Bats
        run: |
          if [[ "${{ matrix.os }}" == "ubuntu-latest" ]]; then
            sudo apt-get update && sudo apt-get install -y bats
          else
            brew install bats-core
          fi

      - name: Run tests
        run: bats tests/install/

      - name: Upload coverage reports
        uses: codecov/codecov-action@v3
```

#### Regular Execution of Actual Setup

More importantly, we should verify in environments identical to the actual user experience. This repository's workflow automatically executes the setup process using [`setup.sh`](https://github.com/shunk031/dotfiles/blob/master/setup.sh) on macOS and Ubuntu runners every Friday. This script wraps the chezmoi environment construction one-liner mentioned earlier.

```yaml:.github/workflows/remote.yaml
name: Snippet install
on:
  schedule:
    - cron: "0 0 * * 5"  # Every Friday

jobs:
  build:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-14]
        system: [client, server]
        exclude:
          - os: macos-14
            system: server

    runs-on: ${{ matrix.os }}
    steps:
      - name: Setup dotfiles with snippet
        run: |
          if [ "${OS}" == "macos-14" ]; then
            bash -c "$(curl -fsLS https://shunk031.me/dotfiles/setup.sh)"
          elif [ "${OS}" == "ubuntu-latest" ]; then
            bash -c "$(wget -qO - https://shunk031.me/dotfiles/setup.sh)"
          fi
```

This regular execution continuously monitors the impact of external dependency changes, OS updates, and package manager changes on environment construction, ensuring reliability when actual users execute the setup.

#### Code Coverage Measurement and Codecov Integration

My repository measures shell script code coverage using [kcov](https://github.com/SimonKagstrom/kcov) and visualizes it with [Codecov](https://codecov.io/). This helps identify untested code paths and improve testing. Actual measurement uses [`scripts/run_unit_test.sh`](https://github.com/shunk031/dotfiles/blob/master/scripts/run_unit_test.sh).

{{< blogcard url="https://github.com/SimonKagstrom/kcov" >}}
{{< blogcard url="https://about.codecov.io/" >}}

```bash
# Example of coverage measurement
kcov --clean --include-path=install/macos/common/ \
  coverage/ \
  bats tests/install/macos/common/brew.bats
```

Coverage reports are automatically commented on Pull Requests using [codecov/codecov-action](https://github.com/codecov/codecov-action), allowing immediate understanding of the impact of changes.

{{< blogcard url="https://github.com/codecov/codecov-action" >}}

#### Performance Measurement and Benchmark Automation

To continuously monitor shell startup performance after dotfiles application and detect the impact of configuration changes early, I've automated benchmark measurement in the workflow of GitHub Actions.

This implementation references the following article using [benchmark-action/github-action-benchmark](https://github.com/benchmark-action/github-action-benchmark). The GitHub Actions workflow measures both initial shell startup time and average startup time (measured 10 times) to quantify the impact of dotfiles configuration on shell startup.

{{< blogcard url="https://github.com/benchmark-action/github-action-benchmark" >}}
{{< blogcard url="https://zenn.dev/odan/articles/17a86574b724c9" >}}

Measurement results are published on [GitHub Pages](https://shunk031.me/my-dotfiles-benchmarks/), achieving continuous performance monitoring. We can numerically confirm the impact of adding new plugins or configurations on shell startup time, preventing performance degradation before it occurs.

{{< blogcard url="https://shunk031.me/my-dotfiles-benchmarks/" >}}

## Implementation Details and Operational Flow

### Structure and Implementation Examples of Setup Scripts

Scripts in the `install/` directory are designed following the single responsibility principle. Each script handles only the installation and configuration of specific tools, creating an independently testable structure.

As a basic script structure, OS-specific processing is separated into different files and implemented as platform-specific scripts. All installation scripts follow the following common pattern. For shell script writing practices, [Minimal safe Bash script template](https://betterdev.blog/minimal-safe-bash-script-template/) is helpful.

{{< blogcard url="https://betterdev.blog/minimal-safe-bash-script-template/" >}}

```bash
#!/usr/bin/env bash
set -Eeuo pipefail

# Debug mode setting
if [ "${DOTFILES_DEBUG:-}" ]; then
    set -x
fi

# Tool-specific functions
function is_tool_exists() {
    command -v tool_name &>/dev/null
}

function install_tool() {
    if ! is_tool_exists; then
        # Platform-specific installation process
        # macOS: brew install tool_name
        # Ubuntu: sudo apt-get install -y tool_name
    fi
}

# Main process
function main() {
    install_tool
    # Execute additional configuration process if needed
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
```

The conditional statement `if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then` executes the `main` function only when the script is directly executed. When a script is loaded from another file using the `source` command (e.g., when calling functions from test files), only function definitions are loaded and `main` is not executed[^3]. This allows the same script to be used both for "execution" and "library" purposes, greatly improving testability.

For example, Homebrew installation is separated into `install/macos/common/brew.sh`, and chezmoi Ubuntu installation is in `install/ubuntu/common/chezmoi.sh`. This structure achieves platform optimization and testability.

### Development and Maintenance Flow

#### New Application Addition Procedure

1. Create installation script

```bash
# Create install/macos/common/new_tool.sh
# Implement following the basic structure above
```

2. Create test file

```bash
# Create tests/install/macos/common/new_tool.bats
@test "new_tool installation script exists" {
  [ -f "install/macos/common/new_tool.sh" ]
}

@test "new_tool can be installed" {
  run bash install/macos/common/new_tool.sh
  [ "$status" -eq 0 ]
}
```

3. Run local tests

```bash
bats tests/install/macos/common/new_tool.bats
```

#### Test-Driven Development Process

Development always proceeds test-first.

1. Create test cases: First write expected behavior as tests
2. Minimal implementation: Implement minimal script that passes tests
3. Refactoring: Improve code while maintaining behavior
4. Integration testing: Verify operation in CI environment

This operational flow allows continuous improvement of dotfiles while maintaining quality and maintainability. Each change is necessarily covered by tests and verified in the CI pipeline, minimizing the risk of problems occurring in actual environments.

## Conclusion

This article explained the approach of "testable dotfiles management" combining chezmoi and test-driven development. We presented a comprehensive solution to the fundamental problem that traditional dotfiles repositories face: "not knowing if setup scripts work correctly until execution". Specifically, this was an approach combining unit testing with Bats, continuous verification with GitHub Actions, and regular execution of actual end-to-end setup. Please consider incorporating testability into your own dotfiles management to achieve reliable development environment construction.

{{< blogcard url="https://github.com/shunk031/dotfiles" >}}

[^1]: [chezmoi starts setup by referencing `$GITHUB_USERNAME/dotfiles` on GitHub.](https://www.chezmoi.io/quick-start/#start-using-chezmoi-on-your-current-machine:~:text=Create%20a%20new%20repository%20on%20GitHub%20called%20dotfiles%20and%20then%20push%20your%20repo%3A)
[^2]: By default, chezmoi uses [the repository root as the source directory](https://www.chezmoi.io/user-guide/advanced/customize-your-source-directory/).
[^3]: This is the same mechanism as Python's `if __name__ == "__main__"`.
