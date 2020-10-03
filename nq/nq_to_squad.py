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


# We include functions that are copied/modified from
# https://github.com/google-research-datasets/natural-questions/blob/master/nq_browser.py
# cite: https://github.com/google-research-datasets/natural-questions/

import json
import argparse
import gzip
import glob
import numpy as np
from bs4 import BeautifulSoup


def has_long_answer(nq_example):
    if len(nq_example['annotations']) == 1:
        annotation = nq_example['annotations'][0]
        return annotation['long_answer']['start_byte'] >= 0
    else:
        return sum([annotation['long_answer']['start_byte'] >= 0 for annotation in nq_example['annotations']]) >= 2


def has_short_answer(nq_example):
    if len(nq_example['annotations']) == 1:
        annotation = nq_example['annotations'][0]
        return annotation['short_answers'] or annotation['yes_no_answer'] != 'NONE'
    else:
        return sum([bool(annotation['short_answers']) or annotation['yes_no_answer'] != 'NONE'
                    for annotation in nq_example['annotations']]) >= 2


def render_answer(nq_example, start_byte, end_byte):
    html = nq_example['document_html'].encode('utf-8')
    answer_text = BeautifulSoup(html[start_byte:end_byte].decode('utf-8'), features='lxml').get_text()
    return answer_text


def get_long_answer(nq_example):
    if has_long_answer(nq_example):
        long_answers = [a['long_answer'] for a in nq_example['annotations'] if a['long_answer']['start_byte'] >= 0]
        long_answer_bounds = [(la['start_byte'], la['end_byte']) for la in long_answers]
        long_answer_counts = [long_answer_bounds.count(la) for la in long_answer_bounds]
        long_answer = long_answers[np.argmax(long_answer_counts)]
        html_tag = nq_example['document_tokens'][long_answer['end_token'] - 1]['token']
        if html_tag == '</P>':
            long_answer_text = render_answer(nq_example, long_answer['start_byte'], long_answer['end_byte'])
            return long_answer_text
    return None


def get_short_answers(nq_example):
    if has_short_answer(nq_example):
        short_answers = [a['short_answers'] for a in nq_example['annotations'] if a['short_answers']]
        short_answers_texts = [
            ', '.join([render_answer(nq_example, s['start_byte'], s['end_byte']) for s in short_answer])
            for short_answer in short_answers]
        short_answers_texts = set(short_answers_texts)
        return short_answers_texts
    return None


def nq_to_squad_format(nq_dir, output_file):
    data = []
    for filename in glob.glob(nq_dir + '/*.gz'):
        with gzip.open(filename, 'r') as f:
            for line in f:
                nq_example = json.loads(line)
                long_answer_text = get_long_answer(nq_example)

                if long_answer_text:
                    question_text = nq_example['question_text']
                    context = long_answer_text
                    para = {'context': context, 'qas': [{'question': question_text, 'answers': []}]}
                    data.append({'paragraphs': [para]})
                    qa = para['qas'][0]
                    qa['id'] = str(nq_example['example_id'])
                    qa['is_impossible'] = True
                    short_answer_texts = get_short_answers(nq_example)

                    if short_answer_texts:
                        for ans_string in short_answer_texts:
                            index = context.find(ans_string)
                            if index != -1:
                                qa['answers'].append({'text': ans_string, 'answer_start': index})
                                qa['is_impossible'] = False

    nq_as_squad = {'data': data, 'version': '2.0'}

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(json.dumps(nq_as_squad, indent=2, sort_keys=True, ensure_ascii=False))


if __name__ == '__main__':
    params = argparse.ArgumentParser()
    params.add_argument('--nq_dir', help='Directory of NQ .gz files')
    params.add_argument('--output_file', help='Output file in SQuAD format')

    args = params.parse_args()

    nq_to_squad_format(args.nq_dir, args.output_file)
