######################################################################################################
#
# Author: Roberto Porfiro (roberto.porfiro@timestamp.pt)
# Created: 2018/06/20
#
# Main Configuration Module
#
#################################################################################################

from weblogic.descriptor import BeanAlreadyExistsException
from java.lang.reflect import UndeclaredThrowableException
from java.lang import System
import javax
from javax import management
from javax.management import MBeanException
from javax.management import RuntimeMBeanException
import javax.management.MBeanException
from java.lang import UnsupportedOperationException
from javax.management import InstanceAlreadyExistsException
from java.lang import Exception
from jarray import array


#################################################################################################
#
#  startTransaction
#
#  Start the transaction for creating the Common infrastructure entities.
#
#
#################################################################################################

def startTransaction():
  edit()
  startEdit()


#################################################################################################
#
#  endTransaction
#
#  End the transaction for creating the Common infrastructure entities.
#
#
#################################################################################################

def endTransaction():
  startEdit()
  save()
  #activate(block="true")


#################################################################################################
#
#  endOfCommonResourcesScriptRun
#
#  Tell the user that the script is finished.
#
#
#################################################################################################

def endOfCommonResourcesScriptRun():
  print "Done executing the Common script."





#################################################################################################
#
#  Do the work
#
#################################################################################################

try:
  try:
    startTransaction()


    # For these WLS resources that are configured, The SPECS array is looped thru to configure all the entries in the array.
    # Also, depending on the resource, the targeting is done to the servers in the cluster or the cluster itself.
    # If it is done to the servers in the cluster, the resource is created with its name appended with the managed server name

	###############################################################################################
	# Create Work Manager  
    try:
		for index, jmsWorkManagerSpec in enumerate(WORK_MANAGER_SPECS):
			create_WorkManager(jmsWorkManagerSpec, global_variables.TARGET_CLUSTER_MBEAN)
    except NameError:
		print 'Variable WORK_MANAGER_SPECS does not exist. Skipping Configuration...'


    ###############################################################################################
    # Create File Stores  

    try:
    	for index, fileStoreSpec in enumerate(FILE_STORE_SPECS):
    		for index1, targetServerMBean in enumerate(global_variables.TARGET_SERVERS_MBEAN):
       			create_FileStore(fileStoreSpec, targetServerMBean, global_variables.TARGET_SERVERS_NAME[index1])
    except NameError:
    	print 'Variable FILE_STORE_SPECS does not exist. Skipping Configuration...'


    ###############################################################################################
    # Configure JDBC Resources...

    try:
    	for index, jdbcDataSourceSpec in enumerate(JDBC_DATA_SOURCE_SPECS):
 		create_JDBCDataSource(jdbcDataSourceSpec, global_variables.TARGET_CLUSTER_MBEAN)
    except NameError:
    	print 'Variable JDBC_DATA_SOURCE_SPECS does not exist. Skipping Configuration...'


    ###############################################################################################
    # Create JDBC Stores  

    try:
    	for index, jdbcStoreSpec in enumerate(JDBC_STORE_SPECS):
    		for index1, targetServerMBean in enumerate(global_variables.TARGET_SERVERS_MBEAN):
       			create_JDBCStore(jdbcStoreSpec, targetServerMBean, global_variables.TARGET_SERVERS_NAME[index1])
    except NameError:
    	print 'Variable JDBC_STORE_SPECS does not exist. Skipping Configuration...'


    ###############################################################################################
    # Create JMS Servers  

    try:
    	for index, jmsServerSpec in enumerate(JMS_SERVER_SPECS):
    		for index1, targetServerMBean in enumerate(global_variables.TARGET_SERVERS_MBEAN):
       			create_JMSServer(jmsServerSpec, targetServerMBean, global_variables.TARGET_SERVERS_NAME[index1])
    except NameError:
    	print 'Variable JMS_SERVER_SPECS does not exist. Skipping Configuration...'

    
    ###############################################################################################
    # Create JMS Modules   

    try:
    	for index, jmsSystemModuleSpec in enumerate(JMS_SYSTEM_MODULE_SPECS):
    		create_JMSSystemModule(jmsSystemModuleSpec, global_variables.TARGET_CLUSTER_MBEAN)
    except NameError:
    	print 'Variable JMS_SYSTEM_MODULE_SPECS does not exist. Skipping Configuration...'

  
    ###############################################################################################
    # Create JMS Template and Quotas 
    
    try:
    	for index, templateSpec in enumerate(TEMPLATE_SPECS):
    		create_Template(templateSpec)
    except NameError:
    	print 'Variable TEMPLATE_SPECS does not exist. Skipping Configuration...'
    
    try:
    	for index, quotaSpec in enumerate(QUOTA_SPECS):
    		create_Quota(quotaSpec)
    except NameError:
    	print 'Variable QUOTA_SPECS does not exist. Skipping Configuration...'

    
    ###############################################################################################
    # Create JMS Subdeployments 

    # targetServerNameArg could be an array of managed server names or a single managed server name
    # depending on the target for subdeployment that is indicated by the boolean targetToIndividualServer.
    # If the target to individual server is true, append the managed server name to the subdeployment
    # name and deploy the subdeployment to the JMS server corresponding to that managed server
    # If the target to individual server is false, keep the name of the subdeployment as it is and
    # Deploy the subdeployment to all the JMS servers in the cluster. This subdeployment could be
    # used for Uniform Distributed Queue or Uniform Distributed Topic etc
  
    try:
	for index, subdeploymentSpec in enumerate(SUBDEPLOYMENT_SPECS):
		if subdeploymentSpec.getTargetToIndividualServer():
			for index1, targetServerName in enumerate(global_variables.TARGET_SERVERS_NAME):
				create_Subdeployment(subdeploymentSpec,targetServerName)
		else:
			create_Subdeployment(subdeploymentSpec,global_variables.TARGET_SERVERS_NAME)

    except NameError:
	print 'Variable SUBDEPLOYMENT_SPECS does not exist. Skipping Configuration...'
  

    print 'Activating the first part of the changes...'
    # After creating the subdeployment and before the UDQ or UDT is created, the session needs to be activated.
    # Otherwise, "Same server added twice?" error occurs.
    endTransaction()
    # Obtain a new session again for furthur changes
    startTransaction()

    ###############################################################################################
    # Create JMS Connection Factories    

    try:
    	for index, connectionFactorySpec in enumerate(CONNECTION_FACTORY_SPECS):
    		create_ConnectionFactory(connectionFactorySpec)  
    except NameError:
    	print 'Variable CONNECTION_FACTORY_SPECS does not exist. Skipping Configuration...'


    ###############################################################################################
    # Create JMS Destinations 

    try:
	for index, queueSpec in enumerate(QUEUE_SPECS):
		for index1, targetServerName in enumerate(global_variables.TARGET_SERVERS_NAME):
    			create_Queue(queueSpec, targetServerName)
    except NameError:
    	print 'Variable QUEUE_SPECS does not exist. Skipping Configuration...'
    
    try:
    	for index, uniformDistributedQueueSpec in enumerate(UNIFORM_DISTRIBUTED_QUEUE_SPECS):
    		create_UniformDistributedQueue(uniformDistributedQueueSpec)
    except NameError:
    	print 'Variable UNIFORM_DISTRIBUTED_QUEUE_SPECS does not exist. Skipping Configuration...'

    try:
    	for index, weightedDistributedQueueSpec in enumerate(WEIGHTED_DISTRIBUTED_QUEUE_SPECS):
    		create_WeightedDistributedQueue(weightedDistributedQueueSpec)
    except NameError:
    	print 'Variable WEIGHTED_DISTRIBUTED_QUEUE_SPECS does not exist. Skipping Configuration...'

    try:
    	for index, topicSpec in enumerate(TOPIC_SPECS):
    		for index1, targetServerName in enumerate(global_variables.TARGET_SERVERS_NAME):
    			create_Topic(topicSpec, targetServerName)
    except NameError:
    	print 'Variable TOPIC_SPECS does not exist. Skipping Configuration...'
    
    try:    
    	for index, uniformDistributedTopicSpec in enumerate(UNIFORM_DISTRIBUTED_TOPIC_SPECS):
    		create_UniformDistributedTopic(uniformDistributedTopicSpec)
    except NameError:
    	print 'Variable UNIFORM_DISTRIBUTED_TOPIC_SPECS does not exist. Skipping Configuration...'

    try:
    	for index, weightedDistributedTopicSpec in enumerate(WEIGHTED_DISTRIBUTED_TOPIC_SPECS):
    		create_WeightedDistributedTopic(weightedDistributedTopicSpec)
    except NameError:
    	print 'Variable WEIGHTED_DISTRIBUTED_TOPIC_SPECS does not exist. Skipping Configuration...'


    ###############################################################################################
    # Configure Mail Sessions...

    try:
    	for index, mailSessionSpec in enumerate(MAIL_SESSION_SPECS):
        	create_MailSession(mailSessionSpec, global_variables.TARGET_CLUSTER_MBEAN)
    except NameError:
    	print 'Variable MAIL_SESSION_SPECS does not exist. Skipping Configuration...'


    ###############################################################################################
    # Startup Classes...

    try:
    	for index, startupClassSpec in enumerate(STARTUP_CLASS_SPECS):
        	create_StartupClass(startupClassSpec,global_variables.TARGET_CLUSTER_MBEAN)
    except NameError:
    	print 'Variable STARTUP_CLASS_SPECS does not exist. Skipping Configuration...'


    ###############################################################################################
    # Foreign Servers...

	  
    try:
    	for index, foreignServerSpec in enumerate(FOREIGN_SERVER_SPECS):
        	create_ForeignServer(foreignServerSpec)
    except NameError:
    	print 'Variable FOREIGN_SERVER_SPECS does not exist. Skipping Configuration...'


    ###############################################################################################
    # Foreign Connection Factories...

    try:
    	for index, foreignConnectionFactorySpec in enumerate(FOREIGN_CONNECTION_FACTORY_SPECS):
        	create_ForeignConnectionFactory(foreignConnectionFactorySpec)
    except NameError:
    	print 'Variable FOREIGN_CONNECTION_FACTORY_SPECS does not exist. Skipping Configuration...'


	###############################################################################################
		# Foreign Destinations...
	try:
		for index, foreignDestinationSpec in enumerate(FOREIGN_DESTINATION_SPECS):
	   	   create_ForeignDestination(foreignDestinationSpec)
	except NameError:
		print 'Variable FOREIGN_DESTINATION_SPECS does not exist. Skipping Configuration...'


	###############################################################################################
	# DbAdapter Connection Factories ...
	try:
		for index, DbAdapterSpec in enumerate(DB_ADAPTER_SPECS):
	   	   create_DbAdapter(DbAdapterSpec, global_variables.TARGET_CLUSTER_MBEAN)
	except NameError:
		print 'Variable DB_ADAPTER_SPECS does not exist. Skipping Configuration...'

    ###############################################################################################
    # Warn ahead of activation...
    #print ""
    #print "*** WARNING ***"
    #print "Preparing to activate changes.  Please make sure the following external resources are configured and available before proceeding:"
    #print " * All configured FileStore directories"
    #print " * All configured managed servers"
    #print "*** WARNING ***"
    #print ""
    
    #raw_input("Press the 'Enter' key to activate changes:")
    #print ""
    
    #print 'Activating the second part of the changes...'
    
    endTransaction()

    ##################################################################################################
    # For creating DbAdapter Connection Factories
    ##################################################################################################
    # Obtain a new session again for furthur changes
    #startTransaction()
    try:
        print 'Started transaction for creating DB Adapter'
    	for index, DbAdapterSpec_OLD in enumerate(DB_ADAPTER_SPECS):
 		create_DbAdapter_Old(DbAdapterSpec, global_variables.TARGET_CLUSTER_MBEAN)
    except NameError:
		print 'Variable DB_ADAPTER_SPECS does not exist. Skipping Configuration...'
    #endTransaction()

  except:
    print "Unexpected error: ", sys.exc_info()[0]
    dumpStack()
    edit()

    cancelEdit("y")

    disconnect()
    raise

finally:
  endOfCommonResourcesScriptRun()

