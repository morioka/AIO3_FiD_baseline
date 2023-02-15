# Copyright 2021 Masatoshi Suzuki (@singletongue)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Modified 2023 Yasuhiro Morioka (@morioka)
import argparse
import gzip
import json

from tqdm import tqdm

import pandas as pd
import math

def clean_answers(x):
    if x is not None:
        try:
            if math.isnan(x):
                return None
            else:
                return [x]
        except:
            return [x]
    else:
        return None

def main(args: argparse.Namespace):

    # Question-Answer の TSVからSQuAD JSONL形式に整形する
    # answers には1個のanswerのみ
    # context情報はなし
    df = pd.read_csv(args.input_file, sep='\t')

    df['title'] = df['genre'].apply(lambda x: x if x is not None else "ジャンルなし")
    df['answers'] = df['answer'].apply(lambda x: clean_answers(x))
    df['timestamp'] = '2022/11/30'

    df = df[['qid', 'title', 'question', 'answers', 'timestamp']]
    df = df.dropna()

    df.to_json(args.output_file, orient='records', lines=True, force_ascii=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, required=True)
    parser.add_argument("--output_file", type=str, required=True)
    args = parser.parse_args()
    main(args)
