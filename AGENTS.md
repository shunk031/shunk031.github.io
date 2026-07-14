# AGENTS.md

shunk031.me (Hugo 製個人サイト) のエージェント向け作業ガイドです。テーマは HugoBlox (hugo-blox-builder 系統) を Hugo Modules で利用し、GitHub Pages (`gh-pages` ブランチ) へデプロイされます。`CLAUDE.md` は本ファイルへの symlink です。

## セットアップ

- ツール管理: 作業開始時に `make setup` (= `mise install`) を実行してください。hugo-extended / lychee のバージョンは `mise.toml` が single source of truth で、CI も `mise.toml` から読み取ります。バージョンを変えるときは `mise.toml` だけを変更してください。
- ローカルサーバ: `make run` で起動します。その他の定型操作 (`make post` / `make news` / `make event` / `make publication` など) は `Makefile` と `README.md` を参照してください。
- ビルド検証: `mise exec -- hugo --gc --minify --printUnusedTemplates` を CI と同条件として使ってください。`layouts/` 配下に未使用テンプレートの警告が出ると CI が fail します。

## ブランチと worktree

- main 読み取り専用: 変更を伴うタスクは、着手時に `gwq add -b <task-branch>` で worktree を作成し、`cd "$(gwq get <task-branch>)"` で移動してから編集を始めてください。
- PR 運用: squash merge 前提です。コミットは conventional commits 形式 (`feat:` / `fix:` / `ci:` / `perf:` など) にしてください。

## テストとリント

- pytest: `uv run --with pytest --with ruamel.yaml pytest tests/ -q` で実行します。`pyproject.toml` は置かず、`uv run --with` で都度依存を解決する方式です。
- CI の全体像: `test.yml` (pytest) / `lint.yml` (`scripts/lint_frontmatter.py`) / `gh-pages.yml` (check-typo → build → check-broken-links → deploy)。deploy は check-broken-links の成功が条件です。
- typo 対応: `typos` の辞書にない誤字 (固有名詞に近い転置ミスなど) を修正したときは、`_typos.toml` の `extend-words` にも追加して再発を CI で検知できるようにしてください。

## Markdown 編集の注意

- 差分の最小化: `content/` の `.md` を編集したら、commit 前に `git diff` を確認し、意図した行以外の整形差分 (空行の増減、リストや footnote の再整形など) が混入していたら取り除いてください。フォーマッタ hook が発火する環境では、数行の修正は `perl -pi -e` など Bash 経由で編集すると安全です。

## コンテンツ規約

- URL 変更時の aliases: permalink・slug・ディレクトリ名を変更するときは、同じ PR で旧 URL の `aliases:` を該当ページの frontmatter に必ず追加してください (過去に `/talk/` → `/event/` の permalink 変更でリダイレクト漏れが起き、全 event ページが 404 になりました)。
- 内部リンクの追従: URL を変えたら、旧 URL への本文リンクが残っていないか `git grep` で確認してください。CI の lychee は `--root-dir` 付きで実行され、root-relative な内部リンク (`/event/...` など) も検査されます。
- タグ/カテゴリの表記: 既存の正規表記に合わせてください (例: `Non-refereed`, `Invited Presentation`, `International Publication`)。表記ゆれは `lint.yml` が fail させます。意図的に残す例外は `scripts/lint_frontmatter.py` の `KNOWN_CASING_EXCEPTIONS` で管理します。
- 著者名の表記: 英語表記は名-姓順 (`Kazuya Ohata`) に統一してください。同じ論文を扱う `content/publication/` と `content/news/` のページ間でも表記を揃えてください。
- view 指定: セクション `_index.md` の `view:` は数値ではなく文字列 (`compact`, `citation` など) を使ってください (Hugo 0.153+ では YAML の非負整数が uint64 になり、テーマの数値マッピングが機能しません)。

## スキル (定型作業)

- 置き場所: `.agents/skills/` が source of truth です。`.claude/skills` はここへの symlink で、Claude Code からも同じスキルが見えます。ツール固有のスキルを重複して作らないでください。
- 対応表: event ページの追加は `hugo-event-intake`、publication のサムネイル生成は `hugo-publication-thumbnail`、採択・発表 news の同期は `hugo-conference-news-sync` を使ってください。呼び出しコマンドは各 `SKILL.md` を参照し、conference news 同期は top-level の `scripts/sync_conference_news.py` を使います (スキル配下に同名スクリプトがあっても top-level 版が正です)。

## リンク切れの運用

- ローカル検査: `make check-broken-links` で CI と同じ検査を実行できます。
- excludes の使い分け: 恒久的に死んだ URL は `.lychee/exclude-permanent.txt`、一時的な障害 (TLS 非互換・レート制限など) は `.lychee/exclude-temporary.txt` に理由コメント付きで追加してください。temporary 側は週次の `lychee-prune.yml` が復活した URL を自動除去します。
- CI の一時失敗: 外部サイトの 503 や timeout で check-broken-links が落ちた場合は、まず `gh run rerun <run-id> --failed` で再実行し、それでも失敗する場合にのみ exclude や修正を検討してください。

## 依存とバージョン

- Hugo の上限: hugo-extended は **0.155.3 が上限**です。0.156.0 以降はテーマの `blox-bootstrap v5.9.7` が削除済みの `getCSV` を使っているためビルドできません。それ以上へ進むには HugoBlox kit への移行が必要です (issue #380)。
- 自動更新: `mise.toml` は Renovate (`renovate.json`)、GitHub Actions と Go modules は Dependabot が追従します。

## アセット

- 画像/PDF: 大きいファイルは追加前に圧縮してください (PNG は可逆圧縮、PDF は Ghostscript `/ebook` 相当で品質確認の上)。content 配下の `featured.*` はテーマがファイル名で参照するためリネームしないでください。
- フォント: OGP 画像生成 (`make ogp-image` / tcardgen) 用の KintoSans は git 管理しません。`scripts/generate_ogp_image_for_publication.sh` が初回実行時に ookamiinc/kinto のリリースから `assets/fonts/` (gitignore 済み) へ自動ダウンロードします。フォントの TTF をコミットしないでください (経緯は issue #381 / PR #388)。
