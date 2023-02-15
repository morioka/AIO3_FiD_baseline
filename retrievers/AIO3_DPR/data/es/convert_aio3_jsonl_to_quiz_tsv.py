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
import pandas as pd

from tqdm import tqdm

def main(args: argparse.Namespace):

    # SQuAD JSONL形式から Question-Answer-Context のTSVに直す
    # 複数の positive_ctx がある場合は、複数の行に直す
    # answers には1個のanswerが含まれるのみの前提
    df = pd.read_json(args.input_file)

    quiz = []
    for i, row in tqdm(df.iterrows()):
        if len(row['positive_ctxs']) > 0:
            for p in row['positive_ctxs']:
                quiz.append([row['question'],   # question
                             row['answers'][0], # answer
                             p['text']])        # context

    del df
    df_new = pd.DataFrame(quiz)
    del quiz
    df_new.to_csv(args.output_file, sep='\t', index=None, header=None)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, required=True)
    parser.add_argument("--output_file", type=str, required=True)
    args = parser.parse_args()
    main(args)
