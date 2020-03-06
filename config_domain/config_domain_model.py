#################################################################################################
#
# Author: Roberto Porfiro (roberto.porfiro@timestamp.pt)
# Created: 2018/06/20
#
# Configuration Model Classes
#
#################################################################################################
class WorkManagerSpec:
    def __init__(self, name, maxThreadsConstraintName,  maxThreadsConstraint, minThreadsConstraintName, minThreadsConstraint):
        self.name                       = name;
	self.maxThreadsConstraintName   = maxThreadsConstraintName
	self.maxThreadsConstraint       = maxThreadsConstraint
	self.minThreadsConstraintName   = minThreadsConstraintName
	self.minThreadsConstraint       = minThreadsConstraint
	return
    
    def getName(self):
        return self.name
	
    def getMaxThreadsConstraintName(self):
        return self.maxThreadsConstraintName
	
    def getMaxThreadsConstraint(self):
        return self.maxThreadsConstraint
	
    def getMinThreadsConstraintName(self):
        return self.minThreadsConstraintName	
	
    def getMinThreadsConstraint(self):
        return self.minThreadsConstraint

class FileStoreSpec:
    def __init__(self, name, storageName):
        self.name        = name;
        self.storageName = storageName;
        return
    
    def getName(self):
        return self.name
                
    def getStorageName(self):
        return self.storageName



class JDBCDataSourceSpec:
    def __init__(self, name, jndiName, username, password, url, driverName, driverProperties, initialCapacity, maxCapacity, testTableName, globalTransactionsProtocol):
        self.name                       = name;
        self.jndiName                   = jndiName        
        self.username                   = username        
        self.password                   = password        
        self.url                        = url        
        self.driverName                 = driverName        
        self.driverProperties           = driverProperties
        self.initialCapacity            = initialCapacity
        self.maxCapacity                = maxCapacity
        self.testTableName              = testTableName
        self.globalTransactionsProtocol = globalTransactionsProtocol
        return
    
    def getName(self):
        return self.name
                
    def getJNDIName(self):
        return self.jndiName

    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.password

    def getURL(self):
        return self.url

    def getDriverName(self):
        return self.driverName

    def getDriverProperties(self):
        return self.driverProperties

    def getInitialCapacity(self):
        return self.initialCapacity

    def getMaxCapacity(self):
        return self.maxCapacity

    def getTestTableName(self):
        return self.testTableName

    def getGlobalTransactionsProtocol(self):
        return self.globalTransactionsProtocol



class JDBCStoreSpec:
    def __init__(self, name, dataSource, prefixName):
        self.name        = name;
        self.dataSource  = dataSource;
        self.prefixName  = prefixName;
        return
    
    def getName(self):
        return self.name
                
    def getDataSource(self):
        return self.dataSource
                
    def getPrefixName(self):
        return self.prefixName



class JMSServerSpec:
    def __init__(self, name, persistentStore, messageBufferSize, bytesThresholdHigh, bytesMaximum):
        self.name               = name;
        self.persistentStore    = persistentStore
        self.messageBufferSize  = messageBufferSize
        self.bytesThresholdHigh = bytesThresholdHigh
        self.bytesMaximum       = bytesMaximum
        return
    
    def getName(self):
        return self.name
                
    def getPersistentStore(self):
        return self.persistentStore

    def getMessageBufferSize(self):
        return self.messageBufferSize

    def getBytesThresholdHigh(self):
        return self.bytesThresholdHigh

    def getBytesMaximum(self):
        return self.bytesMaximum
                
                

class JMSSystemModuleSpec:
    def __init__(self, name):
        self.name    = name;
        return
    
    def getName(self):
        return self.name
                


class ConnectionFactorySpec:
    def __init__(self, name, moduleName, jndiName, xaEnabled, defaultTimeToLive):
        self.name               = name;
        self.moduleName         = moduleName;
        self.jndiName           = jndiName;
        self.xaEnabled          = xaEnabled;
        self.defaultTimeToLive  = defaultTimeToLive;
        return
    
    def getName(self):
        return self.name
                
    def getModuleName(self):
        return self.moduleName
        
    def getJNDIName(self):
        return self.jndiName

    def getXAEnabled(self):
        return self.xaEnabled

    def getDefaultTimeToLive(self):
        return self.defaultTimeToLive



