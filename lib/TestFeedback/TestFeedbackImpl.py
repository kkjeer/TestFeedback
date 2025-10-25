# -*- coding: utf-8 -*-
#BEGIN_HEADER
# The header block is where all import statments should live
import logging
import os
from pprint import pformat

from Utils.FileUtil import FileUtil

from installed_clients.KBaseReportClient import KBaseReport
#END_HEADER


class TestFeedback:
    '''
    Module Name:
    TestFeedback

    Module Description:
    A KBase module: TestFeedback
Gathers feedback on test runs of flux balance analysis.
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = ""

    #BEGIN_CLASS_HEADER
    # Class variables and functions can be defined in this block
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        
        # Any configuration parameters that are important should be parsed and
        # saved in the constructor.
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def run_TestFeedback(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_TestFeedback

        # Print statements to stdout/stderr are captured and available as the App log
        logging.info('Starting run_TestFeedback function. Params=' + pformat(params))

        # Create utilities
        fileUtil = FileUtil(self.config)

        # Read the string data table created from AppRunner
        table = fileUtil.readStringTable(params["table_id"])
        if table is not None:
          logging.info(f'got string data table')

        # Build a Report and return
        reportObj = {
          'objects_created': [],
          'text_message': 'Done running app'
        }
        report = KBaseReport(self.callback_url)
        report_info = report.create({'report': reportObj, 'workspace_name': params['workspace_name']})

        # Contruct the output to send back
        output = {'report_name': report_info['name'],
                  'report_ref': report_info['ref']
                  }
        logging.info('returning:' + pformat(output))
                
        #END run_TestFeedback

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_TestFeedback return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
