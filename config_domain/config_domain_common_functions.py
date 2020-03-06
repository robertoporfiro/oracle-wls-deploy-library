#################################################################################################
#
# Author: Roberto Porfiro (roberto.porfiro@timestamp.pt)
# Created: 2018/06/20
#
# Common Function Library
#
#################################################################################################

from weblogic.descriptor import BeanAlreadyExistsException
from java.lang.reflect import UndeclaredThrowableException
from java.lang import System
import javax
import time
from javax import management
from javax.management import MBeanException
from javax.management import RuntimeMBeanException
import javax.management.MBeanException
from java.lang import UnsupportedOperationException
from javax.management import InstanceAlreadyExistsException
from java.lang import Exception
from jarray import array
from java.util import Properties

#################################################################################################
#
# enumerate
#
# Provides for Jython 2.2 style iteration through lists
#
#
#################################################################################################
class enumerate:
	def __init__(self, seq):
		self.seq = seq
		
	def __getitem__(self, inx):
		return inx, self.seq[inx]
    

def findDestination(moduleBean, destinationName):
	destBean = moduleBean.lookupQueue(destinationName)
	if destBean != None:
		return destBean
	destBean = moduleBean.lookupTopic(destinationName)
	if destBean != None:
		return destBean
	destBean = moduleBean.lookupUniformDistributedQueue(destinationName)
	if destBean != None:
		return destBean
	destBean = moduleBean.lookupUniformDistributedTopic(destinationName)
	if destBean != None:
		return destBean
	destBean = moduleBean.lookupDistributedQueue(destinationName)
	if destBean != None:
		return destBean
	destBean = moduleBean.lookupDistributedTopic(destinationName)
	if destBean != None:
		return destBean
	

#################################################################################################
#
#  create_WorkManager
#
#  Create a work managertargeted to the cluster specified
#  
#
#################################################################################################
def create_WorkManager(spec,targetBean):
  cd("/")
  beanName    = spec.getName()
  domainName = cmo.getName()
  
  print "###################################"
  print "# CREATING WORK MANAGER"
  print "#"
  #print "	Target cluster Name: " + targetClusterName
  

  cd("/SelfTuning/" + domainName + "/WorkManagers")
  
  try:
  
    theBean = cmo.lookupWorkManager(beanName)
    if theBean == None:
      print "	Creating Bean '" + beanName + "' (WorkManager)..."
      #cmo.createWorkManager(beanName)
      wmgr = create(beanName,"WorkManager")
    else:
      print "	Updating MBean '" + beanName + "' (WorkManager)..."
      wmgr = theBean
          
  except java.lang.UnsupportedOperationException, usoe:
    pass
  except weblogic.descriptor.BeanAlreadyExistsException,bae:
    pass
  except java.lang.reflect.UndeclaredThrowableException,udt:
    pass
    
  print '	Setting targets for workmanager (' + beanName + ')'
    
  #set('Targets',targetBean)
  #print '	Getting target (/Clusters/' + targetClusterName + ')'
  #tgt = getMBean('/Clusters/' + targetClusterName)
  #print targetBean
  cd(beanName)
  set('Targets',targetBean)
  print '# CREATED WORKMANAGER ' + beanName
  print '###################################'

#################################################################################################
#
#	getFileStorePath
#
#	gets the path to the root domain directory for creating filestores.  Uses the Staging directory
#   to locate the server directory and then uses the standard paths from there
#
#################################################################################################
def getFileStorePath(targetServer):
	serverConfig()
	cd('Servers/'+targetServer)
	serverStagingPath = get('StagingDirectoryName')
	stagingDir = java.io.File(serverStagingPath)
	serverDir = stagingDir.getParent()
	remotePath = serverDir[2:len(serverDir)]
	host = get('ListenAddress')
	if len(host) < 1:
		raise java.lang.Exception("Unable to determine host for target server "+targetServer+" ensure the ListenAddress is set.")
	shareName = "d$"
	thePath = "\\\\"+host+"\\"+shareName+remotePath+"\\data\\jms\\"
	testFile = java.io.File(thePath)
	if testFile.exists():
		print "using "+thePath +"as JMS FileStore Root"
	else:
		if testFile.mkdirs():
			print "created the JMS root for "+ targetServer+" at path "+thePath
		else:
			print "JMS Root path "+thePath +" is not accessible.  Make sure the ddrive share exists and the build service account has access"
			raise java.lang.Exception("JMS Root path "+thePath +" is not accessible.  Make sure the ddrive share exists and the build servcie account has access")
	return thePath
	
	

  
#################################################################################################
#
#  create_FileStore
#
#  Create a file store in the specifed path.
#  
#
#################################################################################################
def create_FileStore(spec,targetServerMBean,targetServerName):

  beanName    = spec.getName() + "_" + targetServerName
  storageName = spec.getStorageName()
  # until all environments have listen address set, cannot reliably do this
  #rootDir = getFileStorePath(targetServerName)
  #fileStorePath = rootDir+storageName
  #fileStoreDir = java.io.File(fileStorePath)
  #if fileStoreDir.mkdirs():
  #  print "Created JMS Store directory "+fileStorePath
  #
  #if not fileStoreDir.exists():
  #  print "JMS Store directory "+fileStorePath+" does not exist and was not created.  Failing deployment."
  #  raise java.lang.Exception("JMS Store directory "+fileStorePath+" does not exist and was not created.  Failing deployment.")
  #reset the storage names based on our standards
  #storageName = "servers\\"+targetServerName+"\\data\\jms\\"+storageName
  edit()
  cd("/")
  try:
    theBean = cmo.lookupFileStore(beanName)
    if theBean == None:
      print "Creating MBean '" + beanName + "' (FileStore)..."
      cmo.createFileStore(beanName)
    else:
      print "Updating MBean '" + beanName + "' (FileStore)..."
  except java.lang.UnsupportedOperationException, usoe:
    pass
  except weblogic.descriptor.BeanAlreadyExistsException,bae:
   	pass
  except java.lang.reflect.UndeclaredThrowableException,udt:
   	pass

  cd("/FileStores/" + beanName)
  print "Setting attributes for MBean '" + beanName + "' (FileStore)..."
  
  print ""
  print "*** WARNING ***"
  print "Setting the filestore's directory as '" + storageName + "'.  Please make sure this directory exists before changes are activated."
  print "*** WARNING ***"
  print ""
  set("Directory", storageName)
    
  set('Targets',targetServerMBean)



