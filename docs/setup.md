# 環境構築手順書

Minecraft Java版を Python（`mcpi`）で操作できるようにするまでの、詳しい手順です。
上から順番に進めれば動くように書いています。

> 仕組みを先に知りたい人は [そもそもどういう仕組み？](guide/how-it-works.md) からどうぞ。

## 目次

1. [全体の流れ](#1-全体の流れ)
2. [必要なもの](#2-必要なもの)
3. [ソフトのインストール](#3-ソフトのインストール)
4. [リポジトリを手元に持ってくる](#4-リポジトリを手元に持ってくる)
5. [サーバーを起動する](#5-サーバーを起動する)
6. [マイクラを 26.2 で起動する](#6-マイクラを-262-で起動する)
7. [サーバーに接続する](#7-サーバーに接続する)
8. [Python の準備をする](#8-python-の準備をする)
9. [サンプルを動かす](#9-サンプルを動かす)
10. [ふだんの使い方](#10-ふだんの使い方)
11. [トラブルシューティング](#11-トラブルシューティング)
12. [設定の詳細](#12-設定の詳細)
13. [ファイル構成](#13-ファイル構成)
14. [既知の注意点](#14-既知の注意点)

---

## 1. 全体の流れ

```
① Docker でマイクラサーバーを起動する（自分のPCの中）
② いつものマイクラ（公式ランチャー）でそのサーバーに入る
③ Python からサーバーに命令を送ると、ゲームの中に反映される
```

所要時間の目安は、ソフトのインストールも含めて **30分〜1時間** です（大半はダウンロード待ちです）。

## 2. 必要なもの

| もの | 用途 | 備考 |
|---|---|---|
| Minecraft Java版 | ゲーム本体 | 購入済みの Microsoft アカウントが必要 |
| Docker Desktop | マイクラサーバーを動かす | 無料（[Dockerって何？](guide/docker.md)） |
| uv | Python と mcpi を用意する | 無料（[uvって何？](guide/uv.md)）。Python 本体は別途インストール不要 |
| Git | このリポジトリを取ってくる | ZIP でダウンロードするなら不要 |
| ターミナル | コマンドを打つ | Mac は「ターミナル」、Windows は「PowerShell」。VS Code 内のターミナルでもOK |
| VS Code ＋ Python 拡張機能 | Python ファイルを書いて実行する | 無料・おすすめ。拡張機能は VS Code の「拡張機能」で `Python`（Microsoft 製）を検索して入れる |

> **💡 pip を使う場合**: uv の代わりに pip でも動きます。その場合は **Python 3.12 以上** を自分でインストールしておいてください（[python.org](https://www.python.org/downloads/)）。

> この手順書のコマンドは Mac / Windows どちらでも同じように使えます。

## 3. ソフトのインストール

### 3-1. Docker Desktop

1. [Docker Desktop の公式ページ](https://www.docker.com/products/docker-desktop/) から、自分のPC用（Mac なら Apple Silicon か Intel か）をダウンロード
2. インストールして、**Docker Desktop を起動**する（メニューバー／タスクバーにクジラのアイコンが出ればOK）
3. ターミナルで確認

```bash
docker --version
docker compose version
```

バージョン番号が表示されれば成功です。

> Docker Desktop は **起動している間だけ** 使えます。PCを再起動したら、Docker Desktop も起動しておいてください。

### 3-2. uv

Mac:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows（PowerShell）:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

インストール後、**ターミナルを一度閉じて開き直して** から確認します。

```bash
uv --version
```

> Mac で Homebrew を使っているなら `brew install uv` でもOKです。

> **💡 pip を使う場合**: この手順（uv のインストール）は飛ばしてOKです。代わりに `python3 --version`（Windows は `python --version`）で 3.12 以上が表示されるか確認してください。

### 3-3. Git（必要な人だけ）

`git --version` でバージョンが出れば、すでに入っています。
入っていない場合は [Git 公式サイト](https://git-scm.com/downloads) からインストールしてください。

## 4. リポジトリを手元に持ってくる

```bash
git clone <このリポジトリのURL>
cd mcpi-java
```

> Git を使わない場合は、GitHub のページの「Code」→「Download ZIP」でダウンロードして解凍し、ターミナルでそのフォルダに移動してください。

**ここから先のコマンドは、すべてこの `mcpi-java` フォルダの中で実行します。**

## 5. サーバーを起動する

```bash
docker compose up -d
```

初回は、サーバーのイメージと Minecraft サーバー本体のダウンロードがあるので **数分かかります**。
2回目以降は数十秒で起動します。

起動できたかどうかは、ログで確認します。

```bash
docker compose logs -f
```

次の2行が出ていれば準備OKです。

```
[RaspberryJuice] Using host:port - 0.0.0.0:4711
Done (xx.xxxs)! For help, type "help"
```

確認できたら `Ctrl + C` でログ表示を終了します（サーバーは止まりません）。

## 6. マイクラを 26.2 で起動する

> ⚠️ **ここが一番の注意ポイントです。**
> サーバーは **26.2** で動いています。ランチャーの「最新リリース」が 26.2 より新しい場合、そのままでは接続できません。

初回だけ、26.2 用の「起動構成」を作ります。

1. Minecraft ランチャーを起動して、Microsoft アカウントでログイン
2. 「Minecraft: Java Edition」を選ぶ
3. 上のタブの **「起動構成」** → **「新規作成」**
4. 名前に「mcpi 26.2」など分かりやすい名前を入れる
5. **バージョン** で **「release 26.2」** を選ぶ
6. 「作成」

作ったら「プレイ」タブに戻り、左下の選択欄で **「mcpi 26.2」** を選んで「プレイ」します。
（初回は 26.2 本体のダウンロードで少し待ちます）

## 7. サーバーに接続する

1. タイトル画面で **「マルチプレイ」**
2. **「サーバーを追加」**
3. サーバーアドレスに `localhost` と入力して「完了」
4. 追加されたサーバーを選んで **「サーバーに接続」**

ワールドに入れたら成功です。このサーバーは **クリエイティブモード固定** なので、空を飛んだりブロックを自由に出したりできます。

> `localhost` は「自分のPC」という意味です。詳しくは [localhost とポートって何？](guide/localhost-and-ports.md)

## 8. Python の準備をする

```bash
uv sync
```

これで次のことが自動で行われます。

- 必要なバージョンの Python（3.12）を用意する
- このフォルダ専用の Python 環境（`.venv` フォルダ）を作る
- `mcpi` をインストールする

`Installed 1 package` のように表示されれば完了です。**初回だけ** 実行すればOKです。

> **💡 pip を使う場合**（`uv sync` の代わりに）
>
> ```bash
> python3 -m pip install mcpi==1.2.1     # Mac
> python -m pip install mcpi==1.2.1      # Windows
> ```
>
> - `pip install mcpi` ではなく `python3 -m pip ...` と書いているのは、Mac だと `pip` コマンドが無く `pip3` しか無いことが多いからです。この書き方なら確実に「その Python」に入ります
> - `mcpi==1.2.1` とバージョンを指定しているのは、uv の人（`uv.lock`）と同じバージョンにそろえるためです
> - `error: externally-managed-environment` と出て止まった場合は、Homebrew などで入れた Python を使っています。この場合は pip ではなく uv を使ってください（[3-2](#3-2-uv) → この章の `uv sync`）

## 9. サンプルを動かす

マイクラでサーバーに入った状態のまま、VS Code で `samples/hello.py` を開いて、右上の **▷（実行ボタン）** を押します。

> 実行ボタンを押す前に、VS Code の右下に表示されている Python を確認してください。違うときは、そこをクリックして選び直します。
>
> - **uv の人**: `3.12.x (.venv)` のように **`.venv` と書かれた Python**
> - **pip の人**: 手順8で mcpi をインストールした Python（3.12 以上。`.venv` ではないもの）

ターミナルから実行する場合は、次のコマンドでも同じです。

```bash
uv run python samples/hello.py
```

> **💡 pip を使う場合**: `python3 samples/hello.py`（Windows は `python samples/hello.py`）

ゲーム内で次のようになれば、すべて成功です 🎉

- チャットに「hogehoge」と表示される
- 自分の頭の上に金ブロックが置かれる

`samples/hello.py` の中身はこうなっています。

```python
from mcpi.minecraft import Minecraft
mc = Minecraft.create()  # サーバー（localhost:4711）に接続する

mc.postToChat("hogehoge")  # チャットにメッセージを送る

pos = mc.player.getTilePos()  # 自分（プレイヤー）の位置を取得する
mc.setBlock(pos.x, pos.y+2, pos.z, 41)  # 頭の上（y+2）に金ブロック（ID 41）を置く
```

> uv の人がターミナルで Python ファイルを実行するときは、必ず **`uv run python ファイル名`** の形で実行してください。
> `uv run` を付けると、手順8で用意した環境（mcpi が入っている環境）で実行されます。
> VS Code の実行ボタンなら、右下で `.venv` が選ばれていれば自動でその環境が使われます。

## 10. ふだんの使い方

| やりたいこと | コマンド |
|---|---|
| サーバーを起動する | `docker compose up -d` |
| サーバーを止める | `docker compose down` |
| ログを見る | `docker compose logs -f`（`Ctrl + C` で終了） |
| Python を実行する | VS Code の ▷ ボタン、または `uv run python samples/hello.py` |
| ライブラリを追加する | `uv add パッケージ名` |
| ワールドを完全にリセットする | `docker compose down -v`（⚠️ ワールドが消えます） |

> **💡 pip を使う場合**: Python の実行は `python3 ファイル名`、ライブラリの追加は `python3 -m pip install パッケージ名` です（Windows は `python3` → `python`）。

- `docker compose down` で止めても、**ワールドのデータは残ります**。次に起動すると続きから遊べます
- このサーバーは **Docker Desktop が起動していると自動で起動する** 設定です。使わない時に止めたい場合は `docker compose down` してください

## 11. トラブルシューティング

### マイクラで「サーバーのバージョンが古いです」「互換性がありません」と出る

ランチャーで 26.2 以外のバージョンを起動しています。
[手順6](#6-マイクラを-262-で起動する) の起動構成を選んで起動しているか確認してください。

### マイクラで「接続が拒否されました」と出る／Python で `ConnectionRefusedError` が出る

サーバーが起動していません。

1. Docker Desktop が起動しているか確認する
2. `docker compose up -d` を実行する
3. `docker compose logs -f` で `Done` が出るまで待つ

### Python で `ModuleNotFoundError: No module named 'mcpi'` が出る

`uv run` を付けずに `python` だけで実行しています。
`uv run python samples/hello.py` のように実行してください。
それでもダメな場合は `uv sync` をもう一度実行してください。

uv の人が VS Code の実行ボタンで出た場合は、右下の Python が `.venv` のものになっているか確認してください。

pip を使っている場合は、**mcpi をインストールした Python と、実行している Python が別もの** になっています。
PC に Python が複数入っているとよく起きます。次のように、実行するのと同じ `python3` で入れ直すのが確実です。

```bash
python3 -m pip install mcpi==1.2.1   # Windows は python -m pip ...
python3 samples/hello.py             # Windows は python samples/hello.py
```

VS Code の実行ボタンで出た場合は、右下の Python を、mcpi を入れた Python に選び直してください。

### Python で `AttributeError: 'function' object has no attribute 'postToChat'` が出る

`Minecraft.create` の後ろに `()` が抜けています。

```python
mc = Minecraft.create     # ✕
mc = Minecraft.create()   # ○
```

### コードを直したのに、同じエラーが出る

ファイルが保存されていない可能性があります。
VS Code のタブ名の横に「●」が付いていたら未保存です。`Cmd + S`（Windows は `Ctrl + S`）で保存してください。

### ログに `Unsupported class file major version` と出る

Minecraft サーバーのバージョンと RaspberryJuice のバージョンが合っていません。
`docker-compose.yml` の `VERSION` を変更した場合に起きます。
詳しくは [Paper と RaspberryJuice って何？](guide/paper-and-raspberryjuice.md) を参照してください。

### Python からつながらない（タイムアウトする、すぐ切れる）

ログの `[RaspberryJuice] Using host:port` の行を確認してください。
`0.0.0.0:4711` ではなく `localhost:4711` になっている場合は、`plugins/RaspberryJuice/config.yml` がサーバーに反映されていません。
`docker compose up -d --force-recreate` で作り直してください。

## 12. 設定の詳細

### docker-compose.yml

| 設定 | 値 | 意味・理由 |
|---|---|---|
| `name` | `mcpi-java` | プロジェクト名。フォルダ名を変えても、ワールドの保存場所（`mcpi-java_mc-data`）が変わらないように固定している |
| `image` | `itzg/minecraft-server` | マイクラサーバーを Docker で動かすための定番イメージ |
| `TYPE` | `PAPER` | プラグインが使えるサーバー「Paper」を使う |
| `VERSION` | `26.2` | RaspberryJuice v2.0.0 が対応しているバージョン（Paper 26.2 / Java 25 向け） |
| `MODE` | `creative` | ゲームモードをクリエイティブにする |
| `FORCE_GAMEMODE` | `true` | 接続するたびにクリエイティブに戻す（すでにサバイバルで入ったことがある人にも効く） |
| `PLUGINS` | RaspberryJuice の jar の URL | 起動時に自動でダウンロードして配置される |
| `ports` | `127.0.0.1:25565`、`127.0.0.1:4711` | **このPCからしか接続できない** ようにしている（同じ Wi-Fi の他の端末からは不可） |
| `volumes` | `mc-data:/data` | ワールドなどのデータを保存する場所。コンテナを作り直しても消えない |
| `volumes` | `./plugins:/plugins:ro` | リポジトリの `plugins/` を起動時にサーバーへコピーする（RaspberryJuice の設定を配るため） |

- `25565` は Minecraft 本体の接続口、`4711` は Python（mcpi）の接続口です

### plugins/RaspberryJuice/config.yml

RaspberryJuice の設定ファイルです。デフォルトから **`hostname` だけ** 変えています。

| 設定 | 値 | 意味 |
|---|---|---|
| `hostname` | `0.0.0.0` | Docker の外（自分のPC）からの接続を受け付ける。デフォルトの `localhost` だとコンテナの中からしか接続できない |
| `port` | `4711` | Python からの接続口 |
| `location` | `RELATIVE` | 座標は **スポーン地点を (0, 0, 0)** とした相対座標で扱う |

> ⚠️ `hostname: 0.0.0.0` と `ports` の `127.0.0.1` は **セットで扱ってください**。
> 4711番の接続口は、パスワードなしで誰でもブロックを壊したりできます。`127.0.0.1` を外すと、同じネットワークの他人からも操作できてしまいます。
> 理由は [localhost とポートって何？](guide/localhost-and-ports.md) で解説しています。

### Python 環境（uv）

| ファイル | 役割 |
|---|---|
| `pyproject.toml` | 必要なライブラリの一覧（今は `mcpi` だけ） |
| `uv.lock` | ライブラリのバージョンを固定した記録。みんなが同じバージョンを使うためのもの |
| `.python-version` | 使う Python のバージョン（3.12） |

ライブラリを追加したい時は `uv add パッケージ名` を実行し、`pyproject.toml` と `uv.lock` の両方をコミットしてください。

## 13. ファイル構成

```
mcpi-java/
├── README.md               # 入口（概要とクイックスタート）
├── docker-compose.yml      # マイクラサーバーの設定
├── plugins/
│   └── RaspberryJuice/
│       └── config.yml      # RaspberryJuice の設定（hostname: 0.0.0.0）
├── pyproject.toml          # Python で使うライブラリの一覧
├── uv.lock                 # ライブラリのバージョン固定
├── .python-version         # Python のバージョン（3.12）
├── .gitignore
├── samples/
│   └── hello.py            # 動作確認用サンプル
└── docs/
    ├── setup.md            # この手順書
    ├── images/
    │   └── architecture.svg  # 仕組みの図
    └── guide/              # 解説資料
        ├── how-it-works.md
        ├── docker.md
        ├── localhost-and-ports.md
        ├── paper-and-raspberryjuice.md
        └── uv.md
```

## 14. 既知の注意点

- **バージョンを変える時は要注意**: RaspberryJuice は対応している Minecraft / Paper のバージョンが決まっています。`VERSION` を変える前に [RaspberryJuice のリリース情報](https://github.com/sakebomb/RaspberryJuice/releases) で対応状況を確認してください
  - 例: v2.0.0 は Java 25 向けにビルドされているので、Paper 1.21.1 では `Unsupported class file major version 69` というエラーで読み込めません
  - サーバーの `VERSION` を変えたら、ランチャーの起動構成のバージョンも合わせてください
- **用途**: この構成は「自分のPCで、1人〜少人数で試す」ためのものです。教室で複数の生徒に配る運用は別途検討が必要です
