## passageデータ作成用のelasticsearchを再構築する

データ拡張のためにpassageデータ作成用のelasticsearchを用いたい。
そのために `retrievers/AIO3_DPR/data/README.md` 記載の手順のように wikipediaデータを全クロールすることは避けたい。

ここでは、上記のデータ作成の過程で作られて `download_data.sh` で入手できる `jawiki-20220404-c400-large.tsv.gz` を加工前の `passages-jawiki-20220404-paragraphs.json.gz` 相当に変形する。これを元の手順の `build_es_index_passages.py` を用いて elasticsearch に流し込む。

```bash
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

```bash
python convert_quiz_tsv_to_aio3_jsonl.py \
--input_file quiz_question_answer_with_header.tsv \
--output_file aio3_squad_style_question_answer.json 
```

```bash
python convert_aio3_jsonl_to_quiz_tsv.py \
--input_file aio3_squad_style_question_answer_context.json \
--output_file quiz_question_answer_context_without_header.tsv
```