class TemplateSpec:
    def __init__(self, name, moduleName, timeToDeliver):
        self.name          = name;
        self.moduleName    = moduleName;
        self.timeToDeliver = timeToDeliver;
        return
    
    def getName(self):
        return self.name
                
    def getModuleName(self):
        return self.moduleName

    def getTimeToDeliver(self):
        return self.timeToDeliver



class QuotaSpec:
    def __init__(self, name, moduleName):
        self.name       = name;
        self.moduleName = moduleName;
        return
    
    def getName(self):
        return self.name
        
    def getModuleName(self):
        return self.moduleName



class SubdeploymentSpec:
    def __init__(self, name, moduleName,jmsServerName,targetToIndividualServer):
        self.name       = name;
        self.moduleName = moduleName;
        self.jmsServerName = jmsServerName;
        self.targetToIndividualServer = targetToIndividualServer;        
        return
    
    def getName(self):
        return self.name

    def getModuleName(self):
        return self.moduleName

    def getJmsServerName(self):
        return self.jmsServerName

    def getTargetToIndividualServer(self):
        return self.targetToIndividualServer

                

class QueueSpec:
    def __init__(self, name, moduleName, subdeploymentName, jndiName, deadletterQueueName, redeliveryLimit, redeliveryDelay, bytesThresholdHigh, bytesThresholdLow, messagesThresholdHigh, messagesThresholdLow, maximumMessageSize):
        self.name                	= name;
        self.moduleName          	= moduleName;
        self.subdeploymentName   	= subdeploymentName;
        self.jndiName            	= jndiName;
        self.deadletterQueueName 	= deadletterQueueName;
        self.redeliveryLimit     	= redeliveryLimit;
        self.redeliveryDelay     	= redeliveryDelay;
        self.bytesThresholdHigh	 	= bytesThresholdHigh
        self.bytesThresholdLow   	= bytesThresholdLow
        self.messagesThresholdHigh	= messagesThresholdHigh
        self.messagesThresholdLow	= messagesThresholdLow
        self.maximumMessageSize		= maximumMessageSize
        return
    
    def getName(self):
        return self.name
                
    def getModuleName(self):
        return self.moduleName
        
    def getSubdeploymentName(self):
        return self.subdeploymentName
        
    def getJNDIName(self):
        return self.jndiName
        
    def getDeadletterQueueName(self):
        return self.deadletterQueueName
                
    def getRedeliveryLimit(self):
        return self.redeliveryLimit
                
    def getRedeliveryDelay(self):
        return self.redeliveryDelay
                            
    def getBytesThresholdHigh(self):
        return self.bytesThresholdHigh

    def getBytesThresholdLow(self):
        return self.bytesThresholdLow

    def getMessagesThresholdHigh(self):
        return self.messagesThresholdHigh

    def getMessagesThresholdLow(self):
        return self.messagesThresholdLow

    def getMaximumMessageSize(self):
        return self.maximumMessageSize	



class UniformDistributedQueueSpec:
    def __init__(self, name, moduleName, subdeploymentName, jndiName, deadletterQueueName, redeliveryLimit, redeliveryDelay, bytesThresholdHigh, bytesThresholdLow, messagesThresholdHigh, messagesThresholdLow, maximumMessageSize):
        self.name                = name;
        self.moduleName          = moduleName;
        self.subdeploymentName   = subdeploymentName;
        self.jndiName            = jndiName;
        self.deadletterQueueName = deadletterQueueName;
        self.redeliveryLimit     = redeliveryLimit;
        self.redeliveryDelay     = redeliveryDelay;
        self.bytesThresholdHigh	 	= bytesThresholdHigh
        self.bytesThresholdLow   	= bytesThresholdLow
        self.messagesThresholdHigh	= messagesThresholdHigh
        self.messagesThresholdLow	= messagesThresholdLow
        self.maximumMessageSize		= maximumMessageSize
        
        return
    
    def getName(self):
        return self.name
                
    def getModuleName(self):
        return self.moduleName
        
    def getSubdeploymentName(self):
        return self.subdeploymentName
        
    def getJNDIName(self):
        return self.jndiName
                
    def getDeadletterQueueName(self):
        return self.deadletterQueueName
                
    def getRedeliveryLimit(self):
        return self.redeliveryLimit
                
    def getRedeliveryDelay(self):
        return self.redeliveryDelay
                            
    def getBytesThresholdHigh(self):
        return self.bytesThresholdHigh

    def getBytesThresholdLow(self):
        return self.bytesThresholdLow

    def getMessagesThresholdHigh(self):
        return self.messagesThresholdHigh

    def getMessagesThresholdLow(self):
        return self.messagesThresholdLow

    def getMaximumMessageSize(self):
        return self.maximumMessageSize	



