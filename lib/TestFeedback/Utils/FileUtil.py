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
    
  # This method reads a workspace file using its file ref.
  # This is the preferred way to read files.
  def readFileById(self, ctx, file_ref):
    if file_ref is None or file_ref == '':
      logging.error('cannot read empty file ref')
      return None
    try:
      ws = Workspace(self.ws_url, token=ctx['token'])
      obj = ws.get_objects2({'objects' : [{'ref' : file_ref}]})
      logging.info(f'read file {file_ref}: {obj}')
      return obj
    except Exception as e:
      logging.error(f'could not read file {file_ref}: {e}')
      return None
    
  # This method reads a workspace file using its file name (rather than its ref).
  # (See https://github.com/kbaseapps/SpeciesTreeBuilder/blob/dce166f6d1673018a001b750c191b9a2deda0c71/lib/src/workspace/ObjectSpecification.java).
  def readFileByName(self, ctx, file_name, workspace_name):
    if file_name is None or file_name == '':
      logging.error('cannot read empty file name')
      return None
    try:
      ws = Workspace(self.ws_url, token=ctx['token'])
      obj = ws.get_objects2({'objects' : [{'name' : file_name, 'find_reference_path': 1, 'workspace': workspace_name}]})
      logging.info(f'read file {file_name}: {obj}')
      return obj
    except Exception as e:
      logging.error(f'could not read file {file_name}: {e}')
      return None