#################################################################################################
#
#  create_JDBCDataSource
#
#  Create a jdbc datasource.
#  
#
#################################################################################################
def create_JDBCDataSource(spec, targetServerMBean):

  beanName = spec.getName()
  
  cd("/")
  
  try:
  
    theBean = cmo.lookupJDBCSystemResource(beanName)
    if theBean == None:
      print "Creating MBean '" + beanName + "' (JDBCDataSourcee)..."
      cmo.createJDBCSystemResource(beanName)
    else:
      print "Updating MBean '" + beanName + "' (JDBCDataSource)..."
    
      
  except java.lang.UnsupportedOperationException, usoe:
    pass
  except weblogic.descriptor.BeanAlreadyExistsException,bae:
    pass
  except java.lang.reflect.UndeclaredThrowableException,udt:
    pass 
    
  cd("/JDBCSystemResources/" + beanName + "/JDBCResource/" + beanName + "/JDBCDriverParams/" + beanName + "/Properties/" + beanName)
  
  try:
  
    theBean = cmo.lookupProperty("user")
    if theBean == None:
      print "Creating MBean 'user' (Property)..."
      cmo.createProperty("user")
    else:
      print "Updating MBean 'user' (Property)..."
      
  except java.lang.UnsupportedOperationException, usoe:
    pass
  except weblogic.descriptor.BeanAlreadyExistsException,bae:
    pass
  except java.lang.reflect.UndeclaredThrowableException,udt:
    pass
  except TypeError:
    prop = cmo.createProperty()
    prop.setName("user")   
    
  cd("/JDBCSystemResources/" + beanName)
  print "Setting attributes for MBean '" + beanName + "' (JDBCDataSource)..."
  set('Targets',targetServerMBean)

  
  cd("/JDBCSystemResources/" + beanName + "/JDBCResource/" + beanName + "/JDBCDriverParams/" + beanName + "/Properties/" + beanName + "/Properties/user")
  print "Setting attributes for MBean '" + beanName + "' (JDBCProperty)..."
  set("Value", spec.getUsername())
  set("Name", "user")      
      
  cd("/JDBCSystemResources/" + beanName + "/JDBCResource/" + beanName)
  print "Setting attributes for MBean '" + beanName + "' (JDBCDataSource)..."
  set("Name", beanName)  
  
  cd("/JDBCSystemResources/" + beanName + "/JDBCResource/" + beanName + "/JDBCDriverParams/" + beanName)
  print "Setting attributes for MBean '" + beanName + "' (JDBCDriverParams)..."
  set("Password", spec.getPassword())
  set("Url", spec.getURL())
  set("DriverName", spec.getDriverName())
    
  properties = cmo.getProperties()
  
  driverProperties = spec.getDriverProperties()
  
  for indexProperty, property in enumerate(driverProperties):
    propertyName = str(driverProperties[indexProperty][0])
    propertyValue = str(driverProperties[indexProperty][1])
    
    property = None
    propertyOName = properties.lookupProperty(propertyName)
    
    if propertyOName == None:    
      property = properties.createProperty(propertyName)
    else:
      propertyPath = getPath(propertyOName)
      cd("/" + str(propertyPath))
      property = cmo
          
    property.setValue(propertyValue)
  
  cd("/JDBCSystemResources/" + beanName + "/JDBCResource/" + beanName + "/JDBCDataSourceParams/" + beanName)
  print "Setting attributes for MBean '" + beanName + "' (JDBCDataSourceParams)..."
  set("GlobalTransactionsProtocol", spec.getGlobalTransactionsProtocol())
  set("JNDINames", jarray.array([spec.getJNDIName()], String))        

  cd("/JDBCSystemResources/" + beanName + "/JDBCResource/" + beanName + "/JDBCConnectionPoolParams/" + beanName)
  print "Setting attributes for MBean '" + beanName + "' (JDBCConnectionPoolParams)..."
  # Setting TestConnectionsOnReserve to true by default
  set("TestConnectionsOnReserve", "true")
  set("TestTableName", spec.getTestTableName())
  set("InitialCapacity", spec.getInitialCapacity())
  set("MaxCapacity", spec.getMaxCapacity())
  
  

#################################################################################################
#
#  create_JDBCStore
#
#  Create a JDBC store.
#  
#
#################################################################################################
def create_JDBCStore(spec,targetServerMBean,targetServerName):

  beanName    = spec.getName() + "_" + targetServerName
  prefixName  = spec.getPrefixName() + "_" + targetServerName
  
  cd("/")
  
  try:
  
    theBean = cmo.lookupJDBCStore(beanName)
    if theBean == None:
      print "Creating MBean '" + beanName + "' (JDBCStore)..."
      cmo.createJDBCStore(beanName)
    else:
      print "Updating MBean '" + beanName + "' (JDBCStore)..."
    
  except java.lang.UnsupportedOperationException, usoe:
    pass
  except weblogic.descriptor.BeanAlreadyExistsException,bae:
    pass
  except java.lang.reflect.UndeclaredThrowableException,udt:
    pass
    
  cd("/JDBCStores/" + beanName)
  print "Setting attributes for MBean '" + beanName + "' (JDBCStore)..."
  
  cmo.setDataSource(getMBean("/JDBCSystemResources/" + spec.getDataSource()))
  cmo.setPrefixName(prefixName)
  
  set('Targets',targetServerMBean)



#################################################################################################
#
#  create_JMSServer
#
#  Create a JMS server with the specified name in the specified path.
#
#
#################################################################################################
def create_JMSServer(spec,targetServerMBean,targetServerName):

  beanName           = spec.getName() + "_" + targetServerName
  persistentStore    = spec.getPersistentStore() + "_" + targetServerName
  messageBufferSize  = spec.getMessageBufferSize()
  bytesThresholdHigh = spec.getBytesThresholdHigh()
  bytesMaximum       = spec.getBytesMaximum()

  cd("/")
  
  try:
  
    theBean = cmo.lookupJMSServer(beanName)
    if theBean == None:
      print "Creating MBean '" + beanName + "' (JMSServer)..."
      cmo.createJMSServer(beanName)
    else:
      print "Updating MBean '" + beanName + "' (JMSServer)..."
      
  except java.lang.UnsupportedOperationException, usoe:
    pass
  except weblogic.descriptor.BeanAlreadyExistsException,bae:
    pass
  except java.lang.reflect.UndeclaredThrowableException,udt:
    pass
    
  cd("/JMSServers/" + beanName)
  print "Setting attributes for MBean '" + beanName + "' (JMSServer)..."  
  set('Targets',targetServerMBean)

  if persistentStore == None:
    cmo.setPersistentStore(None);
  else:
    storeBean = getMBean("/JDBCStores/" + persistentStore)
    if storeBean == None:
      storeBean = getMBean("/FileStores/" + persistentStore)
    cmo.setPersistentStore(storeBean)

  if messageBufferSize == None or messageBufferSize == "":
    # Default is 10% of the heap size of 2GB
    messageBufferSize = "214748364"

  cmo.setMessageBufferSize(long(messageBufferSize))

  if bytesThresholdHigh == None or bytesThresholdHigh == "":
    bytesThresholdHigh = "-1"

  cmo.setBytesThresholdHigh(long(bytesThresholdHigh))

  if bytesMaximum == None or bytesMaximum == "":
    # Default is 30% of the heap size of 2GB
    bytesMaximum = "715827882"

  cmo.setBytesMaximum(long(bytesMaximum))



