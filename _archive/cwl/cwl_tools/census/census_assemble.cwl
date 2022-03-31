#! cwl-runner

cwlVersion: v1.2
class: CommandLineTool
baseCommand: [python, -m, census.assemble_data]
requirements:
  EnvVarRequirement:
    envDef:
      PYTHONPATH: $(inputs.PYTHONPATH)
      GET_CENSUS_API_KEY: $(inputs.api_key)
      HTTPS_PROXY: $(inputs.http_proxy)
      HTTP_PROXY: $(inputs.http_proxy)
  NetworkAccess:
    networkAccess: true

inputs:
  PYTHONPATH:
    type: string
    default: "/Users/mbs641/Documents/rse_work/learning/cwl/src"
  http_proxy:
    type: string
    default: ""
  api_key:
    type: string
  var_file:
    type: File
    inputBinding:
      prefix: --var_file
  geometry:
    type: string
    inputBinding:
      prefix: --geom
  years:
    type: string
    default: "1999:2019"
    inputBinding:
      prefix: --years
  log:
    type: File
    default:
      class: File
      location: census.log
    inputBinding:
      prefix: --log
  pkl_file:
    type: string
    default: "census.pkl"
    inputBinding:
      prefix: --pkl_file
  state:
    type: string?
    inputBinding:
      prefix: --state
  county:
    type: string?
    inputBinding:
      prefix: --county


outputs:
  pkl:
    type: File
    outputBinding:
      glob: $(inputs.pkl_file)

