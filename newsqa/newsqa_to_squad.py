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

import pandas as pd
import re
import uuid
import json
import argparse


def answer_text(story_text, answer_token_ranges):
    story_text_list = story_text.split()
    if answer_token_ranges:
        token_range = list(map(int, re.split(':|,', answer_token_ranges)))[0:2]
        answer = ' '.join(story_text_list[slice(token_range[0], token_range[1])])
        return answer


def answer_start(story_text, answer_text):
    if answer_text:
        return story_text.find(answer_text)
    else:
        return -1


def newsqa_to_squad(newsqa_file, output_file):
    newsqa = pd.read_csv(newsqa_file)
    newsqa['answer_text'] = newsqa[['story_text', 'answer_token_ranges']].apply(lambda x: answer_text(*x), axis=1)
    newsqa['answer_start'] = newsqa[['story_text', 'answer_text']].apply(lambda x: answer_start(*x), axis=1)
    newsqa['id'] = newsqa['story_id'].apply(lambda x: str(uuid.uuid4().hex))
    newsqa = newsqa[['id', 'story_text', 'question', 'answer_text', 'answer_start']]
    newsqa_json = newsqa.to_json(orient='records')
    newsqa_json = json.loads(newsqa_json)

    data = []

    for newsqa_example in newsqa_json:
        question_text = newsqa_example['question']
        context = newsqa_example['story_text']

        para = {'context': context, 'qas': [{'question': question_text, 'answers': []}]}
        data.append({'paragraphs': [para]})
        qa = para['qas'][0]
        qa['id'] = newsqa_example['id']
        qa['is_impossible'] = True

        if newsqa_example['answer_start'] != -1:
            ans_string = newsqa_example['answer_text']
            index = newsqa_example['answer_start']
            qa['answers'].append({'text': ans_string, 'answer_start': index})
            qa['is_impossible'] = False

    newsqa_as_squad = {'data': data, 'version': '2.0'}

    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(newsqa_as_squad, outfile, indent=2, sort_keys=True, ensure_ascii=False)


if __name__ == '__main__':
    params = argparse.ArgumentParser()
    params.add_argument('--newsqa_file', help='NewsQA file')
    params.add_argument('--output_file', help='Output file in SQuAD format')

    args = params.parse_args()

    newsqa_to_squad(args.newsqa_file, args.output_file)