class WeightedDistributedQueueSpec:
    def __init__(self, name, moduleName, jndiName, queueMembers):
        self.name                = name;
        self.moduleName          = moduleName;
        self.jndiName            = jndiName;
        self.queueMembers        = queueMembers;
        return
    
    def getName(self):
        return self.name
                
    def getModuleName(self):
        return self.moduleName
        
    def getJNDIName(self):
        return self.jndiName

    def getQueueMembers(self):
        return self.queueMembers

                

class TopicSpec:
    def __init__(self, name, moduleName, subdeploymentName, jndiName, deadletterTopicName, redeliveryLimit, redeliveryDelay, bytesThresholdHigh, bytesThresholdLow, messagesThresholdHigh, messagesThresholdLow, maximumMessageSize):
        self.name                = name;
        self.moduleName          = moduleName;
        self.subdeploymentName   = subdeploymentName;
        self.jndiName            = jndiName;
        self.deadletterTopicName = deadletterTopicName;
        self.redeliveryLimit     = redeliveryLimit;
        self.redeliveryDelay     = redeliveryDelay;
        self.bytesThresholdHigh	 	= bytesThresholdHigh
        self.bytesThresholdLow   	= bytesThresholdLow
        self.messagesThresholdHigh	= messagesThresholdHigh
        self.messagesThresholdLow	= messagesThresholdLow
        self.maximumMessageSize		= maximumMessageSize
        return
    
    def getName(self):
        return self.name
                
    def getModuleName(self):
        return self.moduleName
        
    def getSubdeploymentName(self):
        return self.subdeploymentName
        
    def getJNDIName(self):
        return self.jndiName
        
    def getDeadletterTopicName(self):
        return self.deadletterTopicName
                
    def getRedeliveryLimit(self):
        return self.redeliveryLimit
                
    def getRedeliveryDelay(self):
        return self.redeliveryDelay
                            
    def getBytesThresholdHigh(self):
        return self.bytesThresholdHigh

    def getBytesThresholdLow(self):
        return self.bytesThresholdLow

    def getMessagesThresholdHigh(self):
        return self.messagesThresholdHigh

    def getMessagesThresholdLow(self):
        return self.messagesThresholdLow

    def getMaximumMessageSize(self):
        return self.maximumMessageSize	
                            


class UniformDistributedTopicSpec:
    def __init__(self, name, moduleName, subdeploymentName, jndiName, deadletterTopicName, redeliveryLimit, redeliveryDelay, bytesThresholdHigh, bytesThresholdLow, messagesThresholdHigh, messagesThresholdLow, maximumMessageSize):
        self.name                = name;
        self.moduleName          = moduleName;
        self.subdeploymentName   = subdeploymentName;
        self.jndiName            = jndiName;
        self.deadletterTopicName = deadletterTopicName;
        self.redeliveryLimit     = redeliveryLimit;
        self.redeliveryDelay     = redeliveryDelay;
        self.bytesThresholdHigh	 	= bytesThresholdHigh
        self.bytesThresholdLow   	= bytesThresholdLow
        self.messagesThresholdHigh	= messagesThresholdHigh
        self.messagesThresholdLow	= messagesThresholdLow
        self.maximumMessageSize		= maximumMessageSize
        return
    
    def getName(self):
        return self.name
                
    def getModuleName(self):
        return self.moduleName
        
    def getSubdeploymentName(self):
        return self.subdeploymentName
        
    def getJNDIName(self):
        return self.jndiName
                
    def getDeadletterTopicName(self):
        return self.deadletterTopicName
                
    def getRedeliveryLimit(self):
        return self.redeliveryLimit
                
    def getRedeliveryDelay(self):
        return self.redeliveryDelay
                            
    def getBytesThresholdHigh(self):
        return self.bytesThresholdHigh

    def getBytesThresholdLow(self):
        return self.bytesThresholdLow

    def getMessagesThresholdHigh(self):
        return self.messagesThresholdHigh

    def getMessagesThresholdLow(self):
        return self.messagesThresholdLow

    def getMaximumMessageSize(self):
        return self.maximumMessageSize	

                

