import argparse
import json
import re
from utils import *

BEACONS_URL = 'https://www.ebi.ac.uk/pdbe/pdbe-kb/3dbeacons/api/v1/uniprot/summary/{}.json?provider=alphafold'


def download_by_uniprot_id(uniprot_id):
    download_summary_to = "{}/{}_summary.json".format(download_dir, uniprot_id)
    download_model_to = "{}/{}.cif".format(download_dir, uniprot_id)
    download_pae_json_to = "{}/{}_PAE.json".format(download_dir, uniprot_id)
    download_pae_png_to = "{}/{}_PAE.png".format(download_dir, uniprot_id)
    if os.path.exists(download_model_to) \
            and os.path.exists(download_pae_json_to) \
            and os.path.exists(download_pae_png_to) \
            and os.path.exists(download_summary_to):
        print('Skipping id {}, already downloaded'.format(uniprot_id))
        return
    print('Requesting summary for id {}...'.format(uniprot_id))
    summary_response = requests.get(BEACONS_URL.format(uniprot_id))
    print(summary_response)
    if not summary_response.ok:
        print('Cannot access id {} in AFDB'.format(uniprot_id))
        add_to_error_file("not_in_afdb", uniprot_id)
        return
    response_json = summary_response.json()
    for key, value in response_json.items():
        print(key, ':', value)
    with open(download_summary_to, "w") as summary_file:
        summary_file.write(json.dumps(summary_response.json()))
    model_url = response_json['structures'][0]['model_url']
    print(model_url)
    try:
        download_to(model_url, download_model_to)
        pae_json_url = re.sub('.cif', '.json', model_url.replace('model', 'predicted_aligned_error'))
        download_to(pae_json_url, download_pae_json_to)
        pae_png_url = re.sub('.json', '.png', pae_json_url)
        download_to(pae_png_url, download_pae_png_to)
        print("Finished downloading id {}".format(uniprot_id))
    except Exception as e:
        print("Error while downloading: " + str(e))
        add_to_error_file("error_downloading_from_afdb", uniprot_id)


parser = argparse.ArgumentParser(description='Download Alphafold DB structures from 3D Beacons by Uniprot IDs.')
parser.add_argument('ids_filename', nargs='?', default='uniprot_ids.txt')
parser.add_argument('download_dir', nargs='?', default='afdb')
args = parser.parse_args()

ids_filename = args.ids_filename
download_dir = args.download_dir

make_dir(download_dir)
do_per_line(ids_filename, download_by_uniprot_id)