#################################################################################################
#
#  create_JMSSystemModule
#
#  Create a JMS system module with the specified name in the specified path.
#
#
#################################################################################################
def create_JMSSystemModule(spec,targetServerMBean):

  systemModuleName = spec.getName()
  
  modulePath       = "/" + systemModuleName  
  cd("/")
  
  try:
  
    theBean = cmo.lookupJMSSystemResource(systemModuleName)
    if theBean == None:
      print "Creating MBean '" + systemModuleName + "' (JMSSystemModule)..."
      cmo.createJMSSystemResource(systemModuleName)
    else:
      print "Updating MBean '" + systemModuleName + "' (JMSSystemModule)..."
      
  except java.lang.UnsupportedOperationException, usoe:
    pass
  except weblogic.descriptor.BeanAlreadyExistsException,bae:
    pass
  except java.lang.reflect.UndeclaredThrowableException,udt:
    pass
    
  cd("/JMSSystemResources/" + systemModuleName)
  print "Setting attributes for MBean '" + systemModuleName + "' (JMSSystemModule)..."  
  set('Targets',targetServerMBean)

  

#################################################################################################
#
#  create_Template
#
#  Create a JMS template for the specified module.
#
#
#################################################################################################
def create_Template(spec):

  systemModuleName = spec.getModuleName()
  beanName         = spec.getName()
  timeToDeliver    = spec.getTimeToDeliver()
  
  path = "/JMSSystemResources/" + systemModuleName + "/JMSResource/" + systemModuleName + "/Templates"
  cd(path)
  
  try:
  
    theBean = cmo.lookupTemplate(beanName)
    if theBean == None:
      print "Creating MBean '" + beanName + "' (Template)..."
      cmo.createTemplate(beanName)
    else:
      print "Updating MBean '" + beanName + "' (Template)..."

      
  except java.lang.UnsupportedOperationException, usoe:
    pass
  except weblogic.descriptor.BeanAlreadyExistsException,bae:
    pass
  except java.lang.reflect.UndeclaredThrowableException,udt:
    pass
    
  print "Setting attributes for MBean '" + beanName + "' (Template)..."
  cd(path + "/" + beanName)
  set("Name", beanName)

  print "Setting delivery overrides for MBean '" + beanName + "' (Template)..."
  cd("DeliveryParamsOverrides/" +  beanName)
  set("TimeToDeliver", timeToDeliver)
  


#################################################################################################
#
#  create_Quota
#
#  Create a quota for the specified system module.
#
#################################################################################################
def create_Quota(spec):

  systemModuleName = spec.getModuleName()
  beanName         = spec.getName()
  
  modulePath = "/JMSSystemResources/" + systemModuleName + "/JMSResource/" + systemModuleName  
  cd(modulePath)
  
  try:
  
    theBean = cmo.lookupQuota(beanName)
    if theBean == None:
      print "Creating MBean '" + beanName + "' (Quota)..."
      cmo.createQuota(beanName)
    else:
      print "Updating MBean '" + beanName + "' (Quota)..."
          
  except java.lang.UnsupportedOperationException, usoe:
    pass
  except weblogic.descriptor.BeanAlreadyExistsException,bae:
    pass
  except java.lang.reflect.UndeclaredThrowableException,udt:
    pass
    
  cd(modulePath + "/Quotas/" + beanName)
  print "Setting attributes for MBean '" + beanName + "' (Quota)..."
  set("BytesMaximum", "9223372036854775807")
  set("Policy", "FIFO")
  set("Shared", "false")
  set("MessagesMaximum", "9223372036854775807")
  set("Name", beanName)



#################################################################################################
#
#  create_Subdeployment
#
#  Create a subdeployement for the specified system module.
#
#
#################################################################################################
def create_Subdeployment(spec,targetServerNameArg):

  systemModuleName = spec.getModuleName()

  # targetServerNameArg could be an array of managed server names or a single managed server name
  # depending on the target for subdeployment that is indicated by the boolean targetToIndividualServer.
  # If the target to individual server is true, append the managed server name to the subdeployment
  # name and deploy the subdeployment to the JMS server corresponding to that managed server
  # If the target to individual server is false, keep the name of the subdeployment as it is and
  # Deploy the subdeployment to all the JMS servers in the cluster. This subdeployment could be
  # used for Uniform Distributed Queue or Uniform Distributed Topic etc.

  if spec.getTargetToIndividualServer():
  	beanName = spec.getName() + "_" + targetServerNameArg
  	targetJmsServerMBeanList = jarray.array([ObjectName("com.bea:Name=" + spec.getJmsServerName() + "_" + targetServerNameArg + ",Type=JMSServer")], ObjectName)
  else:
  	beanName = spec.getName()
  	targetServerMBeanArray = []
  	for index, targetServerName in enumerate(targetServerNameArg):
		jmsServerMBean = ObjectName("com.bea:Name=" + spec.getJmsServerName() + "_" + targetServerName + ",Type=JMSServer")
		targetServerMBeanArray.append(jmsServerMBean)
  	targetJmsServerMBeanList = jarray.array(targetServerMBeanArray, ObjectName) 

  print targetJmsServerMBeanList
  
  modulePath = "/JMSSystemResources/" + systemModuleName
  cd(modulePath)
  
  try:
  
    theBean = cmo.lookupSubDeployment(beanName)
    if theBean == None:
      print "Creating MBean '" + beanName + "' (SubDeployment)..."
      cmo.createSubDeployment(beanName)
    else:
      print "Updating MBean '" + beanName + "' (SubDeployment)..."
    
  except java.lang.UnsupportedOperationException, usoe:
    pass
  except weblogic.descriptor.BeanAlreadyExistsException,bae:
    pass
  except java.lang.reflect.UndeclaredThrowableException,udt:
    pass
    
  cd(modulePath + "/SubDeployments/" + beanName)
  print "Setting attributes for MBean '" + beanName + "' (SubDeployment)..."  
  set('Targets',targetJmsServerMBeanList)