class WeightedDistributedTopicSpec:
    def __init__(self, name, moduleName, jndiName, topicMembers):
        self.name                = name;
        self.moduleName          = moduleName;
        self.jndiName            = jndiName;
        self.topicMembers        = topicMembers;
        return
    
    def getName(self):
        return self.name
                
    def getModuleName(self):
        return self.moduleName
        
    def getJNDIName(self):
        return self.jndiName

    def getTopicMembers(self):
        return self.topicMembers

                

class MailSessionSpec:
    def __init__(self, name, jndiName, sessionProperties):
        self.name              = name;
        self.jndiName          = jndiName;
        self.sessionProperties = sessionProperties;
        return
    
    def getName(self):
        return self.name
                
    def getJNDIName(self):
        return self.jndiName
                                
    def getSessionProperties(self):
        return self.sessionProperties

                                

class StartupClassSpec:
    def __init__(self, name, className, arguments, failureIsFatal, loadBeforeAppDeployments):
        self.name                     = name;
        self.className                = className;
        self.arguments                = arguments;
        self.failureIsFatal           = failureIsFatal;
        self.loadBeforeAppDeployments = loadBeforeAppDeployments;
        return
    
    def getName(self):
        return self.name
                
    def getClassName(self):
        return self.className
                                
    def getArguments(self):
        return self.arguments

    def getFailureIsFatal(self):
        return self.failureIsFatal

    def getLoadBeforeAppDeployments(self):
        return self.loadBeforeAppDeployments

class ForeignSeverSpec:
    def __init__(self, name, moduleName, subdeploymentName, jndiURL, \
    jndiInitialContextFactory="weblogic.jndi.InitialContextFactory"):
        self.name                              = name;
        self.moduleName                        = moduleName;	
        self.jndiURL                           = jndiURL;
        self.subdeploymentName                 = subdeploymentName;
        self.jndiInitialContextFactory         = jndiInitialContextFactory
        return
    
    def getName(self):
        return self.name
                
    def getModuleName(self):
        return self.moduleName
        
    def getSubdeploymentName(self):
        return self.subdeploymentName
        
    def getJNDIURL(self):
        return self.jndiURL
                
    def getJndiInitialContextFactory(self):
        return self.jndiInitialContextFactory
                



class ForeignConnectionFactorySpec:
    def __init__(self, name, moduleName, foreignServerName, localJndiName, remoteJndiName, username, password):
        self.name                              = name;
        self.moduleName                        = moduleName;
        self.foreignServerName                 = foreignServerName;
        self.localJndiName		       = localJndiName;
        self.remoteJndiName                    = remoteJndiName;
        self.username                          = username;
        self.password                          = password
        return
    
    def getName(self):
        return self.name
                
    def getModuleName(self):
        return self.moduleName
        
    def getForeignServerName(self):
        return self.foreignServerName

    def getLocalJndi(self):
        return self.localJndiName

    def getRemoteJndi(self):
        return self.remoteJndiName

    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.password


class ForeignDestinationSpec:
    def __init__(self, name, moduleName, foreignServerName, localJndiName, remoteJndiName):
        self.name                              = name;
        self.moduleName                        = moduleName;
        self.foreignServerName                 = foreignServerName;
        self.localJndiName		       = localJndiName;
        self.remoteJndiName                    = remoteJndiName
        return
    
    def getName(self):
        return self.name
                
    def getModuleName(self):
        return self.moduleName
        
    def getForeignServerName(self):
        return self.foreignServerName

    def getLocalJndi(self):
        return self.localJndiName

    def getRemoteJndi(self):
        return self.remoteJndiName

class DbAdapterSpec:
    def __init__(self, instanceJNDI, dataSourceType, dataSourceJNDIName):
        self.instanceJNDI                      =instanceJNDI;
	self.dataSourceType                    = dataSourceType;
        self.dataSourceJNDIName                = dataSourceJNDIName;
        return

    def getInstanceJNDI(self):
        return self.instanceJNDI
    
    def getDataSourceType(self):
        return self.dataSourceType

    def getDataSourceJNDIName(self):
        return self.dataSourceJNDIName

