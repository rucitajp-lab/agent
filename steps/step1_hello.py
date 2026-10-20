"""ステップ1: Claude に1回だけ話しかける

AIエージェントの一番小さな部品は「LLMに1回メッセージを送って返事をもらう」ことです。
ここから少しずつ「会話」「道具(ツール)」「自律ループ」を足していきます。

実行方法:
    export ANTHROPIC_API_KEY="sk-ant-..."
    python steps/step1_hello.py
"""

import anthropic

# 環境変数 ANTHROPIC_API_KEY を自動で読み込みます
client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-5-5",  # 使うモデル
    max_tokens=16000,         # 返事の最大トークン数
    system="あなたは親切なアシスタントです。日本語で簡潔に答えてください。",  # キャラ設定・ルール
    messages=[
        {"role": "user", "content": "AIエージェントとは何か、一言で教えて"},
    ],
)

# 返事は「ブロック」のリストで返ってくる。テキストのブロックだけ表示する
for block in response.content:
    if block.type == "text":
        print(block.text)

# 何トークン使ったか(=料金の目安)
print(f"\n[使用トークン] 入力: {response.usage.input_tokens} / 出力: {response.usage.output_tokens}")