#################################################################################################
#
#  create_ConnectionFactory
#
#  Create a connection factory in the specifed system module.
#  
#
#################################################################################################
def create_ConnectionFactory(spec):
  systemModuleName  = spec.getModuleName()
  beanName          = spec.getName()
  jndiName          = spec.getJNDIName()
  xaEnabledFlag     = spec.getXAEnabled()
  if xaEnabledFlag:
  	xaEnabledFlagStr = "true"
  else:
  	xaEnabledFlagStr = "false"
  defaultTimeToLive = spec.getDefaultTimeToLive()
  modulePath = "/JMSSystemResources/" + systemModuleName + "/JMSResource/" + systemModuleName
  cd(modulePath)
  
  try:
    edit()
    theBean = cmo.lookupConnectionFactory(beanName)
    if theBean == None:
      print "Creating MBean '" + beanName + "' (ConnectionFactory)..."
      cmo.createConnectionFactory(beanName)
    else:
      print "Updating MBean '" + beanName + "' (ConnectionFactory)..."
      
  except java.lang.UnsupportedOperationException, usoe:
    pass
  except weblogic.descriptor.BeanAlreadyExistsException,bae:
    pass
  except java.lang.reflect.UndeclaredThrowableException,udt:
    pass
  cd(modulePath + "/ConnectionFactories/" + beanName)
  print "Setting attributes for MBean '" + beanName + "' (ConnectionFactory)..."
  set("JNDIName", jndiName)
  set("DefaultTargetingEnabled", "true")
  set("Name", beanName)
  cd(modulePath + "/ConnectionFactories/" + beanName + "/SecurityParams/" + beanName)
  set("AttachJMSXUserId", "false")
  cd(modulePath + "/ConnectionFactories/" + beanName + "/TransactionParams/" + beanName)
  set("XAConnectionFactoryEnabled", xaEnabledFlagStr)
  cd(modulePath + "/ConnectionFactories/" + beanName + "/LoadBalancingParams/" + beanName)
  set("ServerAffinityEnabled", "false")
  cd(modulePath + "/ConnectionFactories/" + beanName + "/DefaultDeliveryParams/" + beanName)
  
  if defaultTimeToLive == None or defaultTimeToLive == "":
    # Default for time to live is 24 hours
    defaultTimeToLive = "86400000"

  set("DefaultTimeToLive", defaultTimeToLive)



#################################################################################################
#
#  create_Queue
#
#  Create a queue with the given name for the specified module.
#
#
#################################################################################################
def create_Queue(spec, targetServerName):

  systemModuleName    = spec.getModuleName()
  beanName            = spec.getName() + "_" + targetServerName
  jndiName            = spec.getJNDIName()
  deadletterQueueName = spec.getDeadletterQueueName()
  if deadletterQueueName != "":
  	deadletterQueueName += "_" + targetServerName
  redeliveryLimit     = spec.getRedeliveryLimit()
  redeliveryDelay     = spec.getRedeliveryDelay()    
  subDeploymentName   = spec.getSubdeploymentName() + "_" + targetServerName
  bytesThresholdHigh  = spec.getBytesThresholdHigh()
  bytesThresholdLow   	= spec.getBytesThresholdLow()
  messagesThresholdHigh	= spec.getMessagesThresholdHigh()
  messagesThresholdLow	= spec.getMessagesThresholdLow()
  maximumMessageSize	= spec.getMaximumMessageSize()

  
  modulePath = "/JMSSystemResources/" + systemModuleName + "/JMSResource/" + systemModuleName  
  cd(modulePath)
  moduleBean = cmo
  try:
  
    theBean = cmo.lookupQueue(beanName)
    if theBean == None:
      print "Creating MBean '" + beanName + "' (Queue)..."
      cmo.createQueue(beanName)
    else:
      print "Updating MBean '" + beanName + "' (Queue)..."
      
      
  except java.lang.UnsupportedOperationException, usoe:
    pass
  except weblogic.descriptor.BeanAlreadyExistsException,bae:
    pass
  except java.lang.reflect.UndeclaredThrowableException,udt:
    pass
    
  cd(modulePath + "/Queues/" + beanName)
  print "Setting attributes for MBean '" + beanName + "' (Queue)..."
  set("SubDeploymentName", subDeploymentName)
  set("Name", beanName)
  set("JNDIName", jndiName)

  cd(modulePath + "/Queues/" + beanName + "/DeliveryFailureParams/" + beanName)
  print "Setting attributes for MBean '" + beanName + "' (DeliveryFailureParams)..."
  if redeliveryLimit != None  and  redeliveryLimit != "":
    set("RedeliveryLimit", redeliveryLimit)
  else:
    set("RedeliveryLimit", "-1")

  if deadletterQueueName != None  and  deadletterQueueName != "":
    set("ExpirationPolicy", "Redirect")
    deadletterBean = findDestination(moduleBean, deadletterQueueName)#getMBean(modulePath + "/Queues/" + deadletterQueueName)
    set("ErrorDestination", deadletterBean)
    
  cd(modulePath + "/Queues/" + beanName + "/DeliveryParamsOverrides/" + beanName) 
  print "Setting attributes for MBean '" + beanName + "' (DeliveryParamsOverrides)..."
  
  if redeliveryDelay != None  and  redeliveryDelay != "":
    set("RedeliveryDelay", redeliveryDelay)
  else:
    # Default for redelivery delay is 10 minutes
    set("RedeliveryDelay", "600000")

  cd(modulePath + "/Queues/" + beanName + "/Thresholds/" + beanName) 
  if bytesThresholdHigh != None  and bytesThresholdHigh != "":
  	set("BytesHigh", bytesThresholdHigh)
  else:
    	set("BytesHigh", "9223372036854775807")
  	
  if bytesThresholdLow != None  and bytesThresholdLow != "":
  	set("BytesLow", bytesThresholdLow)
  else:
    	set("BytesLow", "9223372036854775807")
  	
  if messagesThresholdHigh != None  and messagesThresholdHigh != "":
  	set("MessagesHigh", messagesThresholdHigh)
  else:
    	set("MessagesHigh", "9223372036854775807")

  if messagesThresholdLow != None  and messagesThresholdLow != "":
  	set("MessagesLow", messagesThresholdLow)
  else:
    	set("MessagesLow", "9223372036854775807")

  cd(modulePath + "/Queues/" + beanName) 
  if maximumMessageSize != None  and maximumMessageSize != "":
  	set("MaximumMessageSize", maximumMessageSize)
  else:
    	set("MaximumMessageSize", "2147483647")



