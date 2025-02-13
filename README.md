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

### まとめ
ice_breakerでは、LangChainではざっくりとこんなことができるよ〜っていう概要を学んだ。LangChainを動かすためには、PromptTemplateの作成、LLMインスタンスの作成、Chainを組み合わせることで、LLMを使ったアプリの構築ができるよってことを学んだ。
その他にも、Agentを使ってLLMが自ら思考して、URLを取得するといったアクションを起こせるということを学んだ。Agentはかなり衝撃的だった。Agentを使うことで、元から定義してある関数が必要になるかどうかを考えて、必要に応じてその関数を実行し、必要なっ情報を取得するというのはかなり便利だし、使い方によっては色々なことができそうだなという印象を持った。

LangChainの基本的な使い方だけでなく、TwitterやLinkedInのスクレイピングの方法も学んだ。Twitterの公式のAPIなどを用いて、SNSからデータを取得する方法も学んだ。お金はかかるが、これを使いこなせばかなり面白いアプリを作れそうだなという印書を持った。

最後はLangSmithの使い方を学んだ。個人的に、LLMのバグの確認やどんな内容を生成しているのかを知りたい場合は必須で必要なサービスだなという印象を持った。レイテンシー、インプット、生成したトークン、料金とかは開発していてめっちゃ重要な情報だと思うので、LangSmithはLLMアプリ開発に必要不可欠だなという印象を持った。

## ReAct Agent
- 