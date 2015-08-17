# NIRAL_DTI_PIPELINE

There are two ways to run the pipeline: using the single-process version or using the multi-process version. To run the single process version from the command line type:

```python
python dti_pipeline.py –config config_pipeline.txt
```

and to run the the multi-process version form the command line type:

```python
python dti_pipeline_mp.py –config config_pipeline.txt
```

In general, the configuration file defines where the subject folder is located, a list that includes only the subjects to be processed, and the locations of the Autoseg computation and parameter files. Example <a href="https://github.com/munsellb/NIRAL_DTI_PIPELINE.git/example_config">configuration files</a> and the autoseg template files can be found in the github repository. 


