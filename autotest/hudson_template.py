#-*- coding: utf-8 -*-
"""
    hudson_tempalte.py
    ~~~~~~~~~

    hudson config xml template

    :copyright: (c) 2013
    :license: BSD, see LICENSE for more details.
"""
import time


class template(object):
    head = u'''
            <project>
            <actions/>
            <description/>
            <project-properties class="java.util.concurrent.ConcurrentHashMap">

            <entry>
            <string>hudson-plugins-disk_usage-DiskUsageProperty</string>
            <base-property>
            <propertyOverridden>false</propertyOverridden>
            </base-property>
            </entry>
            <entry>
            <string>logRotator</string>
            <log-rotator-property>
            <originalValue class="hudson.tasks.LogRotator">
            <daysToKeep>-1</daysToKeep>
            <numToKeep>5</numToKeep>
            <artifactDaysToKeep>-1</artifactDaysToKeep>
            <artifactNumToKeep>-1</artifactNumToKeep>
            </originalValue>
            <propertyOverridden>false</propertyOverridden>
            </log-rotator-property>
            </entry>

            <entry>
            <string>
            org-hudsonci-plugins-snapshotmonitor-WatchedDependenciesProperty
            </string>
            <base-property>
            <propertyOverridden>false</propertyOverridden>
            </base-property>
            </entry>

            <entry>
            <string>cleanWorkspaceRequired</string><boolean-property><originalValue class="boolean">true</originalValue><propertyOverridden>false</propertyOverridden></boolean-property></entry>

            <entry>

            <string>hudson-triggers-SCMTrigger</string>
            <trigger-property>
            <propertyOverridden>false</propertyOverridden>
            </trigger-property>
            </entry>
            <entry>
            <string>builders</string>
            <describable-list-property>
            <originalValue class="hudson.util.DescribableList">
            <hudson.tasks.Shell>
            <command>%(shell)s</command>
            </hudson.tasks.Shell>
            </originalValue>
            <propertyOverridden>false</propertyOverridden>
            </describable-list-property>
            </entry>

            <entry>
            <string>hudson-triggers-TimerTrigger</string>
            <trigger-property>
            <originalValue class="hudson.triggers.TimerTrigger">
            <spec>%(start_time)s</spec>
            </originalValue>
            <propertyOverridden>false</propertyOverridden>
            </trigger-property>
            </entry>


            <entry>
            <string>hudson-plugins-emailext-ExtendedEmailPublisher</string>
            <external-property>
            <originalValue class="hudson.plugins.emailext.ExtendedEmailPublisher">
            <recipientList>%(mail_address)s</recipientList>
            <configuredTriggers>
            <hudson.plugins.emailext.plugins.trigger.FailureTrigger>
            <email>
            <recipientList>%(mail_address)s</recipientList>
            <subject>%(name)s</subject>
            <body>$DEFAULT_CONTENT</body>
            <sendToDevelopers>false</sendToDevelopers>
            <includeCulprits>false</includeCulprits>
            <sendToRecipientList>true</sendToRecipientList>
            </email>
            </hudson.plugins.emailext.plugins.trigger.FailureTrigger>
            <hudson.plugins.emailext.plugins.trigger.SuccessTrigger>
            <email>
            <recipientList>%(mail_address)s</recipientList>
            <subject>%(name)s</subject>
            <body>$DEFAULT_CONTENT</body>
            <sendToDevelopers>false</sendToDevelopers>
            <includeCulprits>false</includeCulprits>
            <sendToRecipientList>true</sendToRecipientList>
            </email>
            </hudson.plugins.emailext.plugins.trigger.SuccessTrigger>
            </configuredTriggers>
            <contentType>text/html</contentType>
            <defaultSubject>%(name)s</defaultSubject>
            <defaultContent/>
            </originalValue>
            <propertyOverridden>false</propertyOverridden>
            <modified>true</modified>
            </external-property>
            </entry>
            '''

    tail = u'''
            </project-properties>
            <keepDependencies>false</keepDependencies>
            <creationTime>%(create_time)s</creationTime>
            <properties/>
            <cascadingChildrenNames class="java.util.concurrent.CopyOnWriteArraySet"/>
            <cascading-job-properties class="java.util.concurrent.CopyOnWriteArraySet">
            <string>hudson-plugins-disk_usage-DiskUsageProperty</string>
            <string>
            org-hudsonci-plugins-snapshotmonitor-WatchedDependenciesProperty
            </string>
            </cascading-job-properties>
            <scm class="hudson.scm.NullSCM"/>
            <canRoam>false</canRoam>
            <disabled>false</disabled>
            <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
            <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
            <concurrentBuild>false</concurrentBuild>
            <cleanWorkspaceRequired>false</cleanWorkspaceRequired>
            <builders/>
            </project>
            '''


def _build_svn(svnlist):
    svn_head = u'''<entry>
            <string>scm</string>
            <scm-property>
            <originalValue class="hudson.scm.SubversionSCM">
            <locations>
            '''
    svn_tail = u'''
            </locations>
            <excludedRegions/>
            <includedRegions/>
            <excludedUsers/>
            <excludedRevprop/>
            <excludedCommitMessages/>
            <workspaceUpdater class="hudson.scm.subversion.UpdateUpdater"/>
            </originalValue>
            <propertyOverridden>false</propertyOverridden>
            </scm-property>
            </entry>'''
    svn_content_temp = u'''
            <hudson.scm.SubversionSCM_-ModuleLocation>
            <remote>%s</remote>
            <local>%s</local>
            <depthOption>infinity</depthOption>
            <ignoreExternalsOption>false</ignoreExternalsOption>
            </hudson.scm.SubversionSCM_-ModuleLocation>'''
    if isinstance(svnlist, list):
        svn_content = ''.join([svn_content_temp % item for item in svnlist])
        return svn_head + svn_content + svn_tail

    return ''


def build(args=None):
    tem = template()
    '''
    set locals
    '''
    create_time = str(int(time.time()))
    shell = ''
    start_time = '# no crontab time'
    mail_address = 'admin@autotest.com'
    name = 'auto test result'
    if args and isinstance(args, dict):
        temp = [(item, locals().get(item)) for item in ['shell', 'start_time', 'mail_address', 'name'] if not args.get(item)]
        if temp:
            args.update(dict(temp))
        head = tem.head % args
    else:
        head = tem.head % locals()
    tail = tem.tail % locals()

    if args and isinstance(args, dict) and args.get('svn', []):
        svn = _build_svn(args.get('svn', []))
        return head + svn + tail
    else:
        return head + tail
