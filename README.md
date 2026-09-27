# webapp-practice

React + FastAPI + PostgreSQL を使用したWebアプリケーション開発の学習用プロジェクトです。

Windows 11上にローカル開発環境を構築し、以下の技術を組み合わせてWebアプリケーションを開発します。

* **Frontend**: React
* **Backend**: Python / FastAPI
* **Database**: PostgreSQL
* **ORM**: SQLAlchemy
* **Version Control**: Git / GitHub

本READMEでは、初期環境構築から、FastAPIとPostgreSQLの接続、ReactからFastAPIへのAPIアクセスまでの手順をまとめています。

## 参考

本プロジェクトの初期環境構築では、以下の記事を参考にしています。

- [ローカルにReact + FastAPI + PostgreSQLの環境構築をする](https://zenn.dev/sanpi34/articles/cb8b97e4ee3756)

> 上記記事はmacOS環境を前提としています。
> 本プロジェクトでは、記事の構成を参考にしつつ、Windows 11環境に合わせて手順を変更しています。

---

## 目次

1. [環境](#環境)
2. [必要なもの](#必要なもの)
3. [ディレクトリ構成](#ディレクトリ構成)
4. [Gitのインストール](#1-gitのインストール)
5. [VS Code](#2-vs-code)
6. [Node.jsのインストール](#3-nodejsのインストール)
7. [Pythonのインストール](#4-pythonのインストール)
8. [PostgreSQLのインストール](#5-postgresqlのインストール)
9. [PostgreSQLの準備](#6-postgresqlの準備)
10. [Python環境構築](#7-python環境構築)
11. [SQLAlchemyの設定](#8-sqlalchemyの設定)
12. [モデル定義](#9-モデル定義)
13. [FastAPIの実装](#10-fastapiの実装)
14. [FastAPIサーバの起動](#11-fastapiサーバの起動)
15. [Reactフロントエンド](#12-reactフロントエンド)
16. [動作確認](#13-動作確認)
17. [トラブルシューティング](#14-トラブルシューティング)
18. [GitHubへの公開](#15-githubへの公開)

---

# 環境

本READMEでは、以下の環境を前提としています。

| 項目         | バージョン                      |
| ---------- | -------------------------- |
| OS         | Windows 11                 |
| Python     | 3.14.7                     |
| Node.js    | 24.20.0                    |
| npm        | 11.19.0　　　　　           |
| Git        | 2.55.0.windows.5           |
| PostgreSQL | 18.6                       |
| SQLAlchemy | 2.0.52                     |
| FastAPI    | 0.141.1                    |
| Uvicorn    | 0.54.0                     |
| React      | 0.1.0                      |

各ツールのバージョンは、以下のコマンドで確認できます。

```bash
python --version
node --version
npm --version
git --version
psql --version
pip show fastapi
pip show uvicorn
pip show sqlalchemy
```

Reactのバージョンは、`frontend/package.json` の `dependencies` を確認します。

---

# 必要なもの

以下のソフトウェアを使用します。

* [Visual Studio Code]
* [Git]
* [Node.js]
* [Python]
* [PostgreSQL]

GitHubを利用するため、GitHubアカウントも必要です。

---

# ディレクトリ構成

最終的なプロジェクト構成は以下を想定しています。

```text
webapp-practice/
├── backend/
│   ├── venv/          # Python仮想環境
│   ├── .env           # データベース接続情報
│   ├── main.py        # FastAPIアプリケーション
│   ├── db.py          # DB接続・セッション管理
│   └── models.py      # DBモデル定義
│
├── frontend/          # Reactアプリケーション
│
└── .gitignore
```

`backend/venv/` と `backend/.env` はGitHubには公開しません。

---

# 1. Gitのインストール

GitHubとの連携やソースコードのバージョン管理に使用します。

[Git公式サイト](https://git-scm.com/install/windows)からGit for Windowsをダウンロードしてインストールします。

インストール後、VS Codeのターミナル（Git Bash）で以下を実行します。

```bash
git --version
```

以下のようにバージョンが表示されればインストール成功です。

```text
git version 2.xx.x
```

---

# 2. VS Code

ソースコードの編集にVisual Studio Codeを使用します。

[Visual Studio Code公式サイト](https://code.visualstudio.com/Download?_exp_download=fb315fc982)からWindows版をダウンロードしてインストールします。

Windowsでは、通常「User Installer」を使用すれば問題ありません。

VS Codeを起動し、

**ターミナル → 新しいターミナル**

からターミナルを開きます。

本READMEでは、Windows上のGit Bashを使用してコマンドを実行します。

---

# 3. Node.jsのインストール

Reactの開発に使用します。

[Node.js公式サイト](https://nodejs.org/en/download)からNode.jsをダウンロードします。

Windowsの場合は、x64向けのインストーラー（.msi）を使用します。

インストール後、VS CodeのGit Bashで以下を実行します。

```bash
node --version
npm --version
```

それぞれバージョンが表示されればOKです。

---

# 4. Pythonのインストール

FastAPIなどのバックエンド開発に使用します。

[Python公式サイト](https://www.python.org/downloads/windows/)からWindows版Pythonをダウンロードします。

Pythonをインストールします。

Windows用インストーラーの最初の画面で、

```text
Add python.exe to PATH
```

にチェックを入れてからインストールします。

インストール後、VS CodeのGit Bashで以下を実行します。

```bash
python --version
```

以下のように表示されればOKです。

```text
Python 3.14.7
```

---

# 5. PostgreSQLのインストール

データベースとしてPostgreSQLを使用します。

[PostgreSQL公式サイト（Windows版）](https://www.postgresql.org/download/windows/)からインストーラーをダウンロードします。

Windows版のインストーラーには、PostgreSQL本体に加えてpgAdminなども含まれています。

インストール時の基本的な設定はデフォルトのままで問題ありません。

途中で設定する`postgres`ユーザーのパスワードは、後でデータベース接続に使用するため、忘れないようにしてください。

## PostgreSQLのPATH設定

PostgreSQLをインストールすると、通常以下の場所に`psql.exe`があります。

```text
C:\Program Files\PostgreSQL\<バージョン>\bin\psql.exe
```

例えばPostgreSQL 18の場合、

```text
C:\Program Files\PostgreSQL\18\bin\psql.exe
```

です。

`psql.exe`が存在することを確認したら、以下のディレクトリをWindowsのPATHに追加します。

```text
C:\Program Files\PostgreSQL\18\bin
```

### PATHへの追加方法

1. Windowsの検索で「環境変数」と検索
2. 「システム環境変数の編集」を開く
3. 「環境変数」をクリック
4. 「ユーザー環境変数」の`Path`を選択
5. 「編集」をクリック
6. 「新規」をクリック
7. PostgreSQLの`bin`ディレクトリを入力
8. 「OK」で閉じる

VS Codeを再起動した後、Git Bashで以下を実行します。

```bash
psql --version
```

以下のように表示されればOKです。

```text
psql (PostgreSQL) 18.6
```

---

# 6. PostgreSQLの準備

## データベースへの接続

Git Bashで以下を実行します。

```bash
psql -U postgres
```

パスワードを求められるので、PostgreSQLのインストール時に設定したパスワードを入力します。

接続に成功すると、以下のようなプロンプトが表示されます。

```text
postgres=#
```

これでPostgreSQLにログインした状態です。

---

## データベースの作成

今回は`testdb`という名前のデータベースを作成します。

```sql
CREATE DATABASE testdb;
```

作成したデータベースを確認します。

```sql
\l
```

一覧の中に`testdb`が存在すればOKです。

---

## PostgreSQLを終了

PostgreSQLの対話型シェルを終了するには、以下を実行します。

```sql
\q
```

---

# 7. Python環境構築

## 仮想環境の作成

`backend`ディレクトリに移動します。

```bash
cd backend
```

Pythonの仮想環境を作成します。

```bash
python -m venv venv
```

作成した仮想環境を有効化します。

```bash
source venv/Scripts/activate
```

ターミナルの先頭に、

```text
(venv)
```

と表示されれば、仮想環境が有効になっています。

例えば、

```text
(venv) user@PC MINGW64 ~/Documents/projects/webapp-practice/backend
```

のようになります。

---

## 必要なPythonパッケージのインストール

仮想環境を有効にした状態で、以下を実行します。

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv
```

各パッケージの役割は以下の通りです。

| パッケージ             | 役割             | 主な用途                 |
| ----------------- | -------------- | -------------------- |
| `fastapi`         | Webフレームワーク     | APIの作成               |
| `uvicorn`         | ASGIサーバ        | FastAPIアプリケーションの起動   |
| `sqlalchemy`      | ORM            | Pythonからデータベースを操作    |
| `psycopg2-binary` | PostgreSQLドライバ | PythonとPostgreSQLの通信 |
| `python-dotenv`   | 環境変数管理         | `.env`から設定値を読み込む     |

---

# 8. SQLAlchemyの設定

## `.env`の作成

`backend`ディレクトリに`.env`ファイルを作成します。

```text
webapp-practice/
└── backend/
    └── .env
```

`.env`には以下を記述します。

```text
DATABASE_URL=postgresql://postgres:<PostgreSQLのパスワード>@localhost:5432/testdb
```

`<PostgreSQLのパスワード>`には、PostgreSQLのインストール時に設定したパスワードを指定します。

例えばパスワードが`example`の場合、

```text
DATABASE_URL=postgresql://postgres:example@localhost:5432/testdb
```

となります。

**実際のパスワードはGitHubに公開しないでください。**

---

## `db.py`の作成

`backend/db.py`を作成します。

```python
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# .envファイルの読み込み
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### `db.py`の役割

このファイルでは、主に以下を行います。

* `.env`からデータベース接続情報を読み込む
* SQLAlchemyのデータベースエンジンを作成する
* DBセッションを作成する
* FastAPIからDBセッションを利用できるようにする

---

# 9. モデル定義

データベースのテーブル構造をPythonのクラスとして定義します。

`backend/models.py`を作成します。

```python
from sqlalchemy import Column, Integer, String

from db import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
```

この`Message`クラスは、PostgreSQLの`messages`テーブルに対応します。

イメージとしては、

```text
Python                         PostgreSQL

Messageクラス       ←→       messagesテーブル

id                  ←→       id
text                ←→       text
```

という関係です。

---

# 10. FastAPIの実装

`backend/main.py`を作成します。

```python
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from db import Base, engine, get_db
from models import Message


# テーブル作成
# 学習・検証用の簡易構成。
# 本格的な開発ではAlembicなどのマイグレーションツールを使用する。
Base.metadata.create_all(bind=engine)


app = FastAPI()


# React（localhost:3000）からのアクセスを許可
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.get("/api/message")
def get_message(db: Session = Depends(get_db)):
    msg = db.query(Message).first()

    if msg:
        return {"message": msg.text}

    new_msg = Message(
        text="Hello from PostgreSQL + SQLAlchemy!"
    )

    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)

    return {"message": new_msg.text}
```

## このAPIで行っていること

`GET /api/message`にアクセスすると、

1. `messages`テーブルからデータを取得
2. データが存在すれば、そのデータを返す
3. データが存在しなければ新しいメッセージを登録
4. 登録したメッセージを返す

という処理を行います。

---

# 11. FastAPIサーバの起動

`backend`ディレクトリにいることを確認します。

```bash
cd backend
```

仮想環境が有効になっていることを確認します。

```text
(venv)
```

その状態で以下を実行します。

```bash
uvicorn main:app --reload --port 8000
```

## コマンドの意味

```text
uvicorn
```

UvicornというASGIサーバを起動します。

```text
main:app
```

`main.py`の中にある`app`というFastAPIアプリケーションを起動します。

```text
--reload
```

Pythonファイルを変更すると、開発サーバを自動的に再起動します。

```text
--port 8000
```

8000番ポートでサーバを起動します。

起動後、以下にアクセスできます。

```text
http://localhost:8000
```

FastAPIが提供するAPIドキュメントは以下です。

```text
http://localhost:8000/docs
```

---

# 12. Reactフロントエンド

## Reactアプリの作成

プロジェクトルートに戻ります。

```bash
cd ..
```

現在位置が以下になることを確認します。

```text
webapp-practice/
```

Reactアプリを作成します。

```bash
npx create-react-app frontend
```

> **注意:** Create React App（CRA）は現在、React公式で非推奨となっています。本プロジェクトでは参考記事に合わせた学習目的で使用しています。新しくReactプロジェクトを作成する場合は、Viteなどの利用も検討してください。

---

## `App.js`の実装

`frontend/src/App.js`を以下のようにします。

```javascript
import { useEffect, useState } from "react";

function App() {
  const [msg, setMsg] = useState("");

  useEffect(() => {
    fetch("http://localhost:8000/api/message")
      .then((res) => res.json())
      .then((data) => setMsg(data.message))
      .catch(() => setMsg("API error"));
  }, []);

  return <h1>{msg}</h1>;
}

export default App;
```

このコードでは、Reactの画面が表示されたときにFastAPIのAPIへリクエストを送信しています。

```text
React
  ↓
GET http://localhost:8000/api/message
  ↓
FastAPI
  ↓
SQLAlchemy
  ↓
PostgreSQL
  ↓
メッセージを取得
  ↓
FastAPI → React
  ↓
画面に表示
```

---

# 13. 動作確認

FastAPIとReactは、それぞれ別のターミナルで起動します。

## ターミナル1：FastAPI

`backend`ディレクトリで、

```bash
uvicorn main:app --reload --port 8000
```

を実行します。

---

## ターミナル2：React

プロジェクトルートから、

```bash
cd frontend
npm start
```

を実行します。

Reactの開発サーバが起動したら、ブラウザで以下を開きます。

```text
http://localhost:3000
```

画面に、

```text
Hello from PostgreSQL + SQLAlchemy!
```

と表示されれば、React → FastAPI → SQLAlchemy → PostgreSQLの接続確認は完了です。

---

# 14. トラブルシューティング

## SQLAlchemyのDLLエラー

環境によっては、以下のようなエラーが発生する場合があります。

```text
ImportError: DLL load failed while importing _immutabledict_cy:
アプリケーション制御ポリシーによってこのファイルがブロックされました。
```

今回のWindows 11環境では、SQLAlchemy `2.1.1`を使用した際にこのエラーが発生しました。

SQLAlchemyのバージョンを確認します。

```bash
pip show sqlalchemy
```

`2.1.1`だった場合、今回動作確認できた`2.0.52`へ変更します。

```bash
pip uninstall sqlalchemy
```

続いて、

```bash
pip install "sqlalchemy==2.0.52"
```

バージョンを確認します。

```bash
python -c "import sqlalchemy; print(sqlalchemy.__version__)"
```

以下のように表示されればOKです。

```text
2.0.52
```

その後、FastAPIを再起動します。

```bash
uvicorn main:app --reload --port 8000
```

### 注意

これは「Python 3.14ではSQLAlchemy 2.1.1が必ず使用できない」という意味ではありません。

今回の環境ではSQLAlchemy 2.1.1の読み込み時にWindows側のDLL読み込みエラーが発生し、SQLAlchemy 2.0.52では正常に動作したため、このプロジェクトでは2.0.52を使用しています。

---

# 15. GitHubへの公開

## 15.1 `.gitignore`を作成する

GitHubに公開する前に、以下のファイルをGitの管理対象から除外します。

プロジェクトルートの`webapp-practice/.gitignore`を作成します。

```gitignore
# Python
__pycache__/
*.pyc

# Python virtual environment
backend/venv/

# Environment variables
backend/.env

# Node.js
frontend/node_modules/

# React build files
frontend/build/

# VS Code
.vscode/
```

特に以下の2つは重要です。

```text
backend/venv/
backend/.env
```

`backend/venv/`には大量のPythonパッケージが入っているため、GitHubにアップロードする必要はありません。

`backend/.env`にはPostgreSQLのパスワードが含まれるため、**絶対にGitHubへ公開しないでください。**

---

## 15.2 `.gitignore`が機能していることを確認

プロジェクトルートで、

```bash
git status
```

を実行します。

`backend/venv/`や`backend/.env`がGitの管理対象として表示されなければOKです。

---

## 15.3 Gitリポジトリを作成

まだGitリポジトリを作成していない場合は、プロジェクトルートで実行します。

```bash
git init
```

現在のブランチを`main`にします。

```bash
git branch -M main
```

---

## 15.4 GitHubでリポジトリを作成

GitHubにログインし、新しいリポジトリを作成します。

リポジトリ名は、

```text
webapp-practice
```

とします。

### 注意

GitHub上でREADMEを自動生成する設定は、今回はOFFにすることをおすすめします。

すでにローカルに`README.md`が存在するためです。

また、`.gitignore`もローカルですでに作成しているので、GitHub側では追加する必要はありません。

---

## 15.5 GitHubリポジトリとローカルを接続

GitHubで作成したリポジトリのURLを使って、以下を実行します。

```bash
git remote add origin <GitHubリポジトリのURL>
```

例えば、

```bash
git remote add origin https://github.com/<ユーザー名>/webapp-practice.git
```

接続先を確認します。

```bash
git remote -v
```

---

## 15.6 ファイルをGitに追加

```bash
git add .
```

追加されるファイルを確認します。

```bash
git status
```

ここで、

```text
backend/.env
backend/venv/
frontend/node_modules/
```

などが表示されていないことを確認してください。

---

## 15.7 最初のコミット

```bash
git commit -m "Initial commit"
```

---

## 15.8 GitHubへpush

```bash
git push -u origin main
```

pushが成功したら、GitHubの`webapp-practice`リポジトリを開きます。

以下のような構成になっていれば成功です。

```text
webapp-practice/
├── backend/
│   ├── main.py
│   ├── db.py
│   └── models.py
├── frontend/
├── .gitignore
└── README.md
```

一方で、以下がGitHub上に存在していないことを必ず確認します。

```text
backend/.env
backend/venv/
frontend/node_modules/
```

---

# まとめ

このプロジェクトでは、以下の構成でWebアプリケーションを開発します。

```text
                    ┌──────────────┐
                    │    React     │
                    │  Frontend    │
                    └──────┬───────┘
                           │
                     HTTP Request
                           │
                           ▼
                    ┌──────────────┐
                    │   FastAPI    │
                    │   Backend    │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  SQLAlchemy  │
                    │     ORM      │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ PostgreSQL   │
                    │  Database    │
                    └──────────────┘
```

GitHubではソースコードを管理し、`.env`や仮想環境などのローカル環境固有のファイルは公開しません。

今後は、この環境をベースとしてAPI、データベース、Reactの画面を追加しながらWebアプリケーションを開発していきます。


参考(https://zenn.dev/sanpi34/articles/cb8b97e4ee3756#%E3%81%AF%E3%81%98%E3%82%81%E3%81%AB)

環境
Windows11
Python 3.14.7
(※ほかに何のバージョンとか書くべき？)

必要なもの
vsCode
Git
Node.js
Python
PostgreSQL

＜環境構築＞

Gitのインストール
GitHubとの連携に必要
公式サイト(https://git-scm.com/?utm_source=chatgpt.com)からインストーラをダウンロード
VSCode
ターミナル→新しいターミナル
git --versionでgit version 2.xx.xと出ればOK

Node.jsのインストール
Reactを動かすために必要
公式サイト(https://nodejs.org/ja?utm_source=chatgpt.com)より、
「Node.js🄬を入手」→「x64」アーキテクチャーで動作する「Windows」用のビルド済みのNode.js🄬も利用できます→「Windowsインストーラー(.msi)」
インストール後、VSCodeのbashターミナルで
node --version
npm --version
それぞれバージョンが表示されればOK

Pythonのインストール
Backend
公式サイト(https://www.python.org/?utm_source=chatgpt.com)からインストーラをダウンロード
インストーラの最初の画面にある
☑ Add python.exe to PATH
にチェックを入れる
インストール後、VSCodeのbashターミナルで
python --version
Python 3.xx.x
と出ればOK

PostgreSQLのインストール
公式サイト(https://www.postgresql.org/download/windows/?utm_source=chatgpt.com)からインストーラをダウンロード
インストーラでの操作は基本的にデフォルトでOK
途中で設定するPasswordは忘れないように注意する
パスを通す
C:\Program Files\PostgreSQL\xx\bin\psql.exeの存在を確認
「システム環境変数の編集」を開く→「環境変数」をクリック→「ユーザー環境変数」からPathを選択→「編集」→「新規」→「C:\Program Files\PostgreSQL\xx\bin」を入力→「OK」で閉じる
VSCodeを再起動後、bashターミナルで
psql --version
psql (PostgreSQL) xx.x
と出ればOK

<ディレクトリ構成>
project-root/
├── backend/      # Python / FastAPI + SQLAlchemy
│   ├── venv/     # 仮想環境
│   ├── main.py
│   ├── db.py
│   └── models.py
└── frontend/     # React アプリ

<PostgreSQLの準備>
データベースの作成をする
PostgreSQLに接続する
bashターミナルで下記コマンドを入力
psql -U postgres
すると、以下のようにパスワードを求められるため入力
Password for user postgres:
パスワードを入力すると接続成功し、次のようなプロンプトになる
postgres=#
これでPostgreSQLにログインした状態
下記コマンドを実行してDBを作成する
今回は「testdb」という名前にする
CREATE DATABASE testdb;
次に、下記コマンドを実行してDBが作成できているかを確認する
\l
「testdb」の行があればOK
\qで対話型シェルを抜ける

<Python環境構築（FastAPI + SQLAlchemy）>
仮想環境作成
backendディレクトリに移動する（cd backend）
下記のコマンドを実行
python -m venv venv
source venv/Scripts/activate
ターミナルに(venv)が表示されるようになればOK

必要なパッケージのインストール
下記コマンドを実行
pip install fastapi uvicorn sqlalchemy psycopg2-binary
パッケージ名	役割	主な用途
fastapi	Web フレームワーク	Python で高速な API サーバを構築するためのフレームワーク。リクエスト処理、ルーティング、バリデーション、レスポンス生成を担当。
uvicorn	ASGI サーバ	FastAPI アプリを動作させる実行サーバ。Node.js でいう npm start のような位置づけ。uvicorn main:app --reload で起動。
sqlalchemy	ORM（Object Relational Mapper）	Python オブジェクトを使ってデータベースを操作するためのライブラリ。SQL を直接書かずにテーブル作成やCRUDが可能。
psycopg2-binary	PostgreSQL ドライバ	Python から PostgreSQL に接続するためのドライバ。SQLAlchemy がこれを通じて実際のDB通信を行う。

<SQLAlchemyの設定>
以下のコマンドを実行してpython-dotenvをインストールする
pip install python-dotenv
backend/.envを作成し、.envの中に
DATABASE_URL=postgresql://postgres:[あなたのPostgreSQLパスワード]@localhost:5432/testdb
と書く
データベース接続とセッション管理を行うファイル
backend/ディレクトリに以下の「db.py」を作成する
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# .envファイルの読み込み
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

.envにはPostgreSQLのパスワードが入るためGitHubに公開してはいけない
project-root/.gitignoreを作成して、以下を追加する
# Python
__pycache__/
*.pyc

# Virtual environment
backend/venv/

# Environment variables
backend/.env

<モデル定義>
データベースのテーブル構造をPythonクラスで定義する
backend/models.py
from sqlalchemy import Column, Integer, String
from db import Base

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)

<FastAPI本体>
APIエンドポイントを定義する
テーブル作成とCORS設定も含まれている
backend/main.py

<FastAPIサーバ起動>
backend/ディレクトリにいる状態で以下のサーバ起動コマンドを実行する
uvicorn main:app --reload --port 8000
ブラウザで http://localhost:8000/api/message にアクセスすると確認できる
※自環境でのトラブルシューティング
ImportError: DLL load failed while importing _immutabledict_cy: アプリケーション制御ポリシーによってこのファイルがブロックされました。
というエラーがでた
sqlalchemyのバージョンを確認(pip show sqlalchemy)したところ、2.1.1であった
これを以下のコマンドで2.0.52にダウングレードするとうまくいった
pip uninstall sqlalchemy
pip install "sqlalchemy==2.0.52"
Python3.14.7との組み合わせの関係？

<Reactフロントエンド>
Reactアプリの作成
プロジェクトルートへ戻りReactアプリを作成する
npx create-react-app frontend

src/App.jsの実装例
import { useEffect, useState } from "react";

function App() {
  const [msg, setMsg] = useState("");

  useEffect(() => {
    fetch("http://localhost:8000/api/message")
      .then((res) => res.json())
      .then((data) => setMsg(data.message))
      .catch(() => setMsg("API error"));
  }, []);

  return <h1>{msg}</h1>;
}

export default App;

サーバーの起動
cd frontend
npm start

ブラウザで http://localhost:3000 を開くと、FastAPI から取得したメッセージが表示される（別ターミナルで「uvicorn main:app --reload --port 8000」を実行してAPIを8000番ポートで起動しておく必要がある）