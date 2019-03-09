import csv
import logging
from typing import List
from xml.etree import ElementTree

from utils.data_helper import get_phrases_and_nodes
from utils.data_structures import UFDS
from utils.feature_extractors import PairSyntacticFeatureExtractor
from utils.training_instances_generator import TrainingInstancesGenerator, BudiInstancesGenerator, \
    SoonInstancesGenerator, GilangInstancesGenerator


def save_mention_pair_features(mention_pairs: List[dict], output_file: str) -> None:
    if len(mention_pairs) == 0:
        return

    with open(output_file, 'w') as f:
        csv_file = csv.DictWriter(f, fieldnames=mention_pairs[0].keys())
        csv_file.writeheader()
        csv_file.writerows(mention_pairs)


def extract_mention_pair_features(input_file: str, instances_generator: TrainingInstancesGenerator) -> List[dict]:
    data = ElementTree.parse(input_file)
    root = data.getroot()
    parent_map = {c: p for p in root.iter() for c in p}

    logging.info('Getting phrases and nodes list')
    ufds = UFDS()
    phrases, nodes, phrase_id_by_node_id = get_phrases_and_nodes(ufds, root)

    feature_extractor = PairSyntacticFeatureExtractor(
        parent_map=parent_map,
        phrases=phrases,
        phrase_id_by_node_id=phrase_id_by_node_id
    )

    logging.info('Generating training instances')
    training_node_ids = list(ufds.nodes)
    training_instances = instances_generator.generate(training_node_ids, ufds)

    logging.info('Extracting mention pairs features')
    mention_pairs = [
        {
            'm1_id': instance[0],
            'm2_id': instance[1],
            **feature_extractor.get_features(nodes[instance[0]], nodes[instance[1]]),
            'is_coreference': instance[2],
        }
        for instance in training_instances
    ]

    return mention_pairs


def main() -> None:
    training_instances_generators = [
        ('soon', SoonInstancesGenerator()),
        ('gilang', GilangInstancesGenerator()),
        ('budi', BudiInstancesGenerator())
    ]

    for name, generator in training_instances_generators:
        logging.info('Extracting features using %s\'s training instances generator...' % name)
        mention_pairs = extract_mention_pair_features('data/training/data.xml', generator)

        logging.info('Saving features using %s\'s training instances generator...' % name)
        save_mention_pair_features(mention_pairs, 'data/training/mention_pairs_%s.csv' % name)

    logging.info('Extracting testing data features...')
    mention_pairs = extract_mention_pair_features('data/testing/data.xml', BudiInstancesGenerator())

    logging.info('Saving testing data features...')
    save_mention_pair_features(mention_pairs, 'data/testing/mention_pairs.csv')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    main()
