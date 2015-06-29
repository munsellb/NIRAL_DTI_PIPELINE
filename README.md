# NIRAL_DTI_PIPELINE

Scripts required to run this pipeline:

    niral_dti_system.py
    dwi_to_dti.py
    nonrigid_registration.py
    warp_image.py
    fdt_bedpost.py
    extract_brain_region.py
    create_fdt_masks.py
    fdt_probtrackx2.py

It is possible to run each of these scripts separately. Use the helper to get more information. *example: python warp_image.py --help

Other files required:

    subjects.txt - It is a list file that contains in each line a path that points to a subject folder
    config_global_system.txt - this is the config file required in order to run he niral_sti_system.py script

