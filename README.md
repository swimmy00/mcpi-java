# mcpi-java

**Minecraft Java版を Python で操作する**ための環境です。  
自分のPCに `Docker` でマイクラサーバーを立てて、Python から `mcpi` の操作が可能になります。

```python
from mcpi.minecraft import Minecraft
mc = Minecraft.create()

# チャットにコメントを表示
mc.postToChat("swimmy is happy!!!")

# ブロックを配置
pos = mc.getTilePos()
mc.setBlock(pos.x, pos.y + 2, pos.z, 46, 1)
```

## 必要なもの

- Minecraft Java版（購入済みのアカウント）
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [uv](https://docs.astral.sh/uv/)（pip でもOK。その場合は Python 3.12 以上が必要）
- [VS Code](https://code.visualstudio.com/) ＋ [Python 拡張機能](https://marketplace.visualstudio.com/items?itemName=ms-python.python)（おすすめ）

## クイックスタート

```bash
git clone <このリポジトリのURL>
cd mcpi-java
docker compose up -d   # サーバー起動（初回は数分かかる）
uv sync                # Python環境の準備（初回のみ）
```

> **💡 pip を使う場合**（`uv sync` の代わりに）
>
> ```bash
> python3 -m venv .venv            # Windows は python -m venv .venv
> source .venv/bin/activate        # Mac
> .venv\Scripts\activate           # Windows（PowerShell）
> source .venv/Scripts/activate    # Windows（Git Bash）
> pip install mcpi==1.2.1
> ```

1. マイクラを **バージョン 26.2** で起動して、マルチプレイ → サーバーを追加 → `localhost` に接続
2. ワールドに入ったら、VS Code で `samples/hello.py` を開いて、右上の **▷（実行ボタン）** を押す

> 右下に `.venv` と書かれた Python が選ばれていればOKです。違うときは、そこをクリックして `.venv` のものを選んでください。
>
> ターミナルから実行する場合は `uv run python samples/hello.py`（pip の人は環境を有効にしてから `python samples/hello.py`）

チャットに「hogehoge」が出て、頭の上に金ブロックが置かれたら成功です 🎉

うまくいかない時や、もっと詳しい手順は 👉 **[環境構築手順書（docs/setup.md）](docs/setup.md)**

## 解説資料

「そもそも何をしているの？」を知りたい人向けの資料です。

| 資料 | 内容 |
|---|---|
| [そもそもどういう仕組み？](docs/guide/how-it-works.md) | サーバーを立ててから Python で操作できるようになるまでの全体像 |
| [Docker って何？](docs/guide/docker.md) | サーバーを「箱」に入れて動かす道具の話 |
| [localhost とポートって何？](docs/guide/localhost-and-ports.md) | `localhost:4711` の意味。いちばんハマりやすいところ |
| [Paper と RaspberryJuice って何？](docs/guide/paper-and-raspberryjuice.md) | マイクラサーバー本体と、Python から操作するためのプラグイン |
| [uv って何？ pip と何が違うの？](docs/guide/uv.md) | Python の環境をみんなで同じにする道具の話 |
