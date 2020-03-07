import os

def check_app_status(appName, serverName):
    cd('domainRuntime:/AppRuntimeStateRuntime/AppRuntimeStateRuntime')
    print appName
    print serverName
    currentState = cmo.getCurrentState(appName, serverName)
    print currentState
    return currentState

def undeploy_app(appName,targeinst):
    edit()
    startEdit(120000, 120000, 'false')
    print "Undeploying " + appName
    stopApplication(appName)
    undeploy(appName,targetinst)
    save()
    status = activate(300000, "block='true'")
    status.getStatusByServer()
    status.getDetails()

#redirect wlst's own output to null, print lines in the script itself
redirect('retire_undeploy.log','false')

#connect('user','password',url='t3://<adminserver_host>:<adminserver_port>')
connect("weblogic","welcome1","t3://localhost:7001")
cd('AppDeployments')
appList = ls(returnMap='true')
print appList
for appName in appList:
  pwd()
  print '\n'
  print 'Analyzing deployments......' + appName
  print '\n'
  domainConfig()
  cd ('/AppDeployments/'+appName+'/Targets')
  mytargets = ls(returnMap='true')
  # print mytargets
  domainRuntime()
  cd('AppRuntimeStateRuntime')
  cd('AppRuntimeStateRuntime')
  for targetinst in mytargets:
    currentAppStatus=cmo.getCurrentState(appName,targetinst)
    print '=============================================================='
    print '||' + appName
    print '||' + targetinst
    print '||' + currentAppStatus
    print '=============================================================='
    print '\n'
    if currentAppStatus == 'STATE_RETIRED':
      print "This app is RETIRED " + appName
      #email that the script has taken an action
      print '=============================================================='
      print "Undeploying app " + appName
      print '\n'
      # stopApplication(appName)
      undeploy_app(appName,targetinst)
      pwd()
      domainConfig()
      print '=============================================================='
    elif currentAppStatus == 'STATE_ACTIVE':
      print '\n'
      print '##############################################################'
      print '#' + appName + ' is in ACTIVE state'
      print '##############################################################'
      print '\n'
  else:
    print '......................................................................................................................................................................'
    print 'App is not in one of the running state App: ' + appName + ' State: ' + currentAppStatus
    print '......................................................................................................................................................................'
