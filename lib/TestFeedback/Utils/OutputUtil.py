import logging
import os

# This class is responsible for constructing objects that will be used in output files and reports.
class OutputUtil:
  def __init__(self, config):
    self.config = config
    self.callback_url = os.environ['SDK_CALLBACK_URL']
    self.ws_url = config["workspace-url"]
    self.shared_folder = config['scratch']
    logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                        level=logging.INFO)
    
  # This method creates data that can be written to an AttributeMapping file.
  # Its can be used to output the FBA test runs, annotated with feedback, to a file.
  def createAttributeMappingData(self, output_json):
    rows = list(output_json.keys())
    cols = list(output_json[rows[0]].keys())

    instances = {}
    for key in output_json:
      instances[key] = [str(output_json[key][param]) for param in output_json[key]]
    mapping_data = {
      'attributes': [{'attribute': param, 'source': 'upload', 'unit': ''} for param in cols],
      'instances': instances,
      'ontology_mapping_method': 'User curation'
    }
    return mapping_data
  
  # This method creates a stringified HTML table containing the results of the FBA runs.
  # This table can be appended to the app summary that is displayed to the user.
  def createSummary(self, output_json):
    rows = list(output_json.keys())
    cols = list(output_json[rows[0]].keys())

    # Top row: column names
    summary = "<table>"
    summary += "<tr>"
    for h in cols:
      summary += f'<th style="padding: 5px">{h}</th>'
    summary += "</tr>"

    # Add each row to the table
    for i in range(0, len(rows)):
      row = rows[i]

      # Open new row
      summary += "<tr style=\"border-top: 1px solid #505050;\">"

      # Define the style of each column
      bg = "#f4f4f4" if i % 2 == 1 else "transparent"
      style = f'style="padding: 5px; background-color: {bg};"'

      # Add the value for each column
      for col in output_json[row]:
        summary += f'<td {style}">{output_json[row][col]}</td>'

      # Close row
      summary += "</tr>"

    summary += "</table>"
    return summary