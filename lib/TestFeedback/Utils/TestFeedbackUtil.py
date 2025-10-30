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
  # If the output file format from AppRunner changes to a different media type, this method can be removed.
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
  
  # This method converts the results of reading an AttributeMapping file into a JSON object
  # that can then be manipulated by the rest of the app.
  # If the output file format from AppRunner changes to a different media type, this method can be removed.
  def getFlippedAttributeMappingOutputAsJson(self, mappings):
    if mappings is None:
      return None
    result = {}
    data = mappings['data'][0]['data']
    logging.info(f'mappings data: {json.dumps(data, indent=2)}')

    for i in range(0, len(data['attributes'])):
      r = data['attributes'][i]['attribute']
      row = {}
      for c in data['instances']:
        row[c] = data['instances'][c][i]
      result[r] = row
    return result
  
  # This method converts the results of reading an AttributeMapping file into a JSON object
  # that can then be manipulated by the rest of the app.
  # If the output file format from AppRunner changes to a different media type, this method can be removed.
  def getAttributeMappingOutputAsJson(self, mappings):
    if mappings is None:
      return None
    result = {}
    data = mappings['data'][0]['data']
    logging.info(f'mappings data: {json.dumps(data, indent=2)}')

    for r in data['instances']:
      row = {}
      for i in range(0, len(data['instances'][r])):
        param = data['attributes'][i]['attribute']
        val = data['instances'][r][i]
        row[param] = val
      result[r] = row
    return result
  
  def addFeedbackToFBAOutput(self, output_json, categories):
    if output_json is None:
      return None
    
    result = {}

    rows = list(output_json.keys())

    for i in range(0, len(rows)):
      r = rows[i]
      feedback = self.getFeedbackFromAttributeMapping(r, categories)
      if r != '':
        feedback = self.getFeedbackFromAttributeMapping(r, categories)
        result[r] = {
          **output_json[r],
          'feedback': feedback
        }

    return result
  
  def getFeedbackFromAttributeMapping(self, run, categories):
    for i in range(0, len(categories)):
      run_id = categories[i]['run_id'][0]
      if run_id == run:
        return categories[i]['feedback']
    return 'no feedback provided'
  
  def getFeedbackFromTextBox(self, run, categories):
    # TODO
    return 'No feedback provided'