#################################################################################################
#
#  create_UniformDistributedQueue
#
#  Create a queue with the given name for the specified module.
#
#
#################################################################################################
def create_UniformDistributedQueue(spec):

  systemModuleName    = spec.getModuleName()
  beanName            = spec.getName()
  jndiName            = spec.getJNDIName()
  deadletterQueueName = spec.getDeadletterQueueName()
  redeliveryLimit     = spec.getRedeliveryLimit()
  redeliveryDelay     = spec.getRedeliveryDelay()  
  subDeploymentName   = spec.getSubdeploymentName()
  bytesThresholdHigh  = spec.getBytesThresholdHigh()
  bytesThresholdLow   	= spec.getBytesThresholdLow()
  messagesThresholdHigh	= spec.getMessagesThresholdHigh()
  messagesThresholdLow	= spec.getMessagesThresholdLow()
  maximumMessageSize	= spec.getMaximumMessageSize()
  
  
  modulePath = "/JMSSystemResources/" + systemModuleName + "/JMSResource/" + systemModuleName  
  cd(modulePath)
  moduleBean = cmo
  try:
  
    theBean = cmo.lookupUniformDistributedQueue(beanName)    
    if theBean == None:
      print "Creating MBean '" + beanName + "' (UniformDistributedQueue)..."
      cmo.createUniformDistributedQueue(beanName)
    else:
      print "Updating MBean '" + beanName + "' (UniformDistributedQueue)..."
    
  except java.lang.UnsupportedOperationException, usoe:
    pass
  except weblogic.descriptor.BeanAlreadyExistsException,bae:
    pass
  except java.lang.reflect.UndeclaredThrowableException,udt:
    pass
    
  cd(modulePath + "/UniformDistributedQueues/" + beanName)
  print "Setting attributes for MBean '" + beanName + "' (UniformDistributedQueue)..."
  set("SubDeploymentName", subDeploymentName)
  set("Name", beanName)
  set("LoadBalancingPolicy", "Round-Robin")
  set("JNDIName", jndiName)
  
  cd(modulePath + "/UniformDistributedQueues/" + beanName + "/DeliveryFailureParams/" + beanName)
  print "Setting attributes for MBean '" + beanName + "' (DeliveryFailureParams)..."
  if redeliveryLimit != None  and  redeliveryLimit != "":
    set("RedeliveryLimit", redeliveryLimit)
  else:
    set("RedeliveryLimit", "-1")

  if deadletterQueueName != None  and  deadletterQueueName != "":
    set("ExpirationPolicy", "Redirect")
    deadletterBean = findDestination(moduleBean, deadletterQueueName)#getMBean(modulePath + "/UniformDistributedQueues/" + deadletterQueueName)
    set("ErrorDestination", deadletterBean)
    

  cd(modulePath + "/UniformDistributedQueues/" + beanName + "/DeliveryParamsOverrides/" + beanName) 
  print "Setting attributes for MBean '" + beanName + "' (DeliveryParamsOverrides)..."
  if redeliveryDelay != None  and  redeliveryDelay != "":
    set("RedeliveryDelay", redeliveryDelay)
  else:
    # Default for redelivery delay is 10 minutes
    set("RedeliveryDelay", "600000")
 
  cd(modulePath + "/UniformDistributedQueues/" + beanName + "/Thresholds/" + beanName) 
  if bytesThresholdHigh != None  and bytesThresholdHigh != "":
  	set("BytesHigh", bytesThresholdHigh)
  else:
    	set("BytesHigh", "9223372036854775807")
  	
  if bytesThresholdLow != None  and bytesThresholdLow != "":
  	set("BytesLow", bytesThresholdLow)
  else:
    	set("BytesLow", "9223372036854775807")
  	
  if messagesThresholdHigh != None  and messagesThresholdHigh != "":
  	set("MessagesHigh", messagesThresholdHigh)
  else:
    	set("MessagesHigh", "9223372036854775807")

  if messagesThresholdLow != None  and messagesThresholdLow != "":
  	set("MessagesLow", messagesThresholdLow)
  else:
    	set("MessagesLow", "9223372036854775807")

  cd(modulePath + "/UniformDistributedQueues/" + beanName) 
  if maximumMessageSize != None  and maximumMessageSize != "":
  	set("MaximumMessageSize", maximumMessageSize)
  else:
    	set("MaximumMessageSize", "2147483647")
    


#################################################################################################
#
#  create_WeightedDistributedQueue
#
#  Create a weighted distributed queue with the given name for the specified module.
#
#
#################################################################################################
def create_WeightedDistributedQueue(spec):

  systemModuleName    = spec.getModuleName()
  beanName            = spec.getName()
  jndiName            = spec.getJNDIName()
  queueMembers	    = spec.getQueueMembers()
  
  modulePath = "/JMSSystemResources/" + systemModuleName + "/JMSResource/" + systemModuleName  
  cd(modulePath)
  moduleBean = cmo
  try:
  
    theBean = cmo.lookupDistributedQueue(beanName)
    if theBean == None:
      print "Creating MBean '" + beanName + "' (WeightedDistributedQueue)..."
      cmo.createDistributedQueue(beanName)
    else:
      print "Updating MBean '" + beanName + "' (WeightedDistributedQueue)..."
    
  except java.lang.UnsupportedOperationException, usoe:
    pass
  except weblogic.descriptor.BeanAlreadyExistsException,bae:
    pass
  except java.lang.reflect.UndeclaredThrowableException,udt:
    pass
    
  cd(modulePath + "/DistributedQueues/" + beanName)
  print "Setting attributes for MBean '" + beanName + "' (WeightedDistributedQueue)..."
  set("Name", beanName)
  set("LoadBalancingPolicy", "Round-Robin")
  set("JNDIName", jndiName)

  distributedQueueMembers = cmo.getDistributedQueueMembers()
  for distributedQueueMember in distributedQueueMembers:
  	cmo.destroyDistributedQueueMember(distributedQueueMember)
  
  queueMemberArray = queueMembers.split(',')
  for currentQueueMember in queueMemberArray:
  	for targetServerName in global_variables.TARGET_SERVERS_NAME:
  		queueMember = currentQueueMember + "_" + targetServerName
  		theBean = cmo.lookupDistributedQueueMember(queueMember)
  		if theBean == None:
      			print "Creating '" + queueMember + "' (WeightedDistributedQueueMember)..."
      			cmo.createDistributedQueueMember(queueMember)
    		else:
      			print queueMember + " (WeightedDistributedQueueMember) already created..."
	


