# RPGゲームプロジェクト

## 概要

このプロジェクトは、PythonとPygameを使用して開発されたRPGゲームエンジンです。
プレイヤーは独自のキャラクターを操作し、豊かなストーリーラインに沿って冒険を進めることができます。

### 主な機能
- エピソードベースのストーリー展開
- リアルタイム戦闘システム
- カスタマイズ可能なキャラクター
- セーブ＆ロード機能
- マップエディタ機能

## 必要環境

- Python 3.8以上
- Pygame 2.0.0以上
- 推奨解像度: 1920x1080

## インストールと実行

1. リポジトリのクローン
```sh
git clone https://github.com/paraccoli/pygame.git
cd pygame
```

2. 依存ライブラリのインストール
```sh
pip install -r requirements.txt
```

3. ゲームの起動
```sh
python main.py
```

# RPG Game Project

## Overview

This project is an RPG game engine developed using Python and Pygame.
Players can control their own characters and progress through a rich storyline.

### Main Features
- Episode-based story progression
- Real-time combat system
- Customizable characters
- Save & Load functionality
- Map editor feature

## Requirements

- Python 3.8 or higher
- Pygame 2.0.0 or higher
- Recommended resolution: 1920x1080

## Installation and Execution

1. Clone the repository
```sh
git clone https://github.com/paraccoli/pygame.git
cd pygame
```


## プロジェクト構造

```
プロジェクトルート/
├── characters/           # キャラクター関連のアセット
│   ├── Arrow/           # 投射物の画像と設定
│   ├── icons/           # UI用アイコン
│   ├── Orc/            # 敵キャラクターの画像と設定
│   └── Soldier/        # プレイヤーキャラクターの画像と設定
├── font/                # ゲームで使用するフォント
├── images/             # 一般的な画像アセット
├── maps/               # マップデータ
├── music/              # BGM
├── save/               # セーブデータ
├── sounds/             # 効果音
└── Texture/            # テクスチャデータ
```

### コアファイル
| ファイル名 | 説明 |
|------------|------|
| main.py | ゲームのエントリーポイントとメインループ |
| config.py | 環境設定と定数の定義 |
| game_logic.py | コアゲームロジックの実装 |
| dialogue_manager.py | 会話システムの管理 |
| field_create.py | マップエディタツール |
| save_manager.py | セーブデータの管理システム |

### エピソードファイル
- episode0.py: プロローグ
- episode0_0.py: チュートリアル
- episode1.py: メインストーリー第1章

## 開発ロードマップ

### 短期目標（〜2025年第2四半期）
- [ ] 戦闘システムの改善
- [ ] 新規エピソード2件の追加
- [ ] UIの改善

### 中期目標（20xx～）
- [ ] マルチプレイヤー機能の実装
- [ ] キャラクターカスタマイズの拡充
- [ ] アイテム合成システムの導入

### 長期目標（20xx年〜）
- [ ] オンラインランキングシステム
- [ ] モバイルアプリ版のリリース
- [ ] コミュニティ作成コンテンツのサポート

## 貢献について

プロジェクトへの貢献を歓迎します。以下の方法で貢献できます：

1. イシューの報告
2. プルリクエストの提出
3. ドキュメントの改善
4. 新規アセットの提供


## 開発者向け情報


## 連絡先
X：[パラッコリー🥦](https://x.com/Paraccoli)
Gmail：m.mirim1357@gmail.com

---
最終更新日: 2024年11月22日
