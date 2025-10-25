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
  def getAppRunnerOutputAsJson(self, table):
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