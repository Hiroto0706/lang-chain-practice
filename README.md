LangChainに詳しくなりたい！

# 学んだこと

## ice_breaker
- 基本的なLangChainを使った実装を学んだ。llmインスタンスの作成、chainの方法、SystemTemplateの定義の仕方などを学んだ。
- linkedinのURLをスクレイピングし、その値をLangChainを用いてLLMに渡して、人物の要約をしてもらう方法
- 開発を通してPythonのvenvの使い方を学んだ。
  [こちら](https://monta-database.notion.site/python-langchain-193cca65093280dabe9af4928e4bd3f2)のリンクで手順をまとめた
- ToolsとAgentについて学んだ。
  [こちら](https://zenn.dev/yuta_enginner/articles/c35768a52c7ba2)のZennの記事がめちゃくちゃわかりやすい。
  Agentは1次下請けでToolsが2次下請け。1次下請けであるAgentが仕事を受注（inputの受け取り）し、2次下請けであるToolsに渡す（仕事の依頼）という流れがめちゃくちゃわかりやすい。
- OutputParserを使ってLLMの生成する内容をparseする方法を学んだ。
  `PydanticOutputParser(pydantic_object=Summary)`を使ってパースしたいクラスをpydanticc_objectに渡すことで、LLMに『あ〜、このクラスの形でアウトプット作ってくれい〜』と伝えることができる。
- LangSmithの使い方について学んだ。LANGCHAIN_API_KEY, LANGCHAIN_TRACING_V2=true, LANGCHAIN_PROJECTさえ設定すれば、LangSmithのログに勝手にLLMの生成結果が反映されるようになる。
  LangSmithのログには、input, 開始時刻, Latency, トークン数, 実行結果などが表示される。また、ログをクリックすればその詳細前追うことができる。エラーハンドリングにはめちゃくちゃ便利だなという印象を持った。
  ![alt text](images/image_1.png)
  また、[こちら](https://zenn.dev/umi_mori/books/prompt-engineer/viewer/langsmith#2.-llm%E3%81%AE%E5%87%BA%E5%8A%9B%E7%B5%90%E6%9E%9C%E3%81%AE%E3%83%87%E3%83%BC%E3%82%BF%E3%82%BB%E3%83%83%E3%83%88%E5%8C%96%EF%BC%88%E3%83%87%E3%83%BC%E3%82%BF%E5%8F%8E%E9%9B%86%E6%A9%9F%E8%83%BD%EF%BC%89)のリンクを見てみた感じ、LangSmithには出力結果をデータセットとして保存することができるっぽい。そして、登録したデータセットを用いてモデルの評価などができる。（すごい）
  このモデル評価機能を使えば、モデルが求めるクオリティに近いかどうかがわかるからかなり使えそうな印象を持った。