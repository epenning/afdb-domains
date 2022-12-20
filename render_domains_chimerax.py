import os
import seaborn as sns
from BCBio import GFF
from chimerax.core.commands import run
from datetime import datetime

# Configurable Variables ----------------------------------------------------

# Filepath for file containing uniprot IDs, one on each line
PATH_TO_UNIPROT_IDS = 'uniprot_ids.txt'

# Filepath patterns for structure and domains (the {} will get replaced with the protein name/id)
PATH_TO_STRUCTURE_PATTERN = 'afdb/{}.cif'
PATH_TO_DOMAINS_PATTERN = 'domains/{}.gff'

# Filepath patterns for outputs (the {} will get replaced with the protein name/id)
FOLDER_TO_SAVE_IN = "chimerax"
PATH_TO_SAVE_SNAPSHOT = FOLDER_TO_SAVE_IN + "/{}.png"
PATH_TO_SAVE_SESSION = FOLDER_TO_SAVE_IN + "/{}.cxs"
PATH_TO_SAVE_LOG = FOLDER_TO_SAVE_IN + "/{}_log.html"

# Seaborn palette - change this to use a particular color palette
SEABORN_PALETTE = 'colorblind'

# ----------------------------------------------------------------------------


# Duplicated from utils.py
def add_to_error_file(error, to_add):
    filename = datetime.now().strftime("{}-%Y_%m_%d-%I_%M_%S_%p.txt").format(error)
    with open(filename, 'a') as error_file:
        error_file.write(to_add + "\n")


# Create output directory
if not os.path.exists(FOLDER_TO_SAVE_IN):
    os.mkdir(FOLDER_TO_SAVE_IN)

# Read IDs of proteins
with open(PATH_TO_UNIPROT_IDS) as ids_file:
    uniprot_ids = [line.rstrip() for line in ids_file]

# Render each protein in ChimeraX
for uniprot_id in uniprot_ids:
    # Chimera X
    run(session, 'close session')
    run(session, 'log clear')

    try:
        structure_filepath = PATH_TO_STRUCTURE_PATTERN.format(uniprot_id)
        opened_models = run(session, 'open ' + structure_filepath)

        # Color all white
        run(session, 'color white')

        # Read features
        domains_filepath = PATH_TO_DOMAINS_PATTERN.format(uniprot_id)
        with open(domains_filepath, 'r') as domains_file:
            # Expect only one record with potential features
            domains_record = next(GFF.parse(domains_file))

        # Get locations of just domains
        domains = []
        for feature in domains_record.features:
            # Only color domains
            if feature.type != 'Domain':
                continue
            domains.append((feature.location.start, feature.location.end))

        # Generate color palette for number of domains
        palette = iter(sns.color_palette(SEABORN_PALETTE, len(domains)).as_hex())

        # Color the domains
        for domain in domains:
            color = next(palette)
            run(session, 'color #1:{}-{} {}'.format(domain[0], domain[1], color))

        # Other display settings
        run(session, 'set bgColor white')
        run(session, 'lighting soft depthCue false')
        run(session, 'lighting model #3 directional false shadows false')
        run(session, 'graphics silhouettes true width 2')
        run(session, 'view clip false')

        # Save Results
        snapshot_path = PATH_TO_SAVE_SNAPSHOT.format(uniprot_id)
        session_path = PATH_TO_SAVE_SESSION.format(uniprot_id)
        log_path = PATH_TO_SAVE_LOG.format(uniprot_id)

        run(session, 'save {} supersample 3'.format(snapshot_path))
        run(session, 'save {} format session'.format(session_path))
        run(session, 'log save {}'.format(log_path))
    except Exception as e:
        add_to_error_file('error_rendering_chimerax', uniprot_id)
