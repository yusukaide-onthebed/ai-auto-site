import os

from google import genai


API_KEY = os.environ["GEMINI_API_KEY"]

client = genai.Client(api_key=API_KEY)

prompt = """
あなたは「AI日報」という日本語Webサイトの編集者です。

今日の記事を1本作成してください。

テーマは「AI・テクノロジー」に関する話題です。

条件：
・日本語で書く
・タイトルを1つ付ける
・本文は500～800文字程度
・読みやすい文章にする
・HTMLとしてそのままサイトに掲載できる形にする
・<html>や<body>は不要
・<article>タグの中だけを出力する
・Markdownは使用しない

以下の形式で出力してください。

<article>
<h2>記事タイトル</h2>
<p>本文</p>
<p>本文</p>
</article>
"""

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)

article = response.text.strip()

# AIがコードブロックを付けてしまった場合に除去
article = article.replace("```html", "")
article = article.replace("```", "")
article = article.strip()

with open("article.html", "w", encoding="utf-8") as f:
    f.write(article)

print("AIが記事を生成しました。")
print(article)
