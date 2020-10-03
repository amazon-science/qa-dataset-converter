# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import argparse


def quac_to_squad(quac_file, output_file):
    quac_json = json.load(open(quac_file))
    data = []

    for quac_example in quac_json['data']:
        for p in quac_example['paragraphs']:
            context = p['context']
            for q in p['qas']:
                question_text = q['question']
                para = {'context': context, 'qas': [{'question': question_text, 'answers': []}]}
                data.append({'paragraphs': [para]})
                qa = para['qas'][0]
                qa['id'] = q['id']
                qa['is_impossible'] = True

                if q['orig_answer']['text'] != 'CANNOTANSWER':
                    ans_string = q['orig_answer']['text']
                    index = q['orig_answer']['answer_start']
                    qa['answers'].append({'text': ans_string, 'answer_start': index})
                    qa['is_impossible'] = False

    quac_as_squad = {'data': data, 'version': '2.0'}

    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(quac_as_squad, outfile, indent=2, sort_keys=True, ensure_ascii=False)


if __name__ == '__main__':
    params = argparse.ArgumentParser()
    params.add_argument('--quac_file', help='QuAC file')
    params.add_argument('--output_file', help='Output file in SQuAD format')

    args = params.parse_args()

    quac_to_squad(args.quac_file, args.output_file)
