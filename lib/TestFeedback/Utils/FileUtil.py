import logging
import os

from installed_clients.WorkspaceClient import Workspace
from installed_clients.DataFileUtilClient import DataFileUtil

# This class is responsible for reading and writing files to the user's workspace.
class FileUtil:
  def __init__(self, config):
    self.config = config
    self.callback_url = os.environ['SDK_CALLBACK_URL']
    self.ws_url = config["workspace-url"]
    self.shared_folder = config['scratch']
    logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                        level=logging.INFO)
    
  # This method reads the string table that was created at the end of running the AppRunner app
  def readStringTable(self, ctx, table_ref):
    try:
      ws = Workspace(self.ws_url, token=ctx['token'])
      obj = ws.get_objects2({'objects' : [{'ref' : table_ref}]})
      logging.info(f'read string table: {obj}')
      return obj
    except Exception as e:
      logging.error(f'could not read string table: {e}')
      return None