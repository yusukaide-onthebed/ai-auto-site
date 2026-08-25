import os

from google import genai


API_KEY = os.environ["GEMINI_API_KEY"]

client = genai.Client(api_key=API_KEY)

prompt = """
あなたは「AI日報」という日本語Webサイトの編集者です。

今日のサイトに掲載する記事を1本作成してください。

テーマは「AI・テクノロジー」に関する話題です。
毎回、できるだけ違うテーマを選んでください。

条件：
・日本語で書く
・タイトルを1つ付ける
・本文は500～800文字程度
・読みやすい文章にする
・HTMLとしてそのまま掲載できる形にする
・<html>や<body>は不要
・<article>タグの中だけを出力する
・Markdownは使用しない
・日付は記事内に書かない

形式：

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


# AIが生成した記事を保存
with open("article.html", "w", encoding="utf-8") as f:
    f.write(article)


# index.htmlを読み込む
with open("index.html", "r", encoding="utf-8") as f:
    index = f.read()


start_marker = "<!-- AI_ARTICLE_START -->"
end_marker = "<!-- AI_ARTICLE_END -->"


if start_marker not in index or end_marker not in index:
    raise Exception("index.htmlに記事の目印が見つかりません。")


start = index.index(start_marker) + len(start_marker)
end = index.index(end_marker)


# AI記事に置き換える
new_index = (
    index[:start]
    + "\n\n"
    + article
    + "\n\n    "
    + index[end:]
)


# index.htmlを更新
with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_index)


print("AIが記事を生成しました。")
print("index.htmlを更新しました。")
print(article)
