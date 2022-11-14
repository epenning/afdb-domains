import argparse
from utils import *

GFF_URL = 'https://rest.uniprot.org/uniprotkb/{}.gff'


def download_uniprot_features_by_id(uniprot_id):
    download_features_to = "{}/{}.gff".format(download_dir, uniprot_id)
    if os.path.exists(download_features_to):
        print('Skipping id {}, already downloaded'.format(uniprot_id))
        return
    try:
        print('Requesting features for id {}...'.format(uniprot_id))
        features_url = GFF_URL.format(uniprot_id)
        download_to(features_url, download_features_to)
        print("Finished downloading features for id {}".format(uniprot_id))
    except Exception as e:
        print("Error while downloading: " + str(e))
        add_to_error_file("error_downloading_domains_from_uniprot", uniprot_id)


parser = argparse.ArgumentParser(description='Download feature files from Uniprot by IDs.')
parser.add_argument('ids_filename', nargs='?', default='uniprot_ids.txt')
parser.add_argument('download_dir', nargs='?', default='features')
args = parser.parse_args()

ids_filename = args.ids_filename
download_dir = args.download_dir

make_dir(download_dir)
do_per_line(ids_filename, download_uniprot_features_by_id)
