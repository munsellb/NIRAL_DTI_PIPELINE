# NIRAL_DTI_PIPELINE

There are two ways to run the pipeline: using the single-process version or using the multi-process version. To run the single process version from the command line type:

```python
python dti_pipeline.py –config config_pipeline.txt
```

and to run the the multi-process version form the command line type:

_ python dti_pipeline_mp.py –config config_pipeline.txt

The configuration file defines where the subject folder is located, a list that defines the subjects to be processed, and the locations of the Autoseg computation and parameter files. Example configuration files and the autoseg template files can be found in the gitbub repository. 


