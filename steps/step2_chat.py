"""ステップ2: 会話を覚えるチャット

LLM 自体は前の会話を覚えていません。毎回「これまでの会話すべて」を
messages に入れて送ることで、会話が続いているように見せています。
この「履歴(history)の管理」が、エージェントの記憶の土台になります。

実行方法:
    export ANTHROPIC_API_KEY="sk-ant-..."
    python steps/step2_chat.py
    (終了するには「exit」と入力するか Ctrl+C)
"""

import anthropic

client = anthropic.Anthropic()

SYSTEM = "あなたは親切なアシスタントです。日本語で簡潔に答えてください。"

# 会話の履歴。ここに user と assistant の発言を交互に積み上げていく
history = []

print("チャットを始めます。終了するには exit と入力してください。\n")

while True:
    user_input = input("あなた> ").strip()
    if user_input in ("exit", "quit"):
        break
    if not user_input:
        continue

    # 1. ユーザーの発言を履歴に追加
    history.append({"role": "user", "content": user_input})

    # 2. 履歴をまるごと送る
    response = client.messages.create(
        model="claude-opus-5-5",
        max_tokens=16000,
        system=SYSTEM,
        messages=history,
    )

    # 3. Claude の返事も履歴に追加する
    #    テキストだけでなく response.content をそのまま入れるのがポイント。
    #    (返事には考えた過程などテキスト以外のブロックも含まれ、それも次回に必要)
    history.append({"role": "assistant", "content": response.content})

    for block in response.content:
        if block.type == "text":
            print(f"Claude> {block.text}")

    # 履歴が増えるほど毎回の入力トークン(=料金)も増えていくのが分かる
    print(f"  [入力: {response.usage.input_tokens} / 出力: {response.usage.output_tokens} トークン]\n")
