from DIRAC.Resources.Computing.ComputingElementFactory import ComputingElementFactory
from DIRAC.WorkloadManagementSystem.Utilities.Utils import createJobWrapper
from DIRAC.Core.Security.ProxyInfo import getProxyInfo

from DIRAC import gLogger
import unittest

class JobWrapperTestCase( unittest.TestCase ):
  """ Base class for the jobWrapper test cases
  """

  def setUp( self ):
    gLogger.setLevel( 'DEBUG' )
    self.wrapperFile = None

    # get proxy
    proxyInfo = getProxyInfo( disableVOMS = True )
    proxyChain = proxyInfo['Value']['chain']
    proxyDumped = proxyChain.dumpAllToString()
    self.payloadProxy = proxyDumped['Value']

  def tearDown( self ):
    pass

class JobWrapperSubmissionCase( JobWrapperTestCase ):
  """  JobWrapperSubmissionCase represents a test suite for
  """

  def test_CreateAndSubmit( self ):

    jobParams = {'JobID': '1',
                 'JobType': 'Merge',
                 'CPUTime': '1000000',
                 'Executable': '$DIRACROOT/scripts/dirac-jobexec',
                 'Arguments': "helloWorld.xml -o LogLevel=DEBUG",
                 'InputSandbox': ['helloWorld.xml', 'exe-script.py']}
    resourceParams = {}
    optimizerParams = {}

#     res = createJobWrapper( 1, jobParams, resourceParams, optimizerParams, logLevel = 'DEBUG' )
#     self.assert_( res['OK'] )
#     wrapperFile = res['Value']

    ceFactory = ComputingElementFactory()
    ceInstance = ceFactory.getCE( 'InProcess' )
    self.assert_( ceInstance['OK'] )
    computingElement = ceInstance['Value']

#     res = computingElement.submitJob( wrapperFile, self.payloadProxy )
#     self.assert_( res['OK'] )

    res = createJobWrapper( 2, jobParams, resourceParams, optimizerParams, extraOptions = 'extra.cfg', logLevel = 'DEBUG' )
    self.assert_( res['OK'] )
    wrapperFile = res['Value']

    res = computingElement.submitJob( wrapperFile, self.payloadProxy )
    self.assert_( res['OK'] )


if __name__ == '__main__':
  suite = unittest.defaultTestLoader.loadTestsFromTestCase( JobWrapperTestCase )
  suite.addTest( unittest.defaultTestLoader.loadTestsFromTestCase( JobWrapperSubmissionCase ) )
  testResult = unittest.TextTestRunner( verbosity = 2 ).run( suite )
