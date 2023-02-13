# Copyright 2021 Masatoshi Suzuki (@singletongue)
# code modified by Yasuhiro Moioka (@morioka), 2023.
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
import argparse
import gzip
import json

from tqdm import tqdm


def main(args: argparse.Namespace):
    with gzip.open(args.input_file, "rt") as f, gzip.open(args.output_file, "wt", encoding='utf-8') as fo:
        for line in tqdm(f):
            id_, text, title = line.strip().split('\t')

            # skip first line
            if (id_ == 'id') & (text == 'text') & (title == 'title'):
                continue

            # create and dump jsonl
            obj = {
                'id': id_,
                'title': title,
                'text': text
            }
            json.dump(obj, fo, ensure_ascii=False)
            fo.write('\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, required=True)
    parser.add_argument("--output_file", type=str, required=True)
    args = parser.parse_args()
    main(args)
