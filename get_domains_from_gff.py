import argparse
from BCBio import GFF
from utils import *


def extract_domains_for_uniprot_id(uniprot_id):
    print('Extracting domains for id {}...'.format(uniprot_id))
    in_file = '{}/{}.gff'.format(features_dir, uniprot_id)
    out_file = '{}/{}.gff'.format(domains_dir, uniprot_id)
    limit_info = dict(gff_type=["Domain"])

    try:
        with open(in_file, 'r') as in_handle:
            records = GFF.parse(in_handle, limit_info=limit_info)
            with open(out_file, "w") as out_handle:
                GFF.write(records, out_handle)
    except Exception as e:
        print("Error getting domains from gff: " + str(e))
        add_to_error_file('error_getting_domains_from_gff', uniprot_id)


parser = argparse.ArgumentParser(description='Extract domains only from feature files.')
parser.add_argument('ids_filename', nargs='?', default='uniprot_ids.txt')
parser.add_argument('features_dir', nargs='?', default='features')
parser.add_argument('domains_dir', nargs='?', default='domains')
args = parser.parse_args()

ids_filename = args.ids_filename
features_dir = args.features_dir
domains_dir = args.domains_dir

make_dir(domains_dir)
do_per_line(ids_filename, extract_domains_for_uniprot_id)
