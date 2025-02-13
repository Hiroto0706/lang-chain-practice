LangChain に詳しくなりたい！

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
