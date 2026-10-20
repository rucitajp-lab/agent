# 自作AIエージェント

Claude API (Python) を使って、AIエージェントを一から少しずつ作っていくプロジェクトです。

## ロードマップ

| ステップ | 内容 | ファイル |
|---|---|---|
| 1 | Claude に1回話しかける | `steps/step1_hello.py` |
| 2 | 会話を覚えるチャット（履歴の管理） | `steps/step2_chat.py` |
| 3 | ツール（道具）を1つ持たせる | |
| 4 | エージェントループ：自分で考えてツールを繰り返し使う | |
| 5 | ツールを増やす・安全対策（確認、上限など） | |

## セットアップ

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."   # https://console.anthropic.com で発行
python steps/step1_hello.py
```
