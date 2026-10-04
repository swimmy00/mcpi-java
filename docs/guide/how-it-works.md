# そもそもどういう仕組み？

この環境で「Python を実行すると、マイクラの世界にブロックが置かれる」までに、裏で何が起きているのかを解説します。

## ひとことで言うと

**自分のPCの中にマイクラサーバーを立てて、「ゲームで遊ぶ自分」と「Python プログラム」の両方がそのサーバーにつながる** 仕組みです。

![マイクラ・Docker の中のサーバー・Python（mcpi）の関係図](../images/architecture.svg)

登場人物は4人です。

| 登場人物 | 役割 | たとえると |
|---|---|---|
| マイクラサーバー（Paper） | ワールドを管理している本体 | 体育館そのもの |
| RaspberryJuice | Python からの命令を受け付けるプラグイン | 体育館の受付窓口 |
| マイクラ（ゲーム） | ワールドを見たり歩いたりする | 体育館に入って遊ぶ人 |
| Python（mcpi） | サーバーに命令を送る | 受付窓口に「ここに跳び箱を置いて」と頼む人 |

ポイントは、**Python はゲーム画面を操作しているわけではない** ということです。
Python はサーバーに直接「ここにブロックを置いて」と頼んでいて、ゲーム画面はサーバーの変化を映しているだけです。
だから、ゲームを開いていなくても Python の命令自体は動きます（見えないだけです）。

## なぜこんな仕組みが必要なの？

もともと `mcpi` は、Raspberry Pi（教育用の小さなコンピューター）向けの「Minecraft: Pi Edition」というマイクラ専用のライブラリでした。
Pi Edition には最初から Python で操作する機能が付いていましたが、**ふつうの Minecraft Java版にはこの機能がありません。**

そこで、

1. プラグインを入れられるマイクラサーバー（**Paper**）を用意して
2. Pi Edition と同じ命令を受け付けるプラグイン（**RaspberryJuice**）を入れる

ことで、Java版でも Pi Edition と同じ `from mcpi.minecraft import Minecraft` のコードが動くようにしています。

> 詳しくは [Paper と RaspberryJuice って何？](paper-and-raspberryjuice.md)

## 最初から動くまでの流れ

### ① `docker compose up -d` でサーバーが立ち上がる

Docker が `docker-compose.yaml` を読んで、次のことを自動でやってくれます。

1. マイクラサーバー用の「箱」（コンテナ）を作る
2. Minecraft サーバー本体（Paper 26.2）をダウンロードする
3. RaspberryJuice をダウンロードして、プラグインとして入れる
4. RaspberryJuice の設定ファイル（`plugins/RaspberryJuice/config.yml`）をコピーする
5. サーバーを起動する。RaspberryJuice も一緒に起動して、4711番で命令を待ち始める

> Docker が何者かは [Docker って何？](docker.md)

### ② マイクラで `localhost` に接続する

`localhost` は「自分のPC」という意味です。
マイクラは何も指定しないと 25565番 の窓口につなぎに行くので、①で立てたサーバーに入れます。

> `localhost` や「○○番」の意味は [localhost とポートって何？](localhost-and-ports.md)

### ③ `uv sync` で Python の準備をする

uv が、Python 本体と `mcpi` ライブラリをこのフォルダ専用に用意します。

> pip を使う場合は、`uv sync` の代わりに `python3 -m pip install mcpi==1.2.1`（Windows は `python -m pip ...`）でインストールします。
>
> uv が何者かは [uv って何？ pip と何が違うの？](uv.md)

### ④ `uv run python scripts/sample.py` で命令を送る

`sample.py` の中で、こんなやりとりが起きています。

```python
mc = Minecraft.create()
```
→ `localhost` の 4711番（RaspberryJuice の窓口）に接続する

```python
mc.postToChat("hogehoge")
```
→ RaspberryJuice に `chat.post(hogehoge)` という文字の命令が届く
→ RaspberryJuice がサーバーに「チャットに hogehoge と出して」と伝える
→ サーバーにつながっている全員のチャットに表示される

```python
pos = mc.player.getTilePos()
```
→ `player.getTile()` という命令が届く
→ RaspberryJuice が「プレイヤーは今ここにいるよ」と座標を返事する

```python
mc.setBlock(pos.x, pos.y+2, pos.z, 41)
```
→ `world.setBlock(x,y,z,41)` という命令が届く
→ サーバーのワールドに金ブロックが置かれ、ゲーム画面にも表示される

`mcpi` の正体は、**こうした文字の命令を送ったり、返事を受け取ったりしてくれる道具** です。

## まとめ

- マイクラサーバーを **Docker** で自分のPCの中に立てる
- サーバーには **RaspberryJuice** というプラグインが入っていて、4711番で Python からの命令を待っている
- 自分は **いつものマイクラ** でそのサーバーに入る
- **Python（mcpi）** が 4711番に命令を送ると、サーバーのワールドが変わって、ゲーム画面にも反映される
