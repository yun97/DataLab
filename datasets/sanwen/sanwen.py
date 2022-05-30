# coding=utf-8
# Copyright 2020 The TensorFlow datasets Authors and the HuggingFace datasets, DataLab Authors.
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

import csv
import datalabs
from datalabs import get_task, TaskType

_DESCRIPTION = """
SanWen is a discourse-level named entity recognition and relation extraction dataset for chinese literature text. 
"""
_CITATION = """\
@inproceedings{dnerre,
    author = {Jingjing Xu and Ji Wen and Xu Sun and Qi Su},
    title = {A Discourse-Level Named Entity Recognition and Relation Extraction Dataset for Chinese Literature Text},
    journal = {CoRR},
    volume = {abs/1711.07010},
    year = {2017},
    url = http://arxiv.org/abs/1711.07010
}
"""

_LICENSE = "NA"

_TRAIN_DOWNLOAD_URL = "http://cdatalab1.oss-cn-beijing.aliyuncs.com/relation_extraction/SanWen/train.txt"
_VALIDATION_DOWNLOAD_URL = "http://cdatalab1.oss-cn-beijing.aliyuncs.com/relation_extraction/SanWen/valid.txt"
_TEST_DOWNLOAD_URL = "http://cdatalab1.oss-cn-beijing.aliyuncs.com/relation_extraction/SanWen/test.txt"

_HOMEPAGE = "https://github.com/lancopku/Chinese-Literature-NER-RE-Dataset"


class SanWenConfig(datalabs.BuilderConfig):

    def __init__(self, **kwargs):
        super(SanWenConfig, self).__init__(**kwargs)


class SanWen(datalabs.GeneratorBasedBuilder):

    BUILDER_CONFIGS = [
        SanWenConfig(
            name="Relation Extraction",
            version=datalabs.Version("1.0.0"),
            description="Relation Extraction",
        ),
    ]

    DEFAULT_CONFIG_NAME = "Relation Extraction"

    def _info(self):

        return datalabs.DatasetInfo(
            description=_DESCRIPTION,
            features=datalabs.Features(
                {
                    "head": datalabs.Value("string"),
                    "link": datalabs.Value("string"),
                    "tail": datalabs.Value("string"),
                    "text": datalabs.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
            languages=["zh"],
            task_templates=[get_task(TaskType.kg_link_tail_prediction)(
                head_column = "head",
                link_column = "link",
                tail_column = "tail",
            ),
            ],
        )

    def _split_generators(self, dl_manager):

        train_path = dl_manager.download_and_extract(_TRAIN_DOWNLOAD_URL)
        validation_path = dl_manager.download_and_extract(_VALIDATION_DOWNLOAD_URL)
        test_path = dl_manager.download_and_extract(_TEST_DOWNLOAD_URL)
        
        return [
            datalabs.SplitGenerator(name=datalabs.Split.TRAIN, gen_kwargs={"filepath": train_path}),
            datalabs.SplitGenerator(name=datalabs.Split.VALIDATION, gen_kwargs={"filepath": validation_path}),
            datalabs.SplitGenerator(name=datalabs.Split.TEST, gen_kwargs={"filepath": test_path}),
        ]

    def _generate_examples(self, filepath):

        with open(filepath, encoding="utf-8") as txt_file:
            txt_file = csv.reader(txt_file, delimiter='\t')
            for id_, row in enumerate(txt_file):
                if len(row) == 4:
                    head, tail, link, text = row
                    yield id_, {"head": head, "tail":tail, "link": link, "text": text}