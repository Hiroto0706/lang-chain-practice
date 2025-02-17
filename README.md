LangChain に詳しくなりたい！

Notion で学習管理してます。

https://monta-database.notion.site/AI-Qiita-167cca650932800481a5efff0880eb56

# 学んだこと

## ice_breaker

- 基本的な LangChain を使った実装を学んだ。llm インスタンスの作成、chain の方法、SystemTemplate の定義の仕方などを学んだ。
- linkedin の URL をスクレイピングし、その値を LangChain を用いて LLM に渡して、人物の要約をしてもらう方法
- 開発を通して Python の venv の使い方を学んだ。
  [こちら](https://monta-database.notion.site/python-langchain-193cca65093280dabe9af4928e4bd3f2)のリンクで手順をまとめた
- Tools と Agent について学んだ。
  [こちら](https://zenn.dev/yuta_enginner/articles/c35768a52c7ba2)の Zenn の記事がめちゃくちゃわかりやすい。
  Agent は 1 次下請けで Tools が 2 次下請け。1 次下請けである Agent が仕事を受注（input の受け取り）し、2 次下請けである Tools に渡す（仕事の依頼）という流れがめちゃくちゃわかりやすい。
- ReAct Agent について学んだ。ReAct Agent とは、Reasoning と Action を掛け合わせた言葉で、推論と試行って意味だと思う。つまり、その都度推論を行い、必要であればアクションを起こす。めちゃくちゃ賢いやつってこと。
  上に書いたように、Reasoning が一次下請けで、設計図を作成し、アクションが必要になれば二次下請けに設計図を渡してアクションを起こさせるって感じ。それが LLM でできるのが ReActAgent っていう理解で良さそう。
- OutputParser を使って LLM の生成する内容を parse する方法を学んだ。
  `PydanticOutputParser(pydantic_object=Summary)`を使ってパースしたいクラスを pydanticc_object に渡すことで、LLM に『あ〜、このクラスの形でアウトプット作ってくれい〜』と伝えることができる。
- LangSmith の使い方について学んだ。LANGCHAIN_API_KEY, LANGCHAIN_TRACING_V2=true, LANGCHAIN_PROJECT さえ設定すれば、LangSmith のログに勝手に LLM の生成結果が反映されるようになる。
  LangSmith のログには、input, 開始時刻, Latency, トークン数, 実行結果などが表示される。また、ログをクリックすればその詳細前追うことができる。エラーハンドリングにはめちゃくちゃ便利だなという印象を持った。
  ![alt text](images/image_1.png)
  また、[こちら](https://zenn.dev/umi_mori/books/prompt-engineer/viewer/langsmith#2.-llm%E3%81%AE%E5%87%BA%E5%8A%9B%E7%B5%90%E6%9E%9C%E3%81%AE%E3%83%87%E3%83%BC%E3%82%BF%E3%82%BB%E3%83%83%E3%83%88%E5%8C%96%EF%BC%88%E3%83%87%E3%83%BC%E3%82%BF%E5%8F%8E%E9%9B%86%E6%A9%9F%E8%83%BD%EF%BC%89)のリンクを見てみた感じ、LangSmith には出力結果をデータセットとして保存することができるっぽい。そして、登録したデータセットを用いてモデルの評価などができる。（すごい）
  このモデル評価機能を使えば、モデルが求めるクオリティに近いかどうかがわかるからかなり使えそうな印象を持った。

### まとめ

ice_breaker では、LangChain ではざっくりとこんなことができるよ〜っていう概要を学んだ。LangChain を動かすためには、PromptTemplate の作成、LLM インスタンスの作成、Chain を組み合わせることで、LLM を使ったアプリの構築ができるよってことを学んだ。
その他にも、Agent を使って LLM が自ら思考して、URL を取得するといったアクションを起こせるということを学んだ。Agent はかなり衝撃的だった。Agent を使うことで、元から定義してある関数が必要になるかどうかを考えて、必要に応じてその関数を実行し、必要なっ情報を取得するというのはかなり便利だし、使い方によっては色々なことができそうだなという印象を持った。

LangChain の基本的な使い方だけでなく、Twitter や LinkedIn のスクレイピングの方法も学んだ。Twitter の公式の API などを用いて、SNS からデータを取得する方法も学んだ。お金はかかるが、これを使いこなせばかなり面白いアプリを作れそうだなという印書を持った。

最後は LangSmith の使い方を学んだ。個人的に、LLM のバグの確認やどんな内容を生成しているのかを知りたい場合は必須で必要なサービスだなという印象を持った。レイテンシー、インプット、生成したトークン、料金とかは開発していてめっちゃ重要な情報だと思うので、LangSmith は LLM アプリ開発に必要不可欠だなという印象を持った。

## ReAct Agent

- ReAct Agent は ChainOfThought という推論（Reasoning）と行動（Action）を繰り返すことで優れた結果を生成するための手法？のようなもの
  ReActAgent には、Tool というものが与えられる。Agent はこの Tool を用いて「ゴールを達成するためにはどのようなアクションを取る必要があるか？」を考える。

  例えば、Tool として calculate という関数が渡されているとする。この関数は受け取った値の計算結果を返す関数。例：2+3 を受け取ったら 5 を返す

  Tool としてこの関数を渡せば、Agent に 1 個 100 円のリンゴを 5 個書いました。5 個買うと 10%の割引になります。この時、最終的な金額はいくらになるか？という質問をしたとする。

  すると、Agent は以下のように施行する。

  1. 1 個 100 円のリンゴが 5 個ということは 100\*5 で 500 円だ！
  2. 5 個買うと 10％の割引だ。つまり、500\*0.1=50 円の割引になるな。
  3. 最終的な金額は 500-50 を計算すれば答えがもとまるな
  4. tools として calculate という計算を行う関数が渡されているからこれを使おう
  5. calculate に 500 - 50 を渡す
  6. 450 が返ってくる。
  7. 答えは 450 円だ！！

  このように、推論と行動と Tool を使いこなすことで最終的な結論を導き出すのが ReActAgent である。

- callback とは、特定のイベントの時に呼び出されるハンドラーのこと。JS でいう eventListener みたいな印象を持った。
  以下のコードだと、llm の推論がスタートした時と終了した時にログを吐き出す処理が実行される。

  ```python
  class AgentCallbackHandler(BaseCallbackHandler):
    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        print(f"***Prompt to LLM was:***\n{prompts[0]}")
        print("*********")

    def on_llm_end(
            self, response: LLMResult, **kwargs: Any
    ) -> Any:
        print(f"***LLM Response:***\n{response.generations[0][0].text}")
        print("*********")
  ```

  基本的な callback の使い方としては、スタート時にはログを吐き出したり初期化に関する処理を実行して、エンド時にはシャットダウン処理を実行したりするのがいいのかなという印象を持った。

  ローカル開発の時にこの機能はめちゃくちゃ便利やなって思った。積極的に使っていこう。

  <details>
  <summary>実行結果</summary>

  ```
  ***Prompt to LLM was:***
  Human:
      Answer the following questions as best you can. You have access to the following tools:

      get_text_length(text: str) -> int - Returns the length of a text by characters

      Use the following format:

      Question: the input question you must answer
      Thought: you should always think about what to do
      Action: the action to take, should be one of [get_text_length]
      Action Input: the input to the action
      Observation: the result of the action
      ... (this Thought/Action/Action Input/Observation can repeat N times)
      Thought: I now know the final answer
      Final Answer: the final answer to the original input question

      Begin!

      Question: What is the length in charaters of the text 吉田万段打 ?
      Thought:

  *********
  ***LLM Response:***
  I need to determine the length of the given text in characters.
      Action: get_text_length
      Action Input: "吉田万段打"
  *********
  tool='get_text_length' tool_input='吉田万段打' log='I need to determine the length of the given text in characters.\n    Action: get_text_length\n    Action Input: "吉田万段打"'
  get_text_length enter with text='吉田万段打'
  observation=5
  ***Prompt to LLM was:***
  Human:
      Answer the following questions as best you can. You have access to the following tools:

      get_text_length(text: str) -> int - Returns the length of a text by characters

      Use the following format:

      Question: the input question you must answer
      Thought: you should always think about what to do
      Action: the action to take, should be one of [get_text_length]
      Action Input: the input to the action
      Observation: the result of the action
      ... (this Thought/Action/Action Input/Observation can repeat N times)
      Thought: I now know the final answer
      Final Answer: the final answer to the original input question

      Begin!

      Question: What is the length in charaters of the text 吉田万段打?
      Thought: I need to determine the length of the given text in characters.
      Action: get_text_length
      Action Input: "吉田万段打"
  Observation: 5
  Thought:
  *********
  ***LLM Response:***
  I now know the final answer: 5

  Final Answer: 5 characters
  *********
  return_values={'output': '5 characters'} log='I now know the final answer: 5\n\nFinal Answer: 5 characters'
  {'output': '5 characters'}
  ```

  </details>

### ChatGPT による解説

<details>
<summary>ReAct Agentとは？</summary>

LangChain における**ReAct Agent**は、**Reasoning（推論）**と**Acting（行動）**を組み合わせたエージェントで、言語モデルが「チェーン・オブ・ソート（chain-of-thought）」の形式で内部推論を行いつつ、必要に応じて外部ツールを呼び出す仕組みです。以下、ステップ・バイ・ステップでその仕組みと具体例を解説します。

---

## 1. ReAct Agent の基本概念

- **Reasoning（推論）:**  
  問題に対して、モデルが自らの思考過程（chain-of-thought）をテキストとして展開します。これにより、どのように問題を解決しようとしているかが可視化され、複雑な問題にも対応できるようになります。

- **Acting（行動）:**  
  推論の過程で、外部のツール（例：計算機、検索エンジン、データベースなど）を呼び出すべきと判断した場合、モデルは「Action（行動）」の指示を出します。これにより、単に言語生成するだけでなく、実際の計算や情報取得といった外部処理を統合できます。

---

## 2. ReAct Agent の動作の流れ

1. **ユーザークエリの受信:**  
   ユーザーから問題が与えられます（例：数値計算や複雑な推論問題）。

2. **内部推論の実行:**  
   言語モデルは、与えられた問題に対して「思考（Thought）」を展開します。ここで、どのように問題を分解し、解決に向けた手順を考えるかを文章化します。

3. **外部ツールの呼び出し:**  
   推論の中で、例えば計算が必要な場合など、外部ツールを使うべきと判断すると、モデルは「Action: ツール名, Input: 入力内容」という形式で命令を出します。

4. **ツールの実行と結果の取得:**  
   エージェントは指定されたツールを呼び出し、その結果を受け取ります。

5. **最終回答の生成:**  
   取得したツールの結果を踏まえ、エージェントは再度推論を進め、最終的な回答を生成します。

---

## 3. 具体例：計算問題への適用

### 問題設定

たとえば、以下のような計算問題を解くとします。

> **問題:** 「3 つの商品がそれぞれ 20 ドルで販売されています。全体に 10%の割引が適用される場合、最終的な金額はいくらになりますか？」

### エージェントの動作例

1. **思考（Thought）の展開:**  
   モデルは以下のように内部で考えます。

   - 「各商品の価格は 20 ドルで、3 つで合計 60 ドルになる。  
     割引は 10%なので、60 ドルの 10%は 6 ドルになる。  
     よって、最終的な金額は 60 ドル - 6 ドル = 54 ドルとなる。」

2. **行動（Action）の指示:**  
   モデルは計算を確実に行うために、計算ツールを呼び出すことにします。  
   例えば、以下のような命令を出すかもしれません。

   ```
   Action: Calculator, Input: "60 * 0.9"
   ```

   ※ここで、60 ドルに 0.9（=1-0.1）を掛けることで、割引後の金額を計算しています。

3. **ツールの実行と結果の取得:**  
   計算ツールが呼ばれ、計算結果として「54」という数字が返ってきます。

4. **最終回答の生成:**  
   取得した結果を元に、エージェントは最終回答として「最終的な金額は 54 ドルです」と回答します。

---

## 4. LangChain での実装例

以下は、Python を使って LangChain の ReAct Agent を利用するサンプルコードです。

```python
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.llms import OpenAI  # 適宜、あなたのLLMに置き換えてください

# 計算用のツール関数の定義
def calculator(input_text: str) -> str:
    try:
        # evalは単純な計算用（安全性に注意）
        result = eval(input_text)
        return str(result)
    except Exception as e:
        return f"計算エラー: {str(e)}"

# ツールの設定
calculator_tool = Tool(
    name="Calculator",
    func=calculator,
    description="算術計算を行うためのツール。計算式を入力として受け取り、結果を返す。"
)

# LLMの初期化（ここではOpenAIのLLMを使用）
llm = OpenAI(temperature=0)

# ReAct Agentの初期化
agent = initialize_agent(
    tools=[calculator_tool],
    llm=llm,
    agent=AgentType.REACT,  # ReAct Agentの指定
    verbose=True  # 詳細なログを表示
)

# 問題の実行
query = "3つの商品がそれぞれ20ドルで販売されています。全体に10%の割引が適用される場合、最終的な金額はいくらになりますか？"
result = agent.run(query)
print("最終回答:", result)
```

### このコードの流れ

1. **ツールの定義:**

   - `calculator`関数を定義し、計算を実行します。
   - `Tool`オブジェクトとして`calculator_tool`を作成します。

2. **エージェントの初期化:**

   - LangChain の`initialize_agent`を使って、ReAct Agent を生成します。
   - ツールとして`calculator_tool`を渡し、LLM として OpenAI のモデルを利用します。

3. **クエリの実行:**
   - 指定したクエリを`agent.run(query)`で実行すると、エージェントが内部で推論（chain-of-thought）を行い、必要に応じて`calculator`ツールを呼び出して回答を導き出します。

---

## 5. まとめ

- **ReAct Agent**は、言語モデルが内部で**思考（推論）**と**外部行動（ツール呼び出し）**を組み合わせて問題を解決する仕組みです。
- LangChain では、`AgentType.REACT`として簡単に ReAct Agent を初期化でき、外部ツールとの連携もシームレスに行えます。
- このアプローチにより、複雑な問題や計算、情報検索などが必要なタスクに対して、柔軟かつ透明な解決プロセスを実現できます。

以上が、LangChain における ReAct Agent の詳細な解説と具体例になります。

</details>

<details><summary>initialize_agent()とcreate_react_agent()のちがい</summary>
`initialize_agent`と`create_react_agent()`は、どちらもReActエージェントを構築するための関数ですが、主に以下の点で違いがあります。

---

### 1. 抽象度と汎用性

- **initialize_agent:**

  - **高レベルのファクトリ関数**  
    LangChain のエージェント全般を初期化するための汎用的なインターフェースです。
  - **多様なエージェントタイプに対応**  
    `AgentType.REACT`やその他のエージェントタイプ（例：ゼロショット ReAct、ツール利用型など）をパラメータで指定でき、内部で必要なコンポーネント（ツール管理、エージェント実行ロジックなど）を自動で組み立てます。

- **create_react_agent():**
  - **低レベル・専用の関数**  
    名前の通り、ReAct エージェント専用に構築されるエージェントのコア部分（内部推論チェーンなど）を作成するための関数です。
  - **細かなカスタマイズ向け**  
    より細かい制御が必要な場合や、内部のチェーン・オブ・ソート（chain-of-thought）の設定などを直接扱いたい場合に使われることが多いです。

---

### 2. 使用方法とカスタマイズの容易さ

- **initialize_agent:**

  - **簡単に使える**  
    ツールのリスト、LLM、エージェントタイプ（たとえば`AgentType.REACT`）などを渡すだけで、エージェント実行に必要なすべての要素が自動的にセットアップされます。
  - **エージェント実行（AgentExecutor）を返す**  
    そのため、ユーザーはすぐにクエリを与えて対話的に利用することができます。

- **create_react_agent():**
  - **より低レベルの構築**  
    ReAct エージェントの内部構造（たとえば、どのように「思考」を展開するか、どのタイミングでツールを呼び出すか）を直接定義・調整できます。
  - **高度なカスタマイズに適する**  
    デフォルトの動作では満足できない場合や、独自のチェーンやプロンプト設計を行いたい場合に利用されることが多いです。

---

### 3. どちらを選ぶべきか？

- **汎用性・簡便性を求める場合:**  
  `initialize_agent`を使うと、エージェントの初期設定やツール連携、実行ロジックなどを自動でまとめてくれるため、すぐに利用を開始できます。

- **詳細な内部動作やカスタマイズが必要な場合:**  
  ReAct エージェントの内部プロセスを直接制御したい場合、`create_react_agent()`を使ってエージェントのコア部分を作成し、必要に応じて自分でラッピングや実行ロジックを追加する方法が適しています。

---

### まとめ

- **initialize_agent:** 高レベルで汎用的なエージェント初期化関数。多くのエージェントタイプに対応しており、セットアップが容易で即座に実行可能なエージェント（AgentExecutor）を返します。
- **create_react_agent():** ReAct エージェント専用の低レベル関数。内部推論のチェーンやプロンプトなどを詳細にカスタマイズしたい場合に適しており、柔軟な設定が可能です。

このように、用途や必要なカスタマイズレベルに応じて使い分けると良いでしょう。

</details>

<details><summary>Chain Of Thoughtについて</summary>
**Chain-of-Thought（CoT）**とは、言語モデルが問題を解決する際に内部で展開する、一連の推論プロセスのことを指します。つまり、最終的な回答に至るまでの思考の流れや中間計算、論理的な推論ステップを文章として表現したものです。

ReActAgent の文脈では、**Chain-of-Thought**は以下のように利用されます：

1. **内部推論:**  
   エージェントはユーザーからのクエリを受け取ると、まず内部で「思考（Thought）」を展開します。このプロセスで、問題をどのように解くか、どのツールをいつ呼び出すかなどの推論が行われます。
2. **外部行動との連携:**  
   思考の過程で、例えば数値計算が必要だと判断した場合、Chain-of-Thought 内の一部で「計算ツールを呼び出す」というアクション指示が含まれ、実際にツールが動かされ、その結果が Chain-of-Thought にフィードバックされます。

3. **透明性とデバッグ:**  
   Chain-of-Thought は、エージェントがどのような推論を経て最終回答に至ったかを理解するために、デバッグや改善時に役立ちます（ただし、実際の利用時には内部で隠蔽される場合もあります）。

---

### 具体例での説明

例えば、次の問題を考えてみましょう：

> **問題:** 「3 つの商品がそれぞれ 20 ドルで販売されています。全体に 10%の割引が適用される場合、最終的な金額はいくらになりますか？」

ReActAgent がこの問題に対してどのように Chain-of-Thought を展開するか、以下のステップで説明します。

1. **問題の理解と初期思考:**  
   エージェントはまず、問題の内容を理解します。

   ```
   Thought: 各商品は20ドルで、3つあるので合計は20ドル * 3 = 60ドルになる。
   ```

2. **割引の計算:**  
   次に、10%の割引が適用されるので、その計算を考えます。

   ```
   Thought: 10%割引は、全体の10%を減じることを意味する。10%は0.1なので、60ドルの0.1は6ドルである。
   ```

3. **最終金額の導出:**  
   最終的な金額を算出します。

   ```
   Thought: 割引後の金額は、60ドル - 6ドル = 54ドルとなる。
   ```

4. **ツールの利用（必要に応じて）:**  
   エージェントは計算結果を正確に得るために、外部の計算ツール（例えば、Calculator）を呼び出す場合もあります。

   ```
   Action: Calculator, Input: "60 - 6"
   ```

5. **最終回答の生成:**  
   計算ツールから得た結果を踏まえ、最終的な回答として出力します。
   ```
   Final Answer: 54ドル
   ```

この一連の内部プロセスが**Chain-of-Thought**です。ReActAgent はこのように、内部で段階的な推論（Chain-of-Thought）を行いながら、必要なタイミングで外部ツールを呼び出す「Act（行動）」部分と連携して最終的な解答を生成します。

---

### まとめ

- **Chain-of-Thought**は、モデルが問題解決のために内部で展開する論理的な思考過程です。
- ReActAgent では、この Chain-of-Thought が外部ツールへの呼び出しなどの行動と連携し、透明性のある解答生成プロセスを実現しています。
- 具体例では、商品の価格計算と割引適用の過程が Chain-of-Thought として展開され、場合によっては計算ツールを利用することで最終回答を導き出す仕組みとなっています。

このように、Chain-of-Thought は ReActAgent における重要な概念であり、エージェントの「思考」と「行動」を結びつける役割を担っています。

</details>

<details>
<summary>from_template(), partial(), render_text_description()について</summary>
以下に、`from_template`、`partial`、`render_text_description`の各関数・メソッドがどのように機能するのか、具体例を交えて解説します。

---

## 1. `from_template`: テンプレート文字列から PromptTemplate を作成する

### 概要

`from_template`は、あらかじめ用意したテンプレート文字列（例："You are a helpful assistant. Answer this: {question}"）から、**PromptTemplate** オブジェクトを生成します。  
テンプレート内の`{...}`で囲まれた部分を変数（プレースホルダー）として認識します。

### 具体例

```python
from langchain.prompts import PromptTemplate

# テンプレート文字列からPromptTemplateを作成する
template_str = "You are a helpful assistant. Answer the following question: {question}"
prompt = PromptTemplate.from_template(template_str)

# 必要な変数が何か（この場合は"question"）が自動的に認識される
print(prompt.input_variables)  # 出力: ['question']

# 実際に変数を埋め込んでプロンプトを生成する
formatted_prompt = prompt.format(question="What is the capital of France?")
print(formatted_prompt)
# 出力: "You are a helpful assistant. Answer the following question: What is the capital of France?"
```

---

## 2. `partial`: テンプレートの一部の変数に値を先にバインドする

### 概要

`partial`は、すでに作成された PromptTemplate に対して、一部の変数に具体的な値を事前に埋め込むためのメソッドです。  
これにより、同じテンプレートを使い回す際、固定部分だけ先に決め、残りの変数は後で埋めることができます。

### 具体例

```python
from langchain.prompts import PromptTemplate

# 複数の変数を持つテンプレートを作成
template_str = "You are a {role}. Please answer this question: {question}"
prompt = PromptTemplate.from_template(template_str)

# partial()を用いて "role" の部分を固定する
partial_prompt = prompt.partial(role="helpful assistant")

# この時点では "question" のみ未定義
# 最後に "question" を指定して最終的なプロンプトを生成
final_prompt = partial_prompt.format(question="What is the capital of France?")
print(final_prompt)
# 出力: "You are a helpful assistant. Please answer this question: What is the capital of France?"
```

---

## 3. `render_text_description`: ツールの情報を整形して文字列化する

### 概要

`render_text_description`は、エージェントが利用可能なツール（例えば、計算や検索など）のオブジェクトリストを、人間にも LLM にも理解しやすいテキスト形式に変換するための関数です。  
このテキストは、プロンプトテンプレート内に埋め込むことで、LLM に「どのツールが使えるのか」を伝える役割を果たします。

### 具体例

まず、ツールを表すシンプルなクラスと、そのリストを作成します。

```python
# ツールを表すシンプルなクラス（実際はLangChainのToolオブジェクトなどを利用）
class Tool:
    def __init__(self, name, description):
        self.name = name
        self.description = description

# 複数のツールをリストとして用意
tools = [
    Tool(name="Calculator", description="Performs arithmetic operations."),
    Tool(name="Search", description="Searches the web for information.")
]
```

次に、`render_text_description`がツールリストから情報を整形する例です。  
※以下は概念的な実装例です。実際の LangChain の実装では、ツールの名前や説明、場合によっては使用例なども含めたよりリッチなフォーマットに変換します。

```python
def render_text_description(tools):
    # 各ツールの名前と説明を "Name: Description" 形式で連結する例
    descriptions = [f"{tool.name}: {tool.description}" for tool in tools]
    return "\n".join(descriptions)

# ツール情報を文字列に変換
tools_description = render_text_description(tools)
print(tools_description)
```

**出力例:**

```
Calculator: Performs arithmetic operations.
Search: Searches the web for information.
```

この整形済みの文字列を、たとえばエージェントのプロンプトテンプレートに埋め込むことで、「利用可能なツール一覧」として LLM に提供できます。

---

## 4. まとめ

- **`from_template`**

  - テンプレート文字列から**PromptTemplate**オブジェクトを生成。
  - テンプレート内のプレースホルダー（例: `{question}`）を自動で認識する。

- **`partial`**

  - 既存の PromptTemplate に対して、一部の変数（例: `role`）に具体的な値を事前に埋め込む。
  - 残りの変数は後から`format()`で埋めることが可能。

- **`render_text_description`**
  - ツールオブジェクトのリストから、その名前や説明を整形し、1 つの文字列に変換する。
  - 整形された文字列をプロンプトに埋め込むことで、LLM に利用可能なツール情報を提供できる。

これらの機能を組み合わせることで、エージェントは柔軟なプロンプト作成とツール連携が可能になり、ユーザーの問いに対してより適切な応答を生成できるようになります。

</details>

<details>
<summary>ChatOpenAI()の引数にstopが必要な理由</summary>

`ChatOpenAI()` の引数に `stop="\nObservation"` を設定する理由は、生成されるテキストの出力を制御し、特定の箇所で生成を停止させるためです。具体的には、ReAct エージェントなどで使われる**Chain-of-Thought（CoT）**のパターンに合わせて、モデルが「Observation（観察結果）」を出力する直前で生成を打ち切るように指示しています。

以下、ステップ・バイ・ステップで説明します。

---

### 1. **stop 引数の役割**

- **生成停止の制御:**  
  `stop` 引数は、言語モデルに対して「この文字列が現れたら生成を停止せよ」と指示します。  
  例えば、`stop="\nObservation"` とすることで、出力の中に改行と「Observation」という文字列が現れた時点で、モデルはそれ以降のテキスト生成を中断します。

---

### 2. **ReAct エージェントと Chain-of-Thought の関係**

- **ReAct のパターン:**  
  ReAct エージェントは、内部で「**Thought**（思考）」や「**Action**（行動）」のプロセスを展開し、ツール呼び出しの前に「Observation」を受け取るための区切りを設けることがあります。
- **生成の区切り:**  
  モデルが出力するチェーン・オブ・ソートは次のようなパターンを取ることが多いです:
  ```
  Thought: 今、計算が必要だと判断した。
  Action: Calculator, Input: "3+2"
  Observation: 5
  ```
  この例では、「Observation:」という部分がツールからの返答を受け取るためのマーカーとなります。  
  `stop="\nObservation"` を設定することで、モデルは「Observation」が出力される前に生成を停止し、内部処理（ツール呼び出しやその結果の挿入）を安全に行うことができます。

---

### 3. **具体的なメリット**

- **不要なテキストの生成を防ぐ:**  
  モデルが「Observation」の後ろまで生成してしまうと、予期しない追加情報が混じる可能性があります。  
  停止シーケンスにより、必要な部分だけを出力し、その後の処理に干渉しないようにします。

- **明確な区切り:**  
  出力が「\nObservation」という文字列で区切られるため、システム側で生成結果とツールの出力を明確に分けることができます。  
  これにより、後続の処理（ツールの実行結果の統合など）がスムーズになります。

---

### 4. **まとめ**

- **`stop="\nObservation"` の目的:**
  - **生成制御:** モデルが「Observation」の手前で生成を停止し、余計なテキストを出力しないようにする。
  - **プロンプトの区切り:** ReAct エージェントのチェーン・オブ・ソートにおいて、思考と外部ツールの結果（Observation）の間に明確な区切りを設ける。
  - **処理の整合性:** ツール呼び出しやその結果の取り込みのタイミングを整えるための仕組み。

このように、`stop="\nObservation"` を設定することで、エージェントが正しいタイミングで生成を停止し、内部の推論と外部ツールの連携がスムーズに行われるようになります。

</details>

<details>
<summary>callbacksってなんなんや？</summary>

LangChain における**callbacks**とは、エージェントや LLM、チェーンの実行中に特定のイベント（例えば、処理の開始、終了、途中経過など）に応じて自動的に呼び出されるハンドラー（関数やオブジェクト）のことです。これにより、実行の進行状況をログに記録したり、デバッグ情報を表示したり、UI を更新したりするなど、さまざまなサイドエフェクトを実装することができます。

### コード例の解説

```python
llm = ChatOpenAI(
    temperature=1,
    stop=["\n    Observation"],
    callbacks=[
        AgentCallbackHandler
    ]
)
```

上記のコードでは、`ChatOpenAI`（大規模言語モデルを扱うクラス）のインスタンスを作成するときに、`callbacks`パラメータに`AgentCallbackHandler`を渡しています。これにより、LLM の呼び出しや応答の各タイミングで`AgentCallbackHandler`内の特定のメソッドが自動的に実行されるようになります。

### 具体例で理解する callbacks

たとえば、以下のようにカスタムのコールバックハンドラーを定義して、LLM の呼び出し開始時と終了時にメッセージを表示する例を考えてみましょう。

```python
from langchain.callbacks.base import BaseCallbackHandler

class MyLoggingCallbackHandler(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        print("LLMの呼び出しを開始しました。プロンプト:", prompts)

    def on_llm_end(self, response, **kwargs):
        print("LLMの応答を受け取りました。応答:", response)

# このカスタムハンドラーをChatOpenAIに渡します。
llm = ChatOpenAI(
    temperature=1,
    stop=["\n    Observation"],
    callbacks=[MyLoggingCallbackHandler()]
)
```

この例では、

- **`on_llm_start` メソッド:**  
  LLM への呼び出しが開始されるときに呼ばれ、送信されたプロンプトの内容をログに出力します。

- **`on_llm_end` メソッド:**  
  LLM から応答を受け取った際に呼ばれ、その応答内容をログに出力します。

### まとめ

- **callbacks の目的:**  
  実行中の各種イベントにフックし、ログ出力、デバッグ、進捗のモニタリング、UI 更新などの追加処理を行うための仕組みです。

- **利用するメリット:**  
  実際にエージェントや LLM がどのように動作しているのか、内部の処理の流れを可視化できるため、開発やデバッグが容易になります。

このように、LangChain の callbacks を使うことで、チェーンやエージェントの動作をより細かく制御・監視できるようになります。

</details>

### まとめ

このセクションでは ReActAgent がどのようにして動いているのかを理解した。
ReAcr とは、Reasoning（推論）と Action（行動）を掛け合わせた言葉。
LLM が与えられたタスクをこなすために、Tool という道具を用いて推論を行い、必要であれば Tool を使って Action を行うのが ReAct であるということを理解した。

個人的に重要だと思ったのが System Prompt だと思った。そもそも ReAct はシステムプロンプトで「推論、アクション、アクション、最後に考察してね。必要な関数は Tool ってのがあるからそれを使ってね。」みたいなのをしているから ReActAgent は動くことができるのだと理解した。そのため、システムプロンプトを ReAct の形にすることが何よりも重要だと感じた。

個人的にすごいなと思ったのが、システムプロンプトの中で以下のように Tool を使ってアクションを起こしてねと書かれてあるのだが、これだけで LLM がよしなに Tool を使って行動してくれるのがすごいなと思った。

```
the action to take, should be one of [{tool_names}]
```

ざっくりと ReActAgent を動かすためのステップは以下の通り。

#### 1. tools の定義

```python
tools = [get_text_length]
```

このように LLM が Action の時に使っても良い Tool をあらかじめ配列で定義しておく。
この時、以下のように関数には`@tool`というデコレータをつける必要がある。こうすることで、システム側に「これは関数やなくてツールなんやで」と伝えることができる。

```python
@tool
def get_text_length(text: str) -> int:
    """
    Returns the length of a text by characters
    """
    print(f"get_text_length enter with {text=}")
    text = text.strip("'\n").strip('"')

    return len(text)
```

#### 2. template の定義

個人的に ReAct の核だなと思ったのがこのシステムテンプレート。システムテンプレートで推論 → アクション（Tool を使う）ように定義しないと、LLM は動いてくれないと思うので、この定義がめちゃくちゃ重要。

```python
template = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}
"""

prompt = PromptTemplate.from_template(template=template).partial(
    tools=render_text_description(tools),
    tool_names=", ".join([t.name for t in tools]),
)
```

上記のプロンプトのインスタンス？を作成している箇所の`partial()`とはシステムプロンプトの変数と引数をマッピングするみたいな役割がある。
`render_text_description()`を使うことで、tools の関数名とその説明（Doc）をテンプレートに渡すことができる。（便利）

#### 3. LLM インスタンスの作成

これは特に話すことない。LLM 開発には必須のやつ。強いていうなら、stop 引数で LLM に対して「stop 引数の内容を生成したらその時点で生成は終了や！」ということを伝えることができる。（へぇ〜）

```python
llm = ChatOpenAI(
    temperature=1,
    stop=["\n    Observation"],
    callbacks=[
        AgentCallbackHandler()
    ]
)
```

callbacks はめちゃくちゃ便利なやつで、例えば LLM が生成を開始する前や後に実行する関数とかを定義することができる。ログをリッチにしていつ LLM の生成が始まって終わったのかをわかりやすくするとかに使えそうな印象。

#### 4. Agent の作成

以下のようにパイプラインで繋げることで Agent を作ることができる。`ReActAgentSingleInputOutputParser()`を使うことで LLM の生成結果をパースして見やすくすることができるよ。

```python
agent = {
    "input": lambda x: x["input"],
    "agent_scratchpad": lambda x: format_log_to_str(x["agent_scratchpad"])
} | prompt | llm | ReActSingleInputOutputParser()
```

あとは以下のように`invoke`したら OK

```python
agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
    {
        "input": "What is the length in charaters of the text 吉田万段打 ?",
        "agent_scratchpad": intermediate_steps
    }
)
```

## intro-to-vector-dbs

- ここではベクトル DB にデータをぶち込んで、それを RAG で取得するという方法を学んだ。
- ベクトルデータにデータをぶち込むには以下のステップが必要。

1. **元のテキストをチャンク化する（細かく分ける）**

   人間も一度にテキストを理解するのではなく、細かい単位に分けて理解するように、機械も同じように理解する必要がある。そのためこのチャンク化は必要なステップとなる。

2. **チャンク化したテキストを埋め込みする**

   埋め込みとは機械が理解しやすい形に加工することである。加工後のデータはベクトルデータとなっている。

3. **ベクトル化したデータと元のテキストをベクトルデータベースのクライアントに渡す**

   あとはベクトルデータに書き込む関数(`PineconeVectorStore.from_documents()`)を使って書き込み先のベクトル DB（index_name）に texts（元のテキストをチャンクしたもの）と embeddings（texts をベクトル化したもの）を渡せば書き込みが行われる

- 以下のコードの解説

  ```python
  PineconeVectorStore.from_documents(
      texts, embeddings, index_name=os.getenv("INDEX_NAME")
  )
  ```

  このコードはベクトルデータベースにチャンク化したテキストとベクトル化したデータを index_name つまり対象のベクトルデータベースにぶち込むためのクライアントを作成している。
  ベクトルデータは機械が理解しやすいように変換しているので、元のテキストいらなくね？って思うかもしれないがそれは間違いで、ベクトルデータと一緒に元のデータも渡すことで検索結果の参照として元のデータを渡すことができるのだ。メタデータ的な立ち位置として texts も渡しているという理解で OK

- ベクトル DB からデータを取得する方法は以下の通り。

1. **embeddings モデルと llm インスタンスの作成**

```python
embeddings = OpenAIEmbeddings()
llm = ChatOpenAI()
```

2. **プロンプトチェーンの作成**

```python
query = "what is pinecone in machine learning?"
chain = PromptTemplate.from_template(template=query) | llm
```

3. **Pinecone オブジェクトの作成**

```python
vectorstore = PineconeVectorStore(
    index_name=os.getenv("INDEX_NAME"), embedding=embeddings
)
```

index_name が対象のベクトル DB の名前、そして、その DB からベクトルデータを取得するために embedding モデルを引数に渡す。

ベクトル DB における検索ではこの embeddings モデルを使って検索を行う。

4. **retrieval QA chain のプロンプトを hub より取得**

```python
retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
```

hub より`langchain-ai/retrieval-qa-chat`というプロンプトテンプレートを取得する。
これは複数のドキュメントから情報をまとめて質問に答えることに適したプロンプトとなっている。

ちなみに中身はこんな感じ。シンプル。

```
Answer any use questions based solely on the context below:

<context>
{context}
</context>
```

5. **ドキュメント統合チェーンの作成**

```python
combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
```

「Document オブジェクトのリスト」を一つのプロンプトにまとめて LLM に渡すチェーン。

例えば以下のような例があるとする。

```python
docs = [
  "もんたは犬が好きですが、猫は普通です",
  "もんたは赤色と青色と黒色が好きです"
]
```

これらのドキュメントを 1 つにまとめてコンテキストに渡すみたいなことがこの関数を使うことでできるようになる。

6. **リトリーバルチェーンの作成**

```python
retrieval_chain = create_retrieval_chain(
    retriever=vectorstore.as_retriever(), combine_docs_chain=combine_docs_chain
)
```

これはユーザーからの質問に対して、Pinecone ベクトル DB から関連するドキュメントを検索（リトリーバル）し、その後 combine_docs_chain で複数のドキュメントを統合し、最終的な回答を生成する一連の流れを構築するための処理である。

ちなみに`vectorstore.as_retriever()`とは、ベクトル DB をリトリーバーとして扱えるように変換する関数である。ユーザーのクエリを受け取り、それをベクトルに変換し、ベクトル DB にて検索を行うためにこの過程が必要なのである。覚えておこう。

まとめるとざっくりと以下のような流れで処理が行われている。
①embeddings モデルはベクトル DB の検索を行うためのモデル →② ベクトル DB のオブジェクトを作成するには index_name と埋め込みモデルが必要 →③ リトリーバルのためのシステムプロンプトを設定する →④`create_stuff_documents_chain()`はドキュメントのリストを 1 つのプロンプトに渡すために必要なチェーン →⑤`create_retrieval_chain()`でベクトル DB の検索（リトリーブ）とドキュメントリスト統合のチェーンを引数に渡し、ベクトル DB のリトリーブのチェーンが完成する →⑥ 最後に`invoke()`し、引数に query を渡せばベクトル DB に埋め込みモデルが検索を行ってくれて、取得したドキュメントリストをコンテキストに渡して回答を答えてくれる。

<details>
<summary>添削</summary>
はい、概ねその通りの流れになっています。以下にそれぞれのステップを再確認します。

1. **Embeddings モデルの利用**

   - **①**: `embeddings`モデルは、クエリや文書を数値のベクトルに変換する役割を担い、これを元にベクトル DB での検索が行われます。

2. **Pinecone ベクトル DB の設定**

   - **②**: `PineconeVectorStore`を作成する際、`index_name`（対象のインデックス名）と`embeddings`モデルが必要です。これにより、どのデータベースから情報を取得するか、そしてテキストをどのようにベクトル化するかが決まります。

3. **リトリーバル用システムプロンプトの設定**

   - **③**: `retrieval_qa_chat_prompt`を通して、どのようにドキュメントを統合して回答を生成するかのプロンプト（テンプレート）が設定されます。

4. **ドキュメント統合チェーンの作成**

   - **④**: `create_stuff_documents_chain()`は、例えば
     ```python
     docs = [
       "もんたは犬が好きですが、猫は普通です",
       "もんたは赤色と青色と黒色が好きです"
     ]
     ```
     のような複数のドキュメントを、一つのプロンプトにまとめ、LLM に渡して回答生成を行うためのチェーンを構築します。

5. **リトリーバルチェーンの完成**

   - **⑤**: `create_retrieval_chain()`により、Pinecone ベクトル DB からのドキュメント検索（リトリーバル）と、統合チェーン（combine_docs_chain）を組み合わせたシステムが完成します。これにより、検索した結果のドキュメントリストを統合して LLM へ渡す処理が一連となります。

6. **クエリの実行と回答生成**
   - **⑥**: 最後に、`invoke()`メソッドを呼び出し、ユーザーの質問（query）を入力すると、
     - Embeddings モデルでクエリがベクトルに変換され、
     - Pinecone ベクトル DB から類似のドキュメントが検索され、
     - 取得したドキュメントリストが統合チェーンに渡され、
     - 統合された情報を元に LLM が最終的な回答を生成します。

この流れにより、ユーザーからの質問に対して、関連情報を効率よく検索し、適切な回答を返すシステムが構築されている、という理解で正しいです。

</details>

個人的に面白いなと思ったのは、プロンプトテンプレートのコンテキストにドキュメントリストをよしなに加工して渡してくれる`create_stuff_documents_chain()`。これがあるから膨大なドキュメントのリストもコンテキストに含めることができる。
そして、<font color="red">**これを`create_retrieval_chain()`の引数に渡すだけでよしなにドキュメントを取得し、結合しコンテキストに渡してくれるのがすごい便利**</font>だなと思った。

- `RunnablePassthrough()`について
  `RunnablePassthrough()`とは pass through つまり、通過するという名前の通り、受け取った値をそのまま渡すという役割を担う。

input として、"これはテストです"と受け取ったら、それを加工せずそのまま"これはテストです"と表示する。

とりあえず何もしない人ってイメージで OK

![alt text](images/image_2.jpg)

上図は LangSmith から見た LLM の実行ログになる。確かにベクトル DB からクエリに関連するドキュメントをリトリーバルできている。

そして、以下は format_docs()の結果になるのだが、シンプルに\n\n で連結されていることがわかる。`RunnablePassthrough()`はこの単純なドキュメントをコンテキストに渡す役割がある。

<details>
<summary>format_docs()の結果</summary>
```
{
  "output": "仕事では人の話に耳を傾け、重要なことを選択し集中する必要があり、正しく優先順位をつける必要がある。\n\n寝不足だとそのような能力に対して大きな悪影響がある。\n\n**寝不足の状態だと前頭葉の良心の阿責を感じにくくなり、大雑把な行動、衝動的な行動、無責任な行動をしやすくなる**という研究結果もある。\n\n寝不足だと衝動的になりやすいのだ。\n\n仕事でもパフォーマンスを発揮するために、睡眠は非常に大切。何よりも睡眠を重要視するべきである。\n\n# もんた的目的\n\n睡眠について学びたい。\n\n睡眠について深く学び、今の生活を改善したい。\n\n最も体調を良くする睡眠方法を学び、実践し、生活のクオリティを高めたい。\n\n# 第1部　科学者がそろって「絶対に寝るべき」と言う理由\n\n## 第1章　24時間にある2つの世界\n\n---\n\n### たった一晩の寝不足を甘く見てはいけない\n\nたった一晩の睡眠も甘く見てはいけない。\n\n「寝溜めしたらなんとかなる」と思っている人も多いだろうが、現実はそう簡単ではない。\n\nたった一晩睡眠を十分に取らなかっただけでも、クロノ・プロテイン（時計タンパク質）を作る遺伝子にエピジェネティック変異が見られたことがわかっている。\n\n時計タンパク質は代謝や体細胞が持つ多くの機能をコントロールしている。\n\nエピジェネティック変異とは体細胞の重要なプロセスに直接的な変化が生まれることである。\n\nつまり、睡眠不足によって体細胞が持つ多くの機能をコントロールする箇所の生成プロセスが変化してしまうということ。\n\nこれはさまざまな代謝障害につながり、2型糖尿病や肥満といったリスクを高める可能性がある。\n\n<aside>\n✅ ＊睡眠は身体に対しても多大なる影響を与える\n＊夕食は熱に変換しづらく、脂肪に変わりやすい\n＊寝不足になると覚醒時間が多いので、**脳はより多くのエネルギーを得ようとする**\n＊睡眠不足になると、樹状細胞とT細胞の連携がうまくいかず、その結果免疫細胞を作るB細胞が免疫細胞をあまり産出できない。その結果、**免疫力が低下**する\n＊睡眠不足になると筋肉は血中の糖を吸収しずらくなり、血糖値が高まる。その結果、糖尿病リスクが高まる\n＊睡眠中はダメージを受けた心臓のタンパク質を入れ替えている。心臓は睡眠によって回復するのだ\n\n</aside>\n\n# もんた的感想\n\n睡眠について深く学べる本だった。\n\n睡眠のコツというよりかは、「睡眠を取らないとこういったリスクがありますよ」ということを教えてくれる本だった。（まぁそもそも睡眠の本ってそんなもんか）\n\nとりあえず、7時間〜8時間の睡眠はマストで取らないとやばいなと思った。\n\n睡眠によって人間の体は健康に保たれているんだということがわかる内容だった。\n\n睡眠は、記憶の定着、健康的な体の維持、メンタル、私生活すべてに影響を与えるものであることを学んだ。\n\nシンプルに考えて、人生の3分の1は寝ているのだからもっと気を使っていこうと思った。\n\n特に、深い睡眠がとても退治ということを本書では学んだ。\n\n深い睡眠中は、記憶の定着、脳内老廃物の排出、心臓のタンパク質の入れ替えなどさまざまな役割があることを学んだ。\n\nそして、睡眠は1日を通して気を使うべきことだということを学んだ。朝しっかり日光を浴びるということからも睡眠は始まっていることを学んだ。\n\n朝しっかり日光を浴びないと、夜にインスリンが分泌されなくなる。\n\nインスリンがあるから深い睡眠ができるのだし、寝る前のスマホや日光を浴びないことがどれだけ愚かな行為かを本書を通して学ぶことができた。\n\nこれからは日光を浴びる、睡眠時間を7時間〜8時間は確保することを肝に銘じようと思う。\n\nそして、仕事でも私生活でも充実した生活をしようと思う。\n\nありがとうござました。おやすみ。\n\n<aside>\n✅ ＊たった一晩の睡眠不足でもタンパク質を生成するプロセスに影響を与える\n＊睡眠には1~4のステージがあり、特に重要なのが深い睡眠である2,3である\n＊深い睡眠の時は**記憶の整理や不要な記憶の削除**を行っている\n＊夢は脳が活発になる時に起きる**ランダムな記憶の選択**によるもの\n＊夜のブルーライトは、朝にしっかりと太陽を浴びている場合はあまり影響を受けない可能性がある\n\n</aside>\n\n# 第2部　睡眠の「すごい効果」を全部受け取る\n\n## 第5章　眠って賢者になる\n\n---\n\n### 短期記憶が長期記憶となるプロセス\n\n短期記憶が長期記憶となるプロセスを説明する。\n\n初めに、「sleep = 睡眠」という単語を覚えたとする。\n\nこのとき覚えた単語は脳の短期記憶保管庫である海馬に蓄積される。海馬は単語を記憶する際に、脳のどの部分が使われたかを記憶している。\n\nそして我々が深い眠りにつくと、言語記憶を司る脳の領域から視床に向けて「睡眠紡錘波を送ってくれ！」というメッセージが伝わり、視床から睡眠紡錘波が送られてくる。\n\n信号が送られてくると、神経細胞へのカルシウムの流れが促され、シナプスの強化のための条件が揃う。\n\n上記のプロセスが続くと、海馬から言語処理を司る脳の領域にリップル波と呼ばれる脳波のパケットを送る。\n\n海馬はどの神経回路が単語の学習に貢献したかを覚えており、リップル波を用いて睡眠紡錘波を正しい領域へと送り、長期記憶を促す。\n\nこのように、**長期記憶には深い眠りが必要不可欠**なのである。"
}
```
</details>

そして、プロンプトテンプレートの中身を見てみると、`format_docs()`の結果がそのまま渡されていることがわかる。

<details>
<summary>実際のテンプレートの中身</summary>

```

    Use the following pieces of context to answer the question at the end.
    if you don't know the answer, just say that you don't know, don't try to make up an answer.
    Use three sentence maximum and keep the answer as concise as possible.
    Always say "thanks for asking!" at the end of the answer.

    仕事では人の話に耳を傾け、重要なことを選択し集中する必要があり、正しく優先順位をつける必要がある。

寝不足だとそのような能力に対して大きな悪影響がある。

**寝不足の状態だと前頭葉の良心の阿責を感じにくくなり、大雑把な行動、衝動的な行動、無責任な行動をしやすくなる**という研究結果もある。

寝不足だと衝動的になりやすいのだ。

仕事でもパフォーマンスを発揮するために、睡眠は非常に大切。何よりも睡眠を重要視するべきである。

# もんた的目的

睡眠について学びたい。

睡眠について深く学び、今の生活を改善したい。

最も体調を良くする睡眠方法を学び、実践し、生活のクオリティを高めたい。

# 第1部　科学者がそろって「絶対に寝るべき」と言う理由

## 第1章　24時間にある2つの世界

---

### たった一晩の寝不足を甘く見てはいけない

たった一晩の睡眠も甘く見てはいけない。

「寝溜めしたらなんとかなる」と思っている人も多いだろうが、現実はそう簡単ではない。

たった一晩睡眠を十分に取らなかっただけでも、クロノ・プロテイン（時計タンパク質）を作る遺伝子にエピジェネティック変異が見られたことがわかっている。

時計タンパク質は代謝や体細胞が持つ多くの機能をコントロールしている。

エピジェネティック変異とは体細胞の重要なプロセスに直接的な変化が生まれることである。

つまり、睡眠不足によって体細胞が持つ多くの機能をコントロールする箇所の生成プロセスが変化してしまうということ。

これはさまざまな代謝障害につながり、2型糖尿病や肥満といったリスクを高める可能性がある。

<aside>
✅ ＊睡眠は身体に対しても多大なる影響を与える
＊夕食は熱に変換しづらく、脂肪に変わりやすい
＊寝不足になると覚醒時間が多いので、**脳はより多くのエネルギーを得ようとする**
＊睡眠不足になると、樹状細胞とT細胞の連携がうまくいかず、その結果免疫細胞を作るB細胞が免疫細胞をあまり産出できない。その結果、**免疫力が低下**する
＊睡眠不足になると筋肉は血中の糖を吸収しずらくなり、血糖値が高まる。その結果、糖尿病リスクが高まる
＊睡眠中はダメージを受けた心臓のタンパク質を入れ替えている。心臓は睡眠によって回復するのだ

</aside>

# もんた的感想

睡眠について深く学べる本だった。

睡眠のコツというよりかは、「睡眠を取らないとこういったリスクがありますよ」ということを教えてくれる本だった。（まぁそもそも睡眠の本ってそんなもんか）

とりあえず、7時間〜8時間の睡眠はマストで取らないとやばいなと思った。

睡眠によって人間の体は健康に保たれているんだということがわかる内容だった。

睡眠は、記憶の定着、健康的な体の維持、メンタル、私生活すべてに影響を与えるものであることを学んだ。

シンプルに考えて、人生の3分の1は寝ているのだからもっと気を使っていこうと思った。

特に、深い睡眠がとても退治ということを本書では学んだ。

深い睡眠中は、記憶の定着、脳内老廃物の排出、心臓のタンパク質の入れ替えなどさまざまな役割があることを学んだ。

そして、睡眠は1日を通して気を使うべきことだということを学んだ。朝しっかり日光を浴びるということからも睡眠は始まっていることを学んだ。

朝しっかり日光を浴びないと、夜にインスリンが分泌されなくなる。

インスリンがあるから深い睡眠ができるのだし、寝る前のスマホや日光を浴びないことがどれだけ愚かな行為かを本書を通して学ぶことができた。

これからは日光を浴びる、睡眠時間を7時間〜8時間は確保することを肝に銘じようと思う。

そして、仕事でも私生活でも充実した生活をしようと思う。

ありがとうござました。おやすみ。

<aside>
✅ ＊たった一晩の睡眠不足でもタンパク質を生成するプロセスに影響を与える
＊睡眠には1~4のステージがあり、特に重要なのが深い睡眠である2,3である
＊深い睡眠の時は**記憶の整理や不要な記憶の削除**を行っている
＊夢は脳が活発になる時に起きる**ランダムな記憶の選択**によるもの
＊夜のブルーライトは、朝にしっかりと太陽を浴びている場合はあまり影響を受けない可能性がある

</aside>

# 第2部　睡眠の「すごい効果」を全部受け取る

## 第5章　眠って賢者になる

---

### 短期記憶が長期記憶となるプロセス

短期記憶が長期記憶となるプロセスを説明する。

初めに、「sleep = 睡眠」という単語を覚えたとする。

このとき覚えた単語は脳の短期記憶保管庫である海馬に蓄積される。海馬は単語を記憶する際に、脳のどの部分が使われたかを記憶している。

そして我々が深い眠りにつくと、言語記憶を司る脳の領域から視床に向けて「睡眠紡錘波を送ってくれ！」というメッセージが伝わり、視床から睡眠紡錘波が送られてくる。

信号が送られてくると、神経細胞へのカルシウムの流れが促され、シナプスの強化のための条件が揃う。

上記のプロセスが続くと、海馬から言語処理を司る脳の領域にリップル波と呼ばれる脳波のパケットを送る。

海馬はどの神経回路が単語の学習に貢献したかを覚えており、リップル波を用いて睡眠紡錘波を正しい領域へと送り、長期記憶を促す。

このように、**長期記憶には深い眠りが必要不可欠**なのである。

    Question: なぜ睡眠をとる必要があるのか？重要性を教えてください。

    Helpful Answer:

```

</details>

なるほどなぁと思ったのは、ドキュメントのリストを\n\nで連結してシンプルなString型に変換したのち、それを`RunnablePassthrough()`に渡すという流れ。
このようなシンプルな実装も含まれているのが面白いなと思った。

### ChatGPT による解説

<details>
<summary>Embeddingとは？</summary>

Embeddings（埋め込み）とは、テキスト（単語、文、段落など）を、機械学習モデルが理解しやすい数値のベクトル（例えば、固定長の数値の配列）に変換したものです。これにより、コンピュータはテキストの意味や文脈を数学的に扱えるようになります。

### 具体例で説明

#### 例 1: 単語の埋め込み

例えば、「猫」と「犬」という単語があるとします。人間はどちらも動物であり、可愛らしいイメージがあるという共通点を直感的に理解できます。しかし、コンピュータは文字列のままではこの類似性を理解できません。

そこで、Word2Vec や GloVe のようなモデルを使って、各単語を 300 次元の数値ベクトルに変換します。すると、

- 「猫」 → `[0.25, -0.13, 0.78, ..., 0.05]`
- 「犬」 → `[0.27, -0.11, 0.75, ..., 0.07]`

というようなベクトルになります。これらのベクトルは「猫」と「犬」が似た意味を持つため、空間上でも近い位置に配置されます。一方、例えば「車」のベクトルは全く異なる方向になるでしょう。

#### 例 2: 文の埋め込み

文章全体の意味を表現するために、BERT や GPT などのモデルを使って、文章全体をベクトル化することもできます。たとえば、

- 「私は毎朝コーヒーを飲みます。」
- 「毎朝、コーヒーを飲むのが私の日課です。」

これら 2 つの文は、意味的に非常に似ています。埋め込みベクトルに変換すると、空間上で互いに近い位置にマッピングされるため、「似た内容の文章はベクトル空間上で近い距離にある」という性質が生まれます。

### Embeddings の活用例

- **類似性検索**: 複数の文書や単語のベクトル間の距離を計算し、意味的に似たものを検索できます。
- **クラスタリング**: 似た内容の文書をグループ化するために使用できます。
- **自然言語処理（NLP）タスク全般**: 翻訳、要約、感情分析など、多くの NLP タスクで基盤となる技術です。

まとめると、Embeddings は「テキストの意味や文脈を数値として表現する技術」であり、これにより機械は人間の言語を数学的に処理できるようになります。

</details>

<details>
<summary>ベクトルDBからコンテキストを取得するステップ</summary>
以下はコード全体の流れと各部分の役割についての詳細な解説です。

---

### 1. ライブラリのインポートと環境変数の読み込み

```python
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

load_dotenv()
```

- **`import os`**  
  OS に関する操作（例: 環境変数の取得）を行うための標準ライブラリです。

- **`from dotenv import load_dotenv`**  
  `.env`ファイルから環境変数を読み込むためのライブラリです。  
  `load_dotenv()` を呼び出すことで、同ディレクトリ内の `.env` に記述された変数が読み込まれ、 `os.getenv()` でアクセスできるようになります。

- **LangChain 関連のインポート**
  - `PromptTemplate`: LLM へ渡すためのプロンプト（問い）を定義するクラスです。
  - `ChatOpenAI`: OpenAI のチャット形式の言語モデルを利用するためのクラス。
  - `OpenAIEmbeddings`: テキストをベクトル（数値表現）に変換するためのクラス。
  - `PineconeVectorStore`: Pinecone（ベクトルデータベース）を利用するためのクラス。
  - `hub`: LangChain が提供する「ハブ」から既存のプロンプトやチェーンを取得するためのモジュール。
  - `create_stuff_documents_chain`: 複数のドキュメント（情報）を統合し、LLM で回答を生成するチェーンを作成する関数。
  - `create_retrieval_chain`: 検索（リトリーバル）と回答生成を組み合わせたチェーンを作成する関数。

---

### 2. メイン処理の開始

```python
if __name__ == "__main__":
    print("Retrieving...")
```

- **`if __name__ == "__main__":`**  
  このスクリプトが直接実行された場合に以下の処理を実行するための条件分岐です。

- **`print("Retrieving...")`**  
  プログラムが実行された際に、「Retrieving...」というメッセージを出力し、処理開始を知らせます。

---

### 3. 埋め込みモデルと LLM の初期化

```python
    embeddings = OpenAIEmbeddings()
    llm = ChatOpenAI()
```

- **`embeddings = OpenAIEmbeddings()`**  
  テキストを数値のベクトルに変換するモデルを初期化します。  
  このベクトル表現は後で Pinecone での類似度検索に使用されます。

- **`llm = ChatOpenAI()`**  
  チャット形式の対話型 LLM（大規模言語モデル）を初期化します。  
  質問に対する回答生成や、複数のドキュメントから情報を統合する際に使用されます。

---

### 4. シンプルなプロンプトチェーンの作成（※コメントアウト部分）

```python
    query = "what is pinecone in machine learning?"
    chain = PromptTemplate.from_template(template=query) | llm
    # result = chain.invoke(input={})
    # print(result.content)
```

- **`query = "what is pinecone in machine learning?"`**  
  ユーザーからの質問を文字列として定義しています。

- **`chain = PromptTemplate.from_template(template=query) | llm`**

  - `PromptTemplate.from_template(template=query)`  
    与えられた文字列を元にプロンプトテンプレートを生成します。
  - `| llm`  
     生成したプロンプトを LLM にパイプラインのように渡すことで、簡単なチェーン（処理の流れ）を構築しています。  
    ※ このチェーンは単一のプロンプトを LLM へ送信して回答を得るシンプルな例ですが、実際には下記のリトリーバルチェーンを使用しています。

- **コメントアウト部分**  
  `chain.invoke(input={})` や `print(result.content)` は実際にチェーンを実行して結果を出力する処理ですが、今回は実行せずにスキップされています。

---

### 5. Pinecone ベクトルストアの設定

```python
    vectorstore = PineconeVectorStore(
        index_name=os.getenv("INDEX_NAME"), embedding=embeddings
    )
```

- **`PineconeVectorStore`**  
  Pinecone というベクトルデータベースを利用して、テキストデータの類似度検索を行うためのオブジェクトです。

- **パラメータ**
  - `index_name=os.getenv("INDEX_NAME")`  
    環境変数からインデックス名を取得します。インデックスは Pinecone 上でデータが保存されている領域を指します。
  - `embedding=embeddings`  
    先ほど初期化した OpenAIEmbeddings のインスタンスを渡すことで、テキストをベクトルに変換する処理を連携させます。

---

### 6. Retrieval QA チャットプロンプトの取得

```python
    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
```

- **`hub.pull("langchain-ai/retrieval-qa-chat")`**  
  LangChain のハブから、既存の「retrieval-qa-chat」という名前のプロンプトテンプレート（またはチェーン）をダウンロードします。  
  これは、複数のドキュメントから情報をまとめて質問に答える際に適したプロンプトです。

---

### 7. ドキュメント統合チェーンの作成

```python
    combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
```

- **`create_stuff_documents_chain`**  
  検索結果として得られた複数のドキュメントを、LLM とプロンプトを使って一つの回答にまとめるためのチェーンを作成します。
  - **引数**
    - `llm`: 回答生成に利用する言語モデル。
    - `retrieval_qa_chat_prompt`: 統合のために利用するプロンプトテンプレート。  
      このチェーンは、類似度検索で取得した複数の情報を「stuff（詰め込む）」て、最終的な回答文を生成する役割を担います。

---

### 8. リトリーバルチェーンの作成

```python
    retrieval_chain = create_retrieval_chain(
        retriever=vectorstore.as_retriever(), combine_docs_chain=combine_docs_chain
    )
```

- **`create_retrieval_chain`**  
  質問に対して、まず関連するドキュメントを検索（リトリーバル）し、その後にそれらの情報を統合して回答を生成する一連のプロセスをチェーンとして構築します。

- **パラメータ**
  - `retriever=vectorstore.as_retriever()`  
    PineconeVectorStore を「リトリーバー」に変換します。これにより、入力クエリに対して最も関連性の高いドキュメントをベクトル検索で取得できるようになります。
  - `combine_docs_chain=combine_docs_chain`  
    先ほど作成した、取得したドキュメントを統合して回答を生成するチェーンを組み込みます。

---

### 9. クエリの実行と結果の出力

```python
    result = retrieval_chain.invoke(input={"input": query})
    print(result)
```

- **`retrieval_chain.invoke(input={"input": query})`**

  - リトリーバルチェーンを実行することで、以下の一連の処理が行われます:
    1. 入力された `query` を用いて、Pinecone ベクトルストアから類似度の高いドキュメントが検索される。
    2. 取得したドキュメント群が、`combine_docs_chain` によって一つの回答に統合される。
    3. 統合された内容をもとに、LLM が最終的な回答を生成する。

- **`print(result)`**  
  チェーンの実行結果（LLM による回答や統合結果）が出力されます。

---

### 全体のまとめ

このコードは、以下のようなワークフローを実現しています:

1. **環境準備**: `.env` から必要な環境変数を読み込み、Pinecone のインデックス名などを取得。
2. **モデルの初期化**: OpenAI の埋め込みモデルとチャット LLM を初期化。
3. **リトリーバル準備**: Pinecone を利用して、ベクトル検索ができるリトリーバーを構築。
4. **プロンプトとチェーンの設定**: ハブから適切なプロンプトを取得し、複数のドキュメントを統合するチェーンを作成。
5. **質問の実行**: ユーザーの質問に対して、関連ドキュメントを検索し、統合して回答を生成。

この仕組みにより、大量のデータから最も関連性の高い情報を抽出し、LLM を使ってわかりやすい回答を生成するリトリーバル QA システムが実現されています。

</details>

<details>
<summary>リトリーバルQAシステムについて</summary>
これらの2行のコードは、**リトリーバルQAシステム**を構築するための重要なステップです。具体的には、以下のような処理を自動化しています。

---

### 1. 複数のドキュメントを統合するチェーンの作成

```python
combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
```

- **目的**:  
  複数の関連ドキュメントから得られた情報を 1 つにまとめ、LLM に最終回答を生成させるためのチェーンを作成します。

- **具体例**:  
  例えば、ユーザーが「What is pinecone in machine learning?」という質問をしたとします。  
  この質問に対して、Pinecone に関する複数の情報（例えば、Pinecone がベクトルデータベースである、どのように使われるかなど）がデータベースから取得されるとします。  
  そのとき、`combine_docs_chain` は取得された各文書（例：ドキュメント A、ドキュメント B、ドキュメント C）をひとつのプロンプトにまとめます。  
  まとめたプロンプトは、

  > 「以下の情報を参考にして、'What is pinecone in machine learning?' に答えてください。  
  > ドキュメント A: ...  
  > ドキュメント B: ...  
  > ドキュメント C: ...」  
  > のような形になり、LLM が全体の文脈を把握して回答を生成できるようになります。

- **ポイント**:
  - `llm`: 回答生成に使われる大規模言語モデル。
  - `retrieval_qa_chat_prompt`: どのように情報を統合し、質問に回答するかのフォーマット（プロンプトテンプレート）を定義しているもの。

---

### 2. リトリーバルと統合を連携するチェーンの作成

```python
retrieval_chain = create_retrieval_chain(
    retriever=vectorstore.as_retriever(), combine_docs_chain=combine_docs_chain
)
```

- **目的**:  
  ユーザーの質問に対して、まず Pinecone ベクトル DB から関連するドキュメントを検索（リトリーバル）し、その後、先ほど作成した`combine_docs_chain`で複数のドキュメントを統合して最終回答を生成する一連の流れを構築します。

- **具体例**:  
  再び「What is pinecone in machine learning?」という質問を考えます。

  1. **検索ステップ**:  
     `vectorstore.as_retriever()` がこの質問を元に、Pinecone 内のインデックスから最も関連性の高い複数の文書（例えば、技術ドキュメント、記事、説明文）を返します。
  2. **統合ステップ**:  
     取得された文書群が、`combine_docs_chain` に渡され、上記のようなひとつの大きなプロンプトにまとめられます。
  3. **回答生成**:  
     最終的に、LLM がこの統合されたプロンプトを元に、ユーザーの質問に対する適切な回答を生成します。

- **ポイント**:
  - **リトリーバー**: ベクトル DB から質問に関連する情報を取得する役割。
  - **統合チェーン**: 取得された情報を整理して、LLM に渡すための適切な形にする役割。

---

### なぜこれらが必要なのか？

- **シンプルな例だけでは不足**:  
  単に LLM に質問を送るだけでは、広範な知識を持っていても、特定のドメインの最新情報や詳細な専門情報を正確に回答するのは難しい場合があります。

- **検索と生成の連携**:  
  ここでは、**検索（Retrieval）** と **生成（Generation）** の 2 つのプロセスを組み合わせています。

  - **検索**で信頼性のあるドキュメントから情報を抽出し、
  - **統合と生成**でその情報をもとに最終的な回答を生成することで、より正確で具体的な回答が得られる仕組みになっています。

- **自動化とスケーラビリティ**:  
  このチェーンの設計により、ユーザーは単一のクエリを入力するだけで、複数のドキュメントの検索と統合、そして回答生成が自動的に行われるため、手動で情報を収集してまとめる必要がなくなります。

---

### まとめ

- **`create_stuff_documents_chain`**: 複数のドキュメントを一つにまとめて、LLM が利用しやすい形に変換するチェーン。
- **`create_retrieval_chain`**: ユーザーの質問に対して、まず関連情報を検索し、その後に統合チェーンを使って最終回答を生成する一連のプロセスを実現するチェーン。

これにより、例えば「What is pinecone in machine learning?」という質問に対して、データベースから関連文書を取得し、それらの文書を LLM で統合して、ユーザーにわかりやすい回答を返すことが可能になります。

</details>

<details>
<summary>vectorstore.as_retrievaer()とは</summary>
以下に、具体例を使って説明します。

---

### 例: Pinecone に保存されたドキュメントがある場合

例えば、あなたが以下のようなドキュメントを Pinecone のベクトルデータベースに保存しているとします。

- **Document 1:**  
  「Pinecone は、高速かつスケーラブルなベクトルデータベースです。」

- **Document 2:**  
  「ベクトルデータベースは、機械学習や類似検索に利用されます。」

- **Document 3:**  
  「Python を使って Pinecone を操作することができます。」

---

### ユーザーのクエリに基づく検索

ユーザーが例えば「Pinecone とは何か？」という質問をしたとします。

1. **クエリのベクトル化**

   - リトリーバーは、`embeddings`モデルを用いてユーザーのクエリ「Pinecone とは何か？」を数値のベクトルに変換します。

2. **類似度検索**

   - 変換したベクトルと、データベースに保存されている各ドキュメントのベクトルとの類似度を計算します。
   - その結果、ユーザーの質問に最も関連のあるドキュメント（例えば Document 1 や Document 2）が見つかります。

3. **結果の返却**
   - 最も類似度の高いドキュメントのリストが返され、後続の処理（たとえば、複数のドキュメントを統合して回答生成するチェーン）に渡されます。

---

### `vectorstore.as_retriever()` の役割

- **目的:**  
  `vectorstore.as_retriever()` は、Pinecone のデータベース（`vectorstore`）を「リトリーバー」として扱えるように変換します。つまり、ユーザーのクエリを受け取り、上記のようなベクトル化と類似度検索を自動で行うオブジェクトにするためのものです。

- **具体例での利用方法:**

  ```python
  # 既に作成されたPineconeVectorStoreのインスタンスからリトリーバーを生成
  retriever = vectorstore.as_retriever()

  # ユーザーのクエリ
  query = "Pineconeとは何か？"

  # リトリーバーを使って関連するドキュメントを取得する
  relevant_docs = retriever.get_relevant_documents(query)

  # ここで、relevant_docsには、
  # 例えば Document 1 や Document 2 など、クエリに最もマッチするドキュメントが入っている
  ```

---

### まとめ

- `vectorstore.as_retriever()` を呼び出すことで、Pinecone のベクトル DB から「リトリーバル」機能を持つオブジェクトが得られます。
- そのリトリーバーは、ユーザーのクエリをベクトル化し、データベース内のドキュメントと類似度計算を行い、関連性の高いドキュメントのリストを返してくれます。
- この仕組みにより、検索機能と後続の処理（例えばドキュメントの統合や LLM による回答生成）がシームレスに連携できるようになります。

このように、`vectorstore.as_retriever()` は、ベクトルデータベースから関連ドキュメントを簡単に取得するための非常に便利なメソッドなのです。

</details>

<details>
<summary>RunnablePassthrough()とは？</summary>
`RunnablePassthrough()`は、LangChainの新しい「Runnable」インターフェースに沿ったコンポーネントの一種で、名前の通り「何もせずにそのまま入力を出力する」パススルー（透過）用のオブジェクトです。つまり、入力されたデータをそのまま変更せずに返す役割を持っています。

---

### 具体例での解説

#### 1. 何も処理をしないチェーンとしての利用

例えば、以下のようなシンプルなコードを考えます。

```python
from langchain.runnables import RunnablePassthrough

# RunnablePassthroughのインスタンスを作成
passthrough = RunnablePassthrough()

# 任意の入力データ
input_data = "これはテストです"

# RunnablePassthroughは何も加工せずそのまま返す
output_data = passthrough.invoke(input_data)
print(output_data)  # 出力は "これはテストです"
```

この例では、`RunnablePassthrough`は入力された文字列「これはテストです」をそのまま返しています。つまり、何の処理も行っていないので、入力と出力が同じです。

---

#### 2. チェーンの一部として利用

LangChain では、複数の処理を連結（パイプライン）してチェーンを構成することができます。たとえば、ある状況では特定の処理を実施するかどうかを条件で変えたい場合があります。処理をスキップする際に`RunnablePassthrough()`を使うと、何も変換せずに入力をそのまま次のステップに渡すことができます。

```python
from langchain.runnables import RunnablePassthrough

def some_processing(input_text):
    # 何かの加工をして結果を返す処理
    return input_text.upper()

# ある条件に基づいて、処理を行うかしないかを決めるとします。
condition = False  # 条件がFalseの場合は処理をスキップする

if condition:
    processor = some_processing  # 実際の加工処理
else:
    processor = RunnablePassthrough()  # 何もしないパススルー

# 入力データ
input_data = "Hello, world!"

# 条件に応じて、加工されたものかそのままが得られる
if condition:
    output_data = processor(input_data)  # "HELLO, WORLD!"
else:
    output_data = processor.invoke(input_data)  # "Hello, world!"

print(output_data)
```

このように、場合によってはチェーン内で「何も処理しない」ステップが必要な時に、`RunnablePassthrough()`を使うことで、コードの流れを崩さずに入力データをそのまま次のステップに渡すことができます。

---

### まとめ

- **目的**:  
  `RunnablePassthrough()`は、入力をそのまま出力する「何もしない」（ノップ）のコンポーネントです。

- **利用シーン**:
  - 単体で使用して、データをそのまま返す動作確認をする場合。
  - 複雑なチェーンの中で、条件によっては処理をスキップしたい場合に使われ、チェーンの一貫性を保ちながら入力を次のステップに渡す。

このように、`RunnablePassthrough()`は、チェーン構築の際に柔軟性を持たせるための便利なツールとして利用されます。

</details>
