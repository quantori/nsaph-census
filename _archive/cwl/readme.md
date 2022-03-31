# NSAPH Data Platform CWL Workflow Storage

## Directory Structure

- `cwl_tools`: 
  - Directory for storing CWL tools + workflows for pipelines. 
  Each general workflow should have it's own directory (i.e. census CWL tools will be 
  stored in the `census` directory). Tools intended to be shared across pipelines
  should be stored in the `shared` directory. Each pipeline directory should
  have a short readme describing each tool in the pipeline.
- `pipelines`:
  - This directory stores inputs and cwl parameter YAML files for use with the previous workflows.
  Each execution of a workflow should have its own directory. For example, the census
  pipeline for county data (YAML file, variable description file, and qc description file) should be 
  stored in a directory named `census_county`, while the zcta execution (despite using the same source
  workflow) should be stored in a directory named `census_zcta`.
- `src`: 
  - This directory contains the code executed by workflows. Each workflow should store all scripts
  called by its tools in a directory with the same name as the workflow directory. Shared
  modules and scripts should be stored in a directory named `shared`. Modules intended to
  serve as libraries should be written as stand alone packages and be installed in the execution environment.

## TODO

- Determine how to specify software environment for each workflow, especially those
  with GIS dependencies


