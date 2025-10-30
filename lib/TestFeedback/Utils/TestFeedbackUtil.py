import logging
import os
import json

# This class is responsible for manipulating data from FBA runs and user-provided feedback.
class TestFeedbackUtil:
  def __init__(self, config):
    self.config = config
    self.callback_url = os.environ['SDK_CALLBACK_URL']
    self.ws_url = config["workspace-url"]
    self.shared_folder = config['scratch']
    logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                        level=logging.INFO)
    
  # This method converts the results of reading a StringDataTable file into a JSON object
  # that can then be manipulated by the rest of the app.
  # If the output file format from AppRunner changes to a different media type, this method should be updated.
  def getStringDataTableOutputAsJson(self, table):
    if table is None:
      return None
    result = {}
    data = table['data'][0]['data']
    logging.info(f'table data: {json.dumps(data, indent=2)}')

    for i in range(0, len(data['row_labels'])):
      key = data['row_labels'][i]
      obj = {}
      d = data['data'][i]
      for j in range(0, len(d)):
        label = data['column_labels'][j]
        obj[label] = d[j]
      result[key] = obj
    return result
  
  def getAttributeMappingOutputAsJson(self, mappings):
    if mappings is None:
      return None
    result = {}
    data = mappings['data'][0]['data']
    logging.info(f'mappings data: {json.dumps(data, indent=2)}')

    for r in mappings['instances']:
      row = {}
      for i in range(0, len(mappings['instances'][r])):
        param = mappings['attributes'][i]['attribute']
        val = mappings['instances'][r][i]
        row[param] = val
      result[r] = {}
    return result
  
  def addFeedbackToFBAOutput(self, output_json, categories):
    if output_json is None:
      return None
    
    result = {}

    rows = list(output_json.keys())

    for i in range(0, len(categories)):
      run = categories[i]['test_run']
      row = ''
      # User entered an index in the test_run field
      if run == str(i):
        row = rows[i]
      # User left the test_run field blank - default to the index in the set of categories
      elif run == '':
        row = rows[i]
      # User entered something else in the test_run field - look through the app runner output
      # to see if their input matches an fba_output_id for any FBA run
      else:
        for r in rows:
          if run == output_json[r]['fba_output_id']:
            row = r
            break
      if row != '':
        result[row] = {
          **output_json[row],
          'feedback': categories[i]['feedback']
        }

    return result