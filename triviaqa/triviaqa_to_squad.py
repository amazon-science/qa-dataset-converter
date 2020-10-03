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


# Script based on https://github.com/mandarjoshi90/triviaqa/blob/master/utils/convert_to_squad_format.py
# We include functions that are modified from https://github.com/mandarjoshi90/triviaqa/tree/master/utils
# cite: https://github.com/mandarjoshi90/triviaqa/

import os
import argparse
import json
import nltk
from utils.convert_to_squad_format import get_qad_triples
from utils.utils import get_file_contents
from utils.dataset_utils import read_triviaqa_data, get_question_doc_string


def answer_index_in_document(answer, document):
    answer_list = answer['Aliases'] + answer['NormalizedAliases']
    for answer_string_in_doc in answer_list:
        index = document.find(answer_string_in_doc)
        if index != -1:
            return answer_string_in_doc, index
    return answer['NormalizedValue'], -1


def select_relevant_portion(text):
    paras = text.split('\n')
    selected = []
    done = False
    for para in paras:
        sents = sent_tokenize.tokenize(para)
        for sent in sents:
            words = nltk.word_tokenize(sent)
            for word in words:
                selected.append(word)
                if len(selected) >= 800:
                    done = True
                    break
            if done:
                break
        if done:
            break
        selected.append('\n')
    st = ' '.join(selected).strip()
    return st


def triviaqa_to_squad_format(triviaqa_file, data_dir, output_file):
    triviaqa_json = read_triviaqa_data(triviaqa_file)
    qad_triples = get_qad_triples(triviaqa_json)

    data = []

    for triviaqa_example in qad_triples:
        question_text = triviaqa_example['Question']
        text = get_file_contents(os.path.join(data_dir, triviaqa_example['Filename']), encoding='utf-8')
        context = select_relevant_portion(text)

        para = {'context': context, 'qas': [{'question': question_text, 'answers': []}]}
        data.append({'paragraphs': [para]})
        qa = para['qas'][0]
        qa['id'] = get_question_doc_string(triviaqa_example['QuestionId'], triviaqa_example['Filename'])
        qa['is_impossible'] = True
        ans_string, index = answer_index_in_document(triviaqa_example['Answer'], context)

        if index != -1:
            qa['answers'].append({'text': ans_string, 'answer_start': index})
            qa['is_impossible'] = False

    triviaqa_as_squad = {'data': data, 'version': '2.0'}

    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(triviaqa_as_squad, outfile, indent=2, sort_keys=True, ensure_ascii=False)


if __name__ == '__main__':
    params = argparse.ArgumentParser()

    params.add_argument('--triviaqa_file', help='TriviaQA file')
    params.add_argument('--data_dir', help='Wikipedia data directory')
    params.add_argument('--output_file', help='Output file in SQuAD format')

    args = params.parse_args()

    sent_tokenize = nltk.data.load('tokenizers/punkt/english.pickle')

    triviaqa_to_squad_format(args.triviaqa_file, args.data_dir, args.output_file)
