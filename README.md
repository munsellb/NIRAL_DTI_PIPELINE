# NIRAL_DTI_PIPELINE

<h3> Table of contents </h3>
<ol>
<li><a href="https://github.com/munsellb/NIRAL_DTI_PIPELINE/blob/master/README.md#pipeline-flow-diagram">Pipeline flow diagram</a></li>
<li><a href="https://github.com/munsellb/NIRAL_DTI_PIPELINE/blob/master/README.md#configuring-and-running-the-pipeline">Pipeline flow diagram</a></li>
</ol>

<h3>Pipeline flow diagram</h3>

!["flow diagram"](https://github.com/munsellb/NIRAL_DTI_PIPELINE/blob/master/pipeline_img.png)

The flow diagram shown above represents the single-process pipeline version. The major difference between the multi-process and single-process version is the multi-process version computes all the seed regions in parallel (i.e. does not include a loop that sequentially processes each seed region).

As illustrated, the pipeline defines six components that perform the sequence of operations listed below:
<ol>
<li><b>DWI to DTI:</b> This takes the skull stripped DWI image and creates a DTI, RD, AD, FA, and DWI-b0 image volume.</li>
<li><b>AutoSeg:</b> Creates a white matter, gray matter, and CSF segmentations using the Imperial atlas and the T1 and T2 images.</li>
<li><b>FDT masks:</b> Creates the masks required to run FDT bedpost and probtrack. Specifically,</li>
    <ul>
    <li>no_diff_brain mask</li>
    <li>waypoint mask</li>
    <li>exclusion mask</li>
    <li>seed masks (one for each brain region defined in Imperial parcellation)</li>
    <li>termination masks (one for each brain region defined in Imperial parcellation)</li>
    </ul>
<li><b>FDT bedpost:</b> Execute the FDT Bayesian Estimation of Diffusion Parameters Obtained using Sampling Techniques (bedpostx) algorithm that includes modeling for crossing fibers.</li>
<li><b>FDT probtrack:</b> Execute the FDT probabilistic tracking with crossing fibers (probtrackx) algorithm for each seed region.</li>
<li><b>Connectome:</b> Create NxN connectivity matrix using output of probtrack results.</li>
</ol>

<h3>Configuring and running the pipeline</h3>

There are two ways to run the pipeline: using the single-process version or using the multi-process version. To run the single process version from the command line type:

```python
python dti_pipeline.py –config config_pipeline.txt
```

and to run the the multi-process version form the command line type:

```python
python dti_pipeline_mp.py –config config_pipeline.txt
```

In general, the configuration file defines where the subject folder is located, a list that includes the subjects to be processed, the locations of the Autoseg computation and parameter files, and the pipeline components to be executed. For instance, on a Linux/UNIX/Mac operating system if the study folder is located at

```
/data/study_subjects
```

and in this folder the following sub-folders (typically named using subject specific unique ids) 

```
subject_id1
subject_id2
subject_id3
subject_id4
```
The subjects.txt file could be created using the command ```ls > subjects.txt```. Then the dti pipeline configuration file would have the following key-value pairs.

```
SubjectFolder:/data/study_subjects
SubjectList:/data/study_subjects/subjects.txt
```

For the autoseg template and pipeline component flag files, if the git rep was cloned in folder ```/data/git/NIRAL_DTI_PIPELINE``` then the dti pipeline configuration file would have the following key-value pairs.

```
COMPFILE:/data/git/NIRAL_DTI_PIPELINE/autoseg_templates/AutoSeg_Computation.txt
PARMFILE:/data/git/NIRAL_DTI_PIPELINE/autoseg_templates/AutoSeg_Parameters.txt
Flags:/data/git/NIRAL_DTI_PIPELINE/example_config/config_pipeline_flags.txt
```
In general, the flag file indicates the pipeline components to be executed. A ```yes``` value indicates the component will be executed, and a ```no``` value indicates the component will not be executed.

Example <a href="https://github.com/munsellb/NIRAL_DTI_PIPELINE.git/example_config">configuration files</a> and <a href="https://github.com/munsellb/NIRAL_DTI_PIPELINE.git/autoseg_templates">autoseg template</a> files can be found in the github repository. 


