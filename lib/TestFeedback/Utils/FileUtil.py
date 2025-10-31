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
    
  # This is a helper method for writing a file to the workspace.
  def writeFile(self, ctx, params, data, name, type, description):
    try:
      ws = Workspace(self.ws_url, token=ctx['token'])
      save_result = ws.save_objects(
         {
           'workspace': params['workspace_name'],
           'objects': [
              {
                'name': name,
                'type': type,
                'data': data,
              }
            ]
          })
      logging.info(f'saved file {name} of type {type}: {save_result}')
      id = save_result[0][0]
      version = save_result[0][4]
      workspace_id = save_result[0][6]
      ref = f'{workspace_id}/{id}/{version}'
      return {'ref': ref, 'description': description}
    except Exception as e:
      logging.error(f'failed to save file {name} of type {type}: {e}')
      return None
  
  # This method writes an attribute mapping file to the workspace.
  # It can be used to save the annotated FBA run results.
  def writeAttributeMappingFile(self, ctx, params, mapping_data, file_name):
    name = file_name or 'test-feedback-output' 
    return self.writeFile(ctx, params, mapping_data, name, 'KBaseExperiments.AttributeMapping', 'test results with feedback')