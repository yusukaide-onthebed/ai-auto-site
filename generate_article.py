import os
import json
import urllib.request

API_KEY = os.environ["GEMINI_API_KEY"]

url = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-2.5-flash:generateContent"
)

prompt = """
あなたは「AI日報」という日本語Webサイトの編集者です。

今日の記事を1本作成してください。

テーマは「AI・テクノロジー」に関する一般的な話題です。

条件：
・日本語で書く
・タイトルを1つ付ける
・本文は500～800文字程度
・読みやすい文章にする
・HTMLとしてそのままサイトに掲載できる形にする
・<html>や<body>は不要
・<article>タグの中だけを出力する
・Markdownは使用しない

例：
<article>
<h2>記事タイトル</h2>
<p>本文……</p>
<p>本文……</p>
</article>
"""

data = {
    "contents": [
        {
            "parts": [
                {
                    "text": prompt
                }
            ]
        }
    ]
}

request = urllib.request.Request(
    url,
    data=json.dumps(data).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    },
    method="POST"
)

try:
    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))

    article = result["candidates"][0]["content"]["parts"][0]["text"]

    article = article.replace("```html", "").replace("```", "").strip()

    with open("article.html", "w", encoding="utf-8") as f:
        f.write(article)

    print("AIが記事を生成しました。")

except Exception as e:
    print("Gemini APIでエラーが発生しました。")
    print(e)
    raise