#################################################################################################
#
#  create_Topic
#
#  Create a topic with the given name for the specified module.
#
#
#################################################################################################
def create_Topic(spec, targetServerName):

  systemModuleName    = spec.getModuleName()
  beanName            = spec.getName() + "_" + targetServerName
  jndiName            = spec.getJNDIName()
  deadletterTopicName = spec.getDeadletterTopicName()
  if deadletterTopicName != "":
  	deadletterTopicName += "_" + targetServerName
  redeliveryLimit     = spec.getRedeliveryLimit()
  redeliveryDelay     = spec.getRedeliveryDelay()    
  subDeploymentName   = spec.getSubdeploymentName() + "_" + targetServerName
  bytesThresholdHigh  = spec.getBytesThresholdHigh()
  bytesThresholdLow   	= spec.getBytesThresholdLow()
  messagesThresholdHigh	= spec.getMessagesThresholdHigh()
  messagesThresholdLow	= spec.getMessagesThresholdLow()
  maximumMessageSize	= spec.getMaximumMessageSize()
  
  modulePath = "/JMSSystemResources/" + systemModuleName + "/JMSResource/" + systemModuleName  
  cd(modulePath)
  moduleBean = cmo
  try:
  
    theBean = cmo.lookupTopic(beanName)
    if theBean == None:
      print "Creating MBean '" + beanName + "' (Topic)..."
      cmo.createTopic(beanName)
    else:
      print "Updating MBean '" + beanName + "' (Topic)..."
      
      
  except java.lang.UnsupportedOperationException, usoe:
    pass
  except weblogic.descriptor.BeanAlreadyExistsException,bae:
    pass
  except java.lang.reflect.UndeclaredThrowableException,udt:
    pass
    
  cd(modulePath + "/Topics/" + beanName)
  print "Setting attributes for MBean '" + beanName + "' (Topic)..."
  set("SubDeploymentName", subDeploymentName)
  set("Name", beanName)
  #set("JNDIName", jndiName)
  set("LocalJNDIName", jndiName)

  cd(modulePath + "/Topics/" + beanName + "/DeliveryFailureParams/" + beanName)
  print "Setting attributes for MBean '" + beanName + "' (DeliveryFailureParams)..."
  if redeliveryLimit != None  and  redeliveryLimit != "":
    set("RedeliveryLimit", redeliveryLimit)
  else:
    set("RedeliveryLimit", "-1")

  if deadletterTopicName != None  and  deadletterTopicName != "":
    set("ExpirationPolicy", "Redirect")
    deadletterBean = findDestination(moduleBean, deadletterTopicName)#getMBean(modulePath + "/Topics/" + deadletterTopicName)
    set("ErrorDestination", deadletterBean)
    
  cd(modulePath + "/Topics/" + beanName + "/DeliveryParamsOverrides/" + beanName) 
  print "Setting attributes for MBean '" + beanName + "' (DeliveryParamsOverrides)..."
  
  if redeliveryDelay != None  and  redeliveryDelay != "":
    set("RedeliveryDelay", redeliveryDelay)
  else:
    # Default for redelivery delay is 10 minutes
    set("RedeliveryDelay", "600000")


  cd(modulePath + "/Topics/" + beanName + "/Thresholds/" + beanName) 
  if bytesThresholdHigh != None  and bytesThresholdHigh != "":
  	set("BytesHigh", bytesThresholdHigh)
  else:
    	set("BytesHigh", "9223372036854775807")
  	
  if bytesThresholdLow != None  and bytesThresholdLow != "":
  	set("BytesLow", bytesThresholdLow)
  else:
    	set("BytesLow", "9223372036854775807")
  	
  if messagesThresholdHigh != None  and messagesThresholdHigh != "":
  	set("MessagesHigh", messagesThresholdHigh)
  else:
    	set("MessagesHigh", "9223372036854775807")

  if messagesThresholdLow != None  and messagesThresholdLow != "":
  	set("MessagesLow", messagesThresholdLow)
  else:
    	set("MessagesLow", "9223372036854775807")

  cd(modulePath + "/Topics/" + beanName) 
  if maximumMessageSize != None  and maximumMessageSize != "":
  	set("MaximumMessageSize", maximumMessageSize)
  else:
    	set("MaximumMessageSize", "2147483647")



#################################################################################################
#
#  create_UniformDistributedTopic
#
#  Create an uniform distributed topic with the given name for the specified module.
#
#
#################################################################################################
def create_UniformDistributedTopic(spec):

  systemModuleName    = spec.getModuleName()
  beanName            = spec.getName()
  jndiName            = spec.getJNDIName()
  deadletterTopicName = spec.getDeadletterTopicName()
  redeliveryLimit     = spec.getRedeliveryLimit()
  redeliveryDelay     = spec.getRedeliveryDelay()  
  subDeploymentName   = spec.getSubdeploymentName()
  bytesThresholdHigh  = spec.getBytesThresholdHigh()
  bytesThresholdLow   	= spec.getBytesThresholdLow()
  messagesThresholdHigh	= spec.getMessagesThresholdHigh()
  messagesThresholdLow	= spec.getMessagesThresholdLow()
  maximumMessageSize	= spec.getMaximumMessageSize()
  
  modulePath = "/JMSSystemResources/" + systemModuleName + "/JMSResource/" + systemModuleName  
  cd(modulePath)
  moduleBean = cmo
  try:
  
    theBean = cmo.lookupUniformDistributedTopic(beanName)    
    if theBean == None:
      print "Creating MBean '" + beanName + "' (UniformDistributedTopic)..."
      cmo.createUniformDistributedTopic(beanName)
    else:
      print "Updating MBean '" + beanName + "' (UniformDistributedTopic)..."
    
  except java.lang.UnsupportedOperationException, usoe:
    pass
  except weblogic.descriptor.BeanAlreadyExistsException,bae:
    pass
  except java.lang.reflect.UndeclaredThrowableException,udt:
    pass
    
  cd(modulePath + "/UniformDistributedTopics/" + beanName)
  print "Setting attributes for MBean '" + beanName + "' (UniformDistributedTopic)..."
  set("SubDeploymentName", subDeploymentName)
  set("Name", beanName)
  set("LoadBalancingPolicy", "Round-Robin")
  set("JNDIName", jndiName)
  
  cd(modulePath + "/UniformDistributedTopics/" + beanName + "/DeliveryFailureParams/" + beanName)
  print "Setting attributes for MBean '" + beanName + "' (DeliveryFailureParams)..."
  if redeliveryLimit != None  and  redeliveryLimit != "":
    set("RedeliveryLimit", redeliveryLimit)
  else:
    set("RedeliveryLimit", "-1")

  if deadletterTopicName != None  and  deadletterTopicName != "":
    set("ExpirationPolicy", "Redirect")
    deadletterBean = findDestination(moduleBean, deadletterTopicName)#getMBean(modulePath + "/UniformDistributedTopics/" + deadletterTopicName)
    set("ErrorDestination", deadletterBean)
    

  cd(modulePath + "/UniformDistributedTopics/" + beanName + "/DeliveryParamsOverrides/" + beanName) 
  print "Setting attributes for MBean '" + beanName + "' (DeliveryParamsOverrides)..."

  if redeliveryDelay != None  and  redeliveryDelay != "":
    set("RedeliveryDelay", redeliveryDelay)
  else:
    # Default for redelivery delay is 10 minutes
    set("RedeliveryDelay", "600000")


  cd(modulePath + "/UniformDistributedTopics/" + beanName + "/Thresholds/" + beanName) 
  if bytesThresholdHigh != None  and bytesThresholdHigh != "":
  	set("BytesHigh", bytesThresholdHigh)
  else:
    	set("BytesHigh", "9223372036854775807")
  	
  if bytesThresholdLow != None  and bytesThresholdLow != "":
  	set("BytesLow", bytesThresholdLow)
  else:
    	set("BytesLow", "9223372036854775807")
  	
  if messagesThresholdHigh != None  and messagesThresholdHigh != "":
  	set("MessagesHigh", messagesThresholdHigh)
  else:
    	set("MessagesHigh", "9223372036854775807")

  if messagesThresholdLow != None  and messagesThresholdLow != "":
  	set("MessagesLow", messagesThresholdLow)
  else:
    	set("MessagesLow", "9223372036854775807")

  cd(modulePath + "/UniformDistributedTopics/" + beanName) 
  if maximumMessageSize != None  and maximumMessageSize != "":
  	set("MaximumMessageSize", maximumMessageSize)
  else:
    	set("MaximumMessageSize", "2147483647")



