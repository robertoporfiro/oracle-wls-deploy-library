######################################################################################################
#
# Author: Roberto Porfiro (roberto.porfiro@timestamp.pt)
# Created: 2018/06/20
######################################################################################################

import sys
import javax
import os
from weblogic.descriptor import BeanAlreadyExistsException
from java.lang.reflect import UndeclaredThrowableException
from java.lang import System
from javax import management
from javax.management import MBeanException
from javax.management import RuntimeMBeanException
from java.lang import UnsupportedOperationException
from javax.management import InstanceAlreadyExistsException
from java.lang import Exception
from jarray import array

sys.path.append(os.path.abspath(os.path.dirname(sys.argv[0]))) #the directory that contains all files
import global_variables

# Global Variables
global_variables.ADMIN_URL = sys.argv[1]
global_variables.ADMIN_USERNAME = sys.argv[2]
global_variables.ADMIN_PASSWORD = sys.argv[3]

# Local Variables
envResourcesPath = sys.argv[4]
environmentValue = ""


#################################################################################################
#
#  initDeployerScriptRun
#
#  Initialize the environment for the script to run including connecting to the WebLogic server.
#
#
#################################################################################################

def initDeployerScriptRun():
    try:
        # Connect to the admin server
        connect(global_variables.ADMIN_USERNAME, global_variables.ADMIN_PASSWORD, global_variables.ADMIN_URL)
        print "CONNECTED" 
        # Obtain the following information and set to the global variables for later use in deploying the WLS resources
        # Servers MBean List, Servers Name List, Cluster MBean and Cluster Name
        targetServerMBeanList = []
        targetServerNameList = []
        clusterInDomain = cmo.getClusters()
    	  # If there is a cluster in the domain, Get the servers in the cluster otherwise get all the servers in the domain
        # This logic takes care of the targeting for a single server domain also
        serverList = []
        if len(clusterInDomain) == 1:
            serverList = clusterInDomain[0].getServers()
        else:
            serverList = cmo.getServers()
            
        # Go thru the list of servers obtained and create the target server MBean and Name lists	
        for server in serverList:
            print server.getName()
            # If there is a cluster in the domain, Set the targets to be of migratable type targets otherwise server type
            if len(clusterInDomain) == 1:
                serverString = jarray.array([ObjectName("com.bea:Name=" + server.getName() + " (migratable),Type=MigratableTarget")], ObjectName)
            else:
                serverString = jarray.array([ObjectName("com.bea:Name=" + server.getName() + ",Type=Server")], ObjectName)
            targetServerMBeanList.append(serverString)
            targetServerNameList.append(server.getName())
            global_variables.TARGET_SERVERS_MBEAN = targetServerMBeanList
            global_variables.TARGET_SERVERS_NAME = targetServerNameList
            # Get the cluster MBean and name
            if len(clusterInDomain) == 1:
                clusterName = clusterInDomain[0].getName()
                global_variables.TARGET_CLUSTER_MBEAN = jarray.array([ObjectName("com.bea:Name=" + clusterName + ",Type=Cluster")], ObjectName)
                global_variables.TARGET_CLUSTER_NAME = clusterName
            else:
                global_variables.TARGET_CLUSTER_MBEAN = serverString

    except WLSTException:
      print 'Error in the connection to the server at '
    
    if connected=='false':
      stopExecution('You need to be connected.')


#################################################################################################
#
#  endOfDeployerScriptRun
#
#  Inform the deployer that the script has finished.
#
#
#################################################################################################

def endOfDeployerScriptRun():
  print 'Disconnecting from WebLogic Server'



#################################################################################################
#
#  
#  Execute the deployment scripts for all modules.
#
#
#################################################################################################


try:

	print 'Starting script to create resources to remote environment ...'

	configurationDirectory = os.path.abspath(os.path.dirname(sys.argv[0]))

	print 'Starting Configuration Directory  ' + configurationDirectory

	print 'Calling initDeployerScriptRun'

	initDeployerScriptRun()

	print 'Loading Python files'
	execfile(configurationDirectory + "/config_domain_model.py")

	#commonResourcesPath = configurationDirectory + "/common.config.py"
	#print commonResourcesPath
	#commonResourcesFile = java.io.File(commonResourcesPath)
	#if commonResourcesFile.exists():
	#	execfile(commonResourcesPath)

	print 'Loading the creation resources ... create_resources.py' 
	envResourcesFile = java.io.File(envResourcesPath)
	if envResourcesFile.exists():
		execfile(envResourcesPath)
	else:
		print 'File create_resources.py does not exist. Skipping Configuration...'
		stopExecution('File to create resource is not available .')

	print 'Loading the common entity creation functions... config_domain_common_functions.py'
 	# import the common entity creation functions...
	execfile(configurationDirectory + "/config_domain_common_functions.py")

	print 'Loading configure all modules... config_domain_module_main.py'
	# configure all modules...
	execfile(configurationDirectory + "/config_domain_module_main.py")

finally:
  endOfDeployerScriptRun()