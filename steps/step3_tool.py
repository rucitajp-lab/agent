"""ステップ3: ツール(道具)を1つ持たせる

Claude 自身は「今の時刻」を知りません。そこで「現在時刻を調べる関数」を
ツールとして渡します。流れは次の3段階です:

    1. ツールの説明書(名前・説明・引数)と一緒に質問を送る
    2. Claude が「このツールをこの引数で使いたい」と返してくる (tool_use)
    3. プログラム側で関数を実行し、結果を返す (tool_result)
       → Claude がその結果を使って最終的な答えを書く

※ Claude はツールを「頼む」だけで、実際に実行するのはこちらのプログラムです。

実行方法:
    export ANTHROPIC_API_KEY="sk-ant-..."
    python steps/step3_tool.py
"""

from datetime import datetime
from zoneinfo import ZoneInfo

import anthropic

client = anthropic.Anthropic()


# --- ツールの中身(普通の Python 関数) ---------------------------------
def get_current_time(timezone: str) -> str:
    """指定したタイムゾーンの現在時刻を返す"""
    try:
        now = datetime.now(ZoneInfo(timezone))
    except Exception:
        return f"エラー: タイムゾーン '{timezone}' が見つかりません"
    return now.strftime("%Y-%m-%d %H:%M:%S (%A)")


# --- ツールの説明書(Claude に渡す) -------------------------------------
# Claude はこの説明を読んで「いつ・どう使うか」を判断する。説明文は丁寧に書くのがコツ。
tools = [
    {
        "name": "get_current_time",
        "description": "指定したタイムゾーンの現在の日付・時刻・曜日を取得する。今の時間や今日の日付を答えるときに使う。",
        "input_schema": {
            "type": "object",
            "properties": {
                "timezone": {
                    "type": "string",
                    "description": "IANA形式のタイムゾーン名。例: Asia/Tokyo, America/New_York",
                },
            },
            "required": ["timezone"],
        },
    }
]

# ツール名 → 実際の関数 の対応表
TOOL_FUNCTIONS = {
    "get_current_time": get_current_time,
}

question = "東京とニューヨークは今それぞれ何時？"
print(f"あなた> {question}\n")
messages = [{"role": "user", "content": question}]

# --- 1回目: 質問 + ツールの説明書を送る --------------------------------
response = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=16000,
    tools=tools,
    messages=messages,
)
print(f"[1回目の stop_reason: {response.stop_reason}]")  # ツールを使いたいときは "tool_use"

# Claude の返事(ツール依頼を含む)を履歴に追加
messages.append({"role": "assistant", "content": response.content})

# --- 2. Claude の依頼どおりにツールを実行する ----------------------------
tool_results = []
for block in response.content:
    if block.type == "tool_use":
        print(f"  🔧 Claude の依頼: {block.name}({block.input})")
        result = TOOL_FUNCTIONS[block.name](**block.input)
        print(f"     → 実行結果: {result}")
        tool_results.append({
            "type": "tool_result",
            "tool_use_id": block.id,  # どの依頼に対する結果かを ID で対応づける
            "content": result,
        })

if not tool_results:
    # ツールを使わずに答えた場合はそのまま表示して終わり
    for block in response.content:
        if block.type == "text":
            print(f"Claude> {block.text}")
    raise SystemExit

# 結果は「user」の発言として返す(複数あれば1つのメッセージにまとめる)
messages.append({"role": "user", "content": tool_results})

# --- 3. 2回目: ツールの結果を踏まえて答えてもらう ------------------------
response = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=16000,
    tools=tools,
    messages=messages,
)
print(f"\n[2回目の stop_reason: {response.stop_reason}]")  # 答え終わったら "end_turn"

for block in response.content:
    if block.type == "text":
        print(f"Claude> {block.text}")