#################################################################################################
#
#  create_WeightedDistributedTopic
#
#  Create a weighted distributed topic with the given name for the specified module.
#
#
#################################################################################################
def create_WeightedDistributedTopic(spec):

  systemModuleName    = spec.getModuleName()
  beanName            = spec.getName()
  jndiName            = spec.getJNDIName()
  topicMembers	    = spec.getTopicMembers()
  
  modulePath = "/JMSSystemResources/" + systemModuleName + "/JMSResource/" + systemModuleName  
  cd(modulePath)
  
  try:
  
    theBean = cmo.lookupDistributedTopic(beanName)
    if theBean == None:
      print "Creating MBean '" + beanName + "' (WeightedDistributedTopic)..."
      cmo.createDistributedTopic(beanName)
    else:
      print "Updating MBean '" + beanName + "' (WeightedDistributedTopic)..."
    
  except java.lang.UnsupportedOperationException, usoe:
    pass
  except weblogic.descriptor.BeanAlreadyExistsException,bae:
    pass
  except java.lang.reflect.UndeclaredThrowableException,udt:
    pass
    
  cd(modulePath + "/DistributedTopics/" + beanName)
  print "Setting attributes for MBean '" + beanName + "' (WeightedDistributedTopic)..."
  set("Name", beanName)
  set("LoadBalancingPolicy", "Round-Robin")
  set("JNDIName", jndiName)

  # First, Delete all the topics that are part of this distributed topic and then add the topics provided by the user
  distributedTopicMembers = cmo.getDistributedTopicMembers()
  for distributedTopicMember in distributedTopicMembers:
  	cmo.destroyDistributedTopicMember(distributedTopicMember)
  
  topicMemberArray = topicMembers.split(',')
  for currentTopicMember in topicMemberArray:
  	for targetServerName in global_variables.TARGET_SERVERS_NAME:
  		topicMember = currentTopicMember + "_" + targetServerName
  		theBean = cmo.lookupDistributedTopicMember(topicMember)
  		if theBean == None:
      			print "Creating '" + topicMember + "' (WeightedDistributedTopicMember)..."
      			cmo.createDistributedTopicMember(topicMember)
    		else:
      			print topicMember + " (WeightedDistributedTopicMember) already created..."
	


#################################################################################################
#
#  create_MailSession
#
#  Create a Java Mail Session
#  
#
#################################################################################################
def create_MailSession(spec,targetServerMBean):

  beanName          = spec.getName()
  jndiName          = spec.getJNDIName()
  sessionProperties = spec.getSessionProperties()

  cd("/")
  
  try:
  
    theBean = cmo.lookupMailSession(beanName)
    if theBean == None:
      print "Creating MBean '" + beanName + "' (MailSession)..."
      cmo.createMailSession(beanName)
    else:
      print "Updating MBean '" + beanName + "' (MailSession)..."
    
  except java.lang.UnsupportedOperationException, usoe:
    pass
  except weblogic.descriptor.BeanAlreadyExistsException,bae:
    pass
  except java.lang.reflect.UndeclaredThrowableException,udt:
    pass 
    
  cd("/MailSessions/" + beanName)
  print "Setting attributes for MBean '" + beanName + "' (MailSession)..."
  set("JNDIName", jndiName)
  set("Properties", makePropertiesObject(sessionProperties))
  set('Targets',targetServerMBean)
  
  
  
#################################################################################################
#
#  create_StartupClass
#
#  Create a Startup Class
#  
#
#################################################################################################
def create_StartupClass(spec,targetServerMBean):

  beanName          = spec.getName()

  cd("/")
  
  try:
  
    theBean = cmo.lookupStartupClass(beanName)
    if theBean == None:
      print "Creating MBean '" + beanName + "' (StartupClass)..."
      cmo.createStartupClass(beanName)
    else:
      print "Updating MBean '" + beanName + "' (StartupClass)..."
    
  except java.lang.UnsupportedOperationException, usoe:
    pass
  except weblogic.descriptor.BeanAlreadyExistsException,bae:
    pass
  except java.lang.reflect.UndeclaredThrowableException,udt:
    pass 
    
  cd("/StartupClasses/" + beanName)
  print "Setting attributes for MBean '" + beanName + "' (StartupClass)..."
  cmo.setClassName(spec.getClassName())
  cmo.setArguments(spec.getArguments())
  cmo.setFailureIsFatal(spec.getFailureIsFatal())
  cmo.setLoadBeforeAppDeployments(spec.getLoadBeforeAppDeployments())
  set('Targets',targetServerMBean)


#################################################################################################
#
#  create_ForeignServer
#
#################################################################################################

