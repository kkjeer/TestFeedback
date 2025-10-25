import logging
import os

from installed_clients.WorkspaceClient import Workspace

# This class is responsible for reading and writing files to the user's workspace.
class FileUtil:
  def __init__(self, config):
    self.config = config
    self.callback_url = os.environ['SDK_CALLBACK_URL']
    self.ws_url = config["workspace-url"]
    self.shared_folder = config['scratch']
    logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                        level=logging.INFO)
    
  # This method reads the string table that was created at the end of running the AppRunner app.
  # For now, it uses the table name and workspace name to (slowly) look up the table file.
  # (See https://github.com/kbaseapps/SpeciesTreeBuilder/blob/dce166f6d1673018a001b750c191b9a2deda0c71/lib/src/workspace/ObjectSpecification.java).
  # TODO: how to get the table_id UI element to pass the table ref rather than the table name to the app?
  def readStringTable(self, ctx, table_name, workspace_name):
    try:
      ws = Workspace(self.ws_url, token=ctx['token'])
      obj = ws.get_objects2({'objects' : [{'name' : table_name, 'find_reference_path': 1, 'workspace': workspace_name}]})
      logging.info(f'read string table: {obj}')
      return obj
    except Exception as e:
      logging.error(f'could not read string table: {e}')
      return None