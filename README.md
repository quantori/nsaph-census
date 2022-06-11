# NSAPH Census Pipelines
 
A Python Module for easy specification of custom census data sets.

To run pipelines use [cwl-tool](https://github.com/common-workflow-language/cwltool).

How to run pipelines with sample parameters:
1. Request for API key [here](https://api.census.gov/data/key_signup.html)
2. Write API key in parameter `api_key` into
   [county_workflow.yml](src/cwl/pipelines/census_county/county_workflow.yml)
    and [zcta_workflow.yml](src/cwl/pipelines/census_zcta/zcta_workflow.yml)
3. Adjust other options in those config files
4. Run command
```
cwl-runner census_workflow.cwl pipelines/census_county/county_workflow.yml

cwl-runner census_workflow.cwl pipelines/census_zcta/zcta_workflow.yml
```

## Change Log

#### Version 0.3 June 2021:
Logging in place instead of print statements, successful complete runs with CWL.
Some user + code documentation, support for commonly used geographies.