def create_ForeignServer(spec):

  cd("/")
  domainName = cmo.getName()

  cd("/JMSSystemResources/" + spec.getModuleName() + "/JMSResource/" + spec.getModuleName())
  
  try:
    print "STARTING"
    theBean = cmo.lookupForeignServer(spec.getName())
    if theBean == None:
      print "Creating MBean '" + spec.getName() + "' (ForeignServer)..."
      cmo.createForeignServer(spec.getName())
    else:
      print "Updating MBean '" + spec.getName() + "' (WorkManager)..."
      
  except java.lang.UnsupportedOperationException, usoe:
    pass
  except weblogic.descriptor.BeanAlreadyExistsException,bae:
    pass
  except java.lang.reflect.UndeclaredThrowableException,udt:
    pass 
    
  cd("/JMSSystemResources/" + spec.getModuleName() + "/JMSResource/" + spec.getModuleName() + "/ForeignServers/" + spec.getName())
  cmo.setSubDeploymentName(spec.getSubdeploymentName())
  cmo.setInitialContextFactory(spec.getJndiInitialContextFactory())
  cmo.setConnectionURL(spec.getJNDIURL())
  cmo.unSet('JNDIPropertiesCredentialEncrypted')



#################################################################################################
#
#  create_ForeignConnectionFactory
#
#################################################################################################

def create_ForeignConnectionFactory(spec):

  cd("/")
  domainName = cmo.getName()

  cd("/JMSSystemResources/" + spec.getModuleName() + "/JMSResource/" + spec.getModuleName() + "/ForeignServers/" + spec.getForeignServerName())
  
  try:
    print "STARTING"
    theBean = cmo.lookupForeignConnectionFactory(spec.getName())
    if theBean == None:
      print "Creating MBean '" + spec.getName() + "' (ForeignConnectionFactory)..."
      cmo.createForeignConnectionFactory(spec.getName())
    else:
      print "Updating MBean '" + spec.getName() + "' (ForeignConnectionFactory)..."
      
  except java.lang.UnsupportedOperationException, usoe:
    pass
  except weblogic.descriptor.BeanAlreadyExistsException,bae:
    pass
  except java.lang.reflect.UndeclaredThrowableException,udt:
    pass 
    
  cd("/JMSSystemResources/" + spec.getModuleName() + "/JMSResource/" + spec.getModuleName() + "/ForeignServers/" + spec.getForeignServerName() + "/ForeignConnectionFactories/" + spec.getName())
  cmo.setLocalJNDIName(spec.getLocalJndi())
  cmo.setRemoteJNDIName(spec.getRemoteJndi())
  cmo.setPassword(spec.getPassword())
  cmo.setUsername(spec.getUsername())



#################################################################################################
#
#  create_ForeignDestination
#
#################################################################################################

def create_ForeignDestination(spec, targetServerMBean):

  cd("/")
  domainName = cmo.getName()

  cd("/JMSSystemResources/" + spec.getModuleName() + "/JMSResource/" + spec.getModuleName() + "/ForeignServers/" + spec.getForeignServerName())
  
  try:
    print "STARTING"
    theBean = cmo.lookupForeignDestination(spec.getName())
    if theBean == None:
      print "Creating MBean '" + spec.getName() + "' (ForeignDestination)..."
      cmo.createForeignDestination(spec.getName())
    else:
      print "Updating MBean '" + spec.getName() + "' (ForeignDestination)..."
      
  except java.lang.UnsupportedOperationException, usoe:
    pass
  except weblogic.descriptor.BeanAlreadyExistsException,bae:
    pass
  except java.lang.reflect.UndeclaredThrowableException,udt:
    pass 
    
  cd("/JMSSystemResources/" + spec.getModuleName() + "/JMSResource/" + spec.getModuleName() + "/ForeignServers/" + spec.getForeignServerName() + "/ForeignDestinations/" + spec.getName())
  cmo.setLocalJNDIName(spec.getLocalJndi())
  #cmo.setRemoteJNDIName(spec.getRemoteJndi())
  cmo.createJNDIProperty(spec.getRemoteJndi())

#################################################################################################
#
#  create_DbAdapter
#
#################################################################################################

def create_DbAdapter(spec, targetServerMBean):

  appName = 'DbAdapter'
  moduleOverrideName = appName+'.rar'
  uniqueString = str(int(time.time()))

  cd("/")
  domainName = cmo.getName()
  #
  # update the deployment plan
  #
  try:
    print('–> about to update the deployment plan for the DbAdapter')
    #startEdit()
    planPath = get('/AppDeployments/DbAdapter/PlanPath')
    appPath = get('/AppDeployments/DbAdapter/SourcePath')
    print('–> Using plan ' + planPath)
    plan = loadApplication(appPath, planPath)
    print('–> adding variables to plan')
    makeDeploymentPlanVariable(plan, 'ConnectionInstance_eis/DB/' + spec.getDataSourceJNDIName() + '_JNDIName_' + uniqueString, spec.getInstanceJNDI(), '/weblogic-connector/outbound-resource-adapter/connection-definition-group/[connection-factory-interface="javax.resource.cci.ConnectionFactory"]/connection-instance/[jndi-name="' + spec.getInstanceJNDI() + '"]/jndi-name')
    makeDeploymentPlanVariable(plan, 'ConfigProperty_xADataSourceName_Value_' + uniqueString, spec.getInstanceJNDI(), '/weblogic-connector/outbound-resource-adapter/connection-definition-group/[connection-factory-interface="javax.resource.cci.ConnectionFactory"]/connection-instance/[jndi-name="'+spec.getInstanceJNDI()+'"]/connection-properties/properties/property/[name="XADataSourceName"]/value')
    print('–> saving plan')
    plan.save();
    save();
    print('–> activating changes')
    #activate(block='true');
    cd('/AppDeployments/DbAdapter/Targets');
    print('–> redeploying the DbAdapter')
    #stopApplication(appName)
    updateApplication(appName, planPath);
    startApplication(appName)
    #redeploy(appName, planPath, targets=targetServerMBean);
    print('–> done')

  except:
    print('–> something went wrong, bailing out')
    #stopEdit('y')
  raise SystemExit

#
# method definitions
#

def makeDeploymentPlanVariable(wlstPlan, name, value, xpath, origin='planbased'):

	appName = 'DbAdapter'
	moduleOverrideName = appName+'.rar'
	moduleDescriptorName = 'META-INF/weblogic-ra.xml'

	try:
		wlstPlan.destroyVariable(name)
		wlstPlan.destroyVariableAssignment(name, moduleOverrideName, moduleDescriptorName)
		variableAssignment = wlstPlan.createVariableAssignment(name, moduleOverrideName, moduleDescriptorName)
		variableAssignment.setXpath(xpath)
		variableAssignment.setOrigin(origin)
		wlstPlan.createVariable(name, value)

	except:
		print('–> was not able to create deployment plan variables successfully')