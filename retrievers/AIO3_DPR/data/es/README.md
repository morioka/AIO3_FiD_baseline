## passageデータ作成用のelasticsearchを再構築する

データ拡張のためにpassageデータ作成用のelasticsearchを用いたい。
そのために `retrievers/AIO3_DPR/data/README.md` 記載の手順のように wikipediaデータを全クロールすることは避けたい。

ここでは、上記のデータ作成の過程で作られて `AIO3_DPR/download_data.sh` の実行で入手できる `jawiki-20220404-c400-large.tsv.gz` を加工前の `passages-jawiki-20220404-paragraphs.json.gz` 相当に変形する。これを元の手順 `"5. 作成されたパッセージを用いて、 Elasticsearch のインデックスを作成します。"` の `build_es_index_passages.py` を用いて elasticsearch に流し込む。

```bash
AIO3_DPR/scripts/download_data.sh
python make_es_wikipedia_passages_json.py \
--input_file wiki/jawiki-20220404-c400-large.tsv.gz \
--output_file passages-jawiki-20220404-paragraphs.json.gz
```

- 実際には、上記では id, text, title のtsv を id, text, title の jsonl に直すだけである。
- 出力方法は、これにならった。[pythonでJSON Linesを作る方法 - qtatsuの週報](https://qtatsu.hatenablog.com/entry/2021/03/27/143233)
- 同様の手順で任意のパッセージを elasticsearch へ index 登録できるはず
  - index登録のほか、QAデータセットへのパッセージ付与は、`retrievers/AIO3_DPR/data/README.md` の手順を参照すること。
- 参考のため、上記データを流し込む elasticsearch は `docker-compose.yaml` で起動する。

----

- 以下のファイルを追加。
  - `convert_quiz_tsv_to_aio3_jsonl.py` 
    - question-answerのTSVをpassageなしのSQuAD JSONL形式に変換する。passageを付与する前段階
  - `convert_aio3_jsonl_to_quiz_tsv.py`
    - positive contextが付与された SQuAD JSONLをquestion-answer-contextのTSVに変換する。

```sh
$ python convert_quiz_tsv_to_aio3_jsonl.py \
--input_file quiz_question_answer_with_header.tsv \
--output_file aio3_squad_style_question_answer.json 
```

```sh
$ python convert_aio3_jsonl_to_quiz_tsv.py \
--input_file aio3_squad_style_question_answer_context.json \
--output_file quiz_question_answer_context_without_header.tsv
```

----

## passageデータ作成用のelasticsearchの再構築手順

1. Wikipedia パッセージの elasticsearchを起動します。

```sh
$ cd AIO3_DPR/data/es
$ docker-compose up
```

2. `AIO3_DPR/download_data.sh` を実行して、AI王向けに処理済のデータセットを入手します。

```sh
$ AIO3_DPR/download_data.sh
```

3. `jawiki-20220404-c400-large.tsv.gz` を加工前の `passages-jawiki-20220404-paragraphs.json.gz` 相当に変形します。

```sh
$ python make_es_wikipedia_passages_json.py \
--input_file wiki/jawiki-20220404-c400-large.tsv.gz \
--output_file passages-jawiki-20220404-paragraphs.json.gz
```

4. AIO3_DPR/data/README.md `5. 作成されたパッセージを用いて、 Elasticsearch のインデックスを作成します。`  と同じ手順です。

```sh
$ python build_es_index_passages.py \
--input_file <work_dir>/passages-jawiki-20220404-paragraphs.json.gz \
--index_name jawiki-20220404-paragraphs \
--hostname localhost \
--port 9200
```


### 独自質問応答データセット作成手順

1. Wikipedia パッセージのインデックスを作成済の elasticsearchを起動します。

```sh
$ cd AIO3_DPR/data/es
$ docker-compose up
```

2. パッセージなしの質問応答データセットを AIO3 JSONL形式に変換します。

```bash
$ python convert_quiz_tsv_to_aio3_jsonl.py \
--input_file quiz_question_answer_with_header.tsv.gz \
--output_file aio3_squad_style_question_answer.jsonl
```

3. AIO3_DPR/data/README.md `6. 質問応答データの質問に対して、適合度が高いパッセージを検索して付与します。` と同じ手順です。

```sh
$ python make_dpr_retriever_dataset.py \
--input_file <data_dir>/aio3_squad_style_question_answer.jsonl \
--output_file <dpr_retriever_data_dir>/aio3_squad_style_question_answer.jsonl.gz \
--es_index_name jawiki-20220404-paragraphs \
--num_documents_per_question 100
```

4. 質問-応答-パッセージ のTSV形式の質問応答データセットに変換します。

```bash
python convert_aio3_jsonl_to_quiz_tsv.py \
--input_file <dpr_retriever_data_dir>/aio3_squad_style_question_answer.jsonl.gz \
--output_file quiz_question_answer_context_without_header.tsv
```
