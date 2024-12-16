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
- インベントリシステム
- アイテムドロップと取得
- 敵キャラクターのリスポーン
- ミニマップ表示
- 体力バーと敵の体力表示

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
- Inventory system
- Item drop and pickup
- Enemy respawn
- Minimap display
- Health bar and enemy health display

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

2. Install dependencies
```sh
pip install -r requirements.txt
```

3. Run the game
```sh
python main.py
```

## プロジェクト構造

```
プロジェクトルート/
├── characters/           # キャラクター関連のアセット
│   ├── Arrow/           # 投射物の画像と設定
│   ├── icons/           # UI用アイコン
│   ├── Enemy/           # 敵キャラクターの画像と設定(追加キャラクターは今後実装予定)
│   ├── Friends/         # プレイヤーキャラクターの画像と設定(追加キャラクターは今後実装予定)
│   └── Zenny/           # ゼニー関連の画像と設定
├── font/                # ゲームで使用するフォント
├── images/              # 一般的な画像アセット
├── maps/                # マップデータ
├── music/               # BGM
├── save/                # セーブデータ
├── sounds/              # 効果音
└── Texture/             # テクスチャデータ
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
- [ ] アイテム合成システムの導入

### 中期目標（2025年〜2026年）
- [ ] マルチプレイヤー機能の実装
- [ ] キャラクターカスタマイズの拡充
- [ ] 新しい敵キャラクターの追加

### 長期目標（2026年〜）
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

バージョン: v0.1.2
