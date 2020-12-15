# QA Dataset Converter

In this repository, we release code from the paper [What do Models Learn from Question Answering Datasets?](https://arxiv.org/abs/2004.03490) by Priyanka Sen and Amir Saffari. 

These scripts convert four popular question answering datasets into a common format based on SQuAD 2.0 to allow for easier probing and experimentation. An example of a question in the SQuAD 2.0 format is shown below:
  
```
{
  "context": "The Normans were the people who in the 10th and 11th centuries..."
  "qas": [
    {
      "question": "In what country is Normandy located?",
      "id": "56ddde6b9a695914005b9628",
      "answers": [
        {
          "text": "France",
          "answer_start": 159
        }
      ],
      "is_impossible": false
    }
...
```

In the following sections, we guide you through converting TriviaQA, Natural Question, QuAC, and NewsQA into a SQuAD 2.0 format.

---
## TriviaQA

**Step 1**

Clone this repo and go into the TriviaQA directory.

```
cd qa-dataset-converter/triviaqa
```

**Step 2**

Download the TriviaQA dataset from https://nlp.cs.washington.edu/triviaqa/ This will include a *qa* directory with question-answer files and an *evidence* containing the documents for context.

**Step 3**

Clone the TriviaQA repo.

```
git clone https://github.com/mandarjoshi90/triviaqa
```

**Step 4**

Move our triviaqa_to_squad.py script into the TriviaQA repo.

```
mv triviaqa_to_squad.py  triviaqa/
```

**Step 5**

Set *--triviaqa_file* to a file in your *qa* directory and *--data_dir* to the Wikipedia path in your *evidence* directory. Run:

```
python triviaqa_to_squad.py --triviaqa_file qa/wikipedia-train.json --data_dir evidence/wikipedia/ --output_file triviaqa_train.json

python triviaqa_to_squad.py --triviaqa_file qa/wikipedia-dev.json --data_dir evidence/wikipedia/ --output_file triviaqa_dev.json
```

This will return two files **triviaqa_train.json** and **triviaqa_dev.json** in the SQuAD 2.0 format.


---
## Natural Questions

**Step 1**

Clone this repo and go into the Natural Questions directory.

```
cd qa-dataset-converter/nq
```

**Step 2**

Download the Natural Questions dataset from https://ai.google.com/research/NaturalQuestions/download This will download *train* and *dev* directories of jsonl.gz files.


**Step 3**

Set *--nq_dir* to your Natural Questions train or dev directory. Run:

```
python nq_to_squad.py --nq_dir train/ --output_file nq_train.json

python nq_to_squad.py --nq_dir dev/ --output_file nq_dev.json
```

This will return two files **nq_train.json** and **nq_dev.json** in the SQuAD 2.0 format.

---
## QuAC

**Step 1**

Clone this repo and go into the QuAC directory

```
cd qa-dataset-converter/quac
```

**Step 2**

Download the QuAC dataset from https://quac.ai/

**Step 3**

Set *--quac_file* to the path of your QuAC train or dev file. Run:

```
python quac_to_squad.py --quac_file train_v0.2.json --output_file quac_train.json

python quac_to_squad.py --quac_file val_v0.2.json --output_file quac_dev.json
```

This will return two files **quac_train.json** and **quac_dev.json** in the SQuAD 2.0 format.

---
## NewsQA

**Step 1**

Clone this repo and go into the NewsQA directory

```
cd qa-dataset-converter/newsqa
```

**Step 2**

Follow the instructions at https://github.com/Maluuba/newsqa to build the NewsQA dataset. This will result in a directory called *split_data* with train, dev, and test CSVs.

**Step 3**

Note: If you used a Python 2.7 conda environment to set up NewsQA, make sure to deactivate your environment before this step.

Set *--newsqa_file* to the path of a NewsQA file in the *split_data* directory. Run:

```
python newsqa_to_squad.py --newsqa_file split_data/train.csv --output_file newsqa_train.json

python newsqa_to_squad.py --newsqa_file split_data/dev.csv --output_file newsqa_dev.json
```

---
## Acknowledgements

Our TriviaQA script modifies code released in [TrivaiQA repo](https://github.com/mandarjoshi90/triviaqa/) In particular, we take inspiration from [convert_to_squad_format.py](https://github.com/mandarjoshi90/triviaqa/blob/master/utils/convert_to_squad_format.py) for all our scripts.

We also use modified code from the [Nautral Question browser script](https://github.com/google-research-datasets/natural-questions/blob/master/nq_browser.py) to process Natural Questions examples.

We are thankful to the authors for making this code available. 

---
## License

This code is licensed under the Apache License, Version 2.0.

---
## Citation
If you use our code, please cite us!

```
@inproceedings{sen-saffari-2020-models,
    title = "What do Models Learn from Question Answering Datasets?",
    author = "Sen, Priyanka  and
      Saffari, Amir",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.emnlp-main.190",
    doi = "10.18653/v1/2020.emnlp-main.190",
    pages = "2429--2438",
}

```
