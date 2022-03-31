#! cwl-runner

cwlVersion: v1.1
class: CommandLineTool
baseCommand: [python, -m, shared.csv_qc]
requirements:
  EnvVarRequirement:
    envDef:
      PYTHONPATH: $(inputs.PYTHONPATH)

inputs:
  PYTHONPATH:
    type: string
    default: "/Users/mbs641/Documents/rse_work/cwl_workflows/src"
  csv_file:
    type: File
    inputBinding:
      prefix: --csv_file
  qc_log:
    type: string
    default: "qc_log.log"
    inputBinding:
      prefix: --qc_log
  qc_file:
    type: File
    default:
      class: File
      location: "qc.yml"
    inputBinding:
      prefix: --qc_file
  name:
    type: string?
    inputBinding:
      prefix: --name
  log:
    type: File?
    inputBinding:
      prefix: --log

outputs:
  qc_log:
    type: File
    outputBinding:
      glob: $(inputs.qc_log)
