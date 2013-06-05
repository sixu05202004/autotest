#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Python API for Hudson

Examples:

    Hudson.get_jobs()
    Hudson.create_job('ade', EMPTY_CONFIG_XML)
    Hudson.disable_job('ade')
    Hudson.copy_job('ade', 'ade_copy')
    Hudson.enable_job('ade_copy')
    Hudson.reconfig_job('ade_copy', RECONFIG_XML)

    Hudson.delete_job('ade')
    Hudson.delete_job('ade_copy')

    # build a parameterized job
    Hudson.build_job('api-test', {'param1': 'test value 1',
                                  'param2': 'test value 2'})
'''

import urllib2
import urllib
import base64
import json
import httplib
from hudson_template import build

INFO = 'api/json'
JOB_INFO = 'job/%(name)s/api/json?depth=0'
Q_INFO = 'queue/api/json?depth=0'
CREATE_JOB = 'createItem?name=%(name)s'  # also post config.xml
CONFIG_JOB = 'job/%(name)s/config.xml'
DELETE_JOB = 'job/%(name)s/doDelete'
ENABLE_JOB = 'job/%(name)s/enable'
DISABLE_JOB = 'job/%(name)s/disable'
COPY_JOB = 'createItem?name=%(to_name)s&mode=copy&from=%(from_name)s'
BUILD_JOB = 'job/%(name)s/build'
BUILD_WITH_PARAMS_JOB = 'job/%(name)s/buildWithParameters'

CREATE_NODE = 'computer/doCreateItem?%s'
DELETE_NODE = 'computer/%(name)s/doDelete'
NODE_INFO = 'computer/%(name)s/api/json?depth=0'
NODE_TYPE = 'hudson.slaves.DumbSlave$DescriptorImpl'


class HudsonException(Exception):
    pass


def auth_headers(username, password):
    '''
    Simple implementation of HTTP Basic Authentication.
    Returns the 'Authentication' header value. For example:
    "Authorization: Basic jdhaHY0="
    '''
    return 'Basic ' + base64.encodestring('%s:%s' % (username, password))[:-1]


class Hudson(object):

    def __init__(self, url, username=None, password=None):
        '''
        Create handle to Hudson instance.

        @param url: URL of Hudson server
        @type  url: str
        '''
        if url[-1] == '/':
            self.server = url
        else:
            self.server = url + '/'
        if username is not None and password is not None:
            self.auth = auth_headers(username, password)
        else:
            self.auth = None

    def get_job_info(self, name):
        try:
            response = self.Hudson_open(urllib2.Request(self.server +
                                                        JOB_INFO % locals()))
            if response:
                return json.loads(response)
            else:
                raise HudsonException('job[%s] does not exist' % name)
        except urllib2.HTTPError:
            raise HudsonException('job[%s] does not exist' % name)
        except ValueError:
            raise HudsonException("Could not parse JSON info for job[%s]" %
                                  name)

    def debug_job_info(self, job_name):
        '''
        Print out job info in more readable format
        '''
        for k, v in self.get_job_info(job_name).iteritems():
            print k, v

    def Hudson_open(self, req):
        '''
        Utility routine for opening an HTTP request to a Hudson server.
        '''
        try:
            if self.auth:
                req.add_header('Authorization', self.auth)
            return urllib2.urlopen(req).read()
        except urllib2.HTTPError, e:
            if e.code in [401, 403, 500]:
                raise HudsonException('Error in request. Possibly\
                    authentication failed [%s]' % (e.code))

    def get_queue_info(self):
        '''
        @return: list of job dictionaries
        '''
        return json.loads(self.Hudson_open(urllib2.Request(self.server +
                                                           Q_INFO)))['items']

    def get_info(self):
        """
        Get information on this Hudson server.  This information
        includes job list and view information.

        @return: dictionary of information about Hudson server
        @rtype: dict
        """
        try:
            return json.loads(self.Hudson_open(urllib2.Request(self.server +
                                                               INFO)))
        except urllib2.HTTPError:
            raise HudsonException("Error communicating with server[%s]" %
                                  self.server)
        except httplib.BadStatusLine:
            raise HudsonException("Error communicating with server[%s]" %
                                  self.server)
        except ValueError:
            raise HudsonException("Could not parse JSON info for server[%s]" %
                                  self.server)

    def get_jobs(self):
        """
        Get list of jobs running.  Each job is a dictionary with
        'name', 'url', and 'color' keys.

        @return: list of jobs
        @rtype: [ { str: str} ]
        """
        return self.get_info()['jobs']

    def copy_job(self, from_name, to_name):
        '''
        Copy a Hudson job

        @param from_name: Name of Hudson job to copy from
        @type  from_name: str
        @param to_name: Name of Hudson job to copy to
        @type  to_name: str
        '''
        self.get_job_info(from_name)
        self.Hudson_open(urllib2.Request(self.server +
                                         COPY_JOB % locals(), ''))
        if not self.job_exists(to_name):
            raise HudsonException('create[%s] failed' % (to_name))

    def delete_job(self, name):
        '''
        Delete Hudson job permanently.

        @param name: Name of Hudson job
        @type  name: str
        '''
        self.get_job_info(name)
        self.Hudson_open(urllib2.Request(self.server +
                                         DELETE_JOB % locals(), ''))
        if self.job_exists(name):
            raise HudsonException('delete[%s] failed' % (name))

    def enable_job(self, name):
        '''
        Enable Hudson job.

        @param name: Name of Hudson job
        @type  name: str
        '''
        self.get_job_info(name)
        self.Hudson_open(urllib2.Request(self.server +
                                         ENABLE_JOB % locals(), ''))

    def disable_job(self, name):
        '''
        Disable Hudson job. To re-enable, call enable_job().

        @param name: Name of Hudson job
        @type  name: str
        '''
        self.get_job_info(name)
        self.Hudson_open(urllib2.Request(self.server +
                                         DISABLE_JOB % locals(), ''))

    def job_exists(self, name):
        '''
        @param name: Name of Hudson job
        @type  name: str
        @return: True if Hudson job exists
        '''
        try:
            self.get_job_info(name)
            return True
        except HudsonException:
            return False

    def create_job(self, name, config_xml):
        '''
        Create a new Hudson job

        @param name: Name of Hudson job
        @type  name: str
        @param config_xml: config file text
        @type  config_xml: str
        '''
        if self.job_exists(name):
            raise HudsonException('job[%s] already exists' % (name))

        headers = {'Content-Type': 'text/xml'}
        self.Hudson_open(urllib2.Request(self.server + CREATE_JOB % locals(),
                                         config_xml, headers))
        if not self.job_exists(name):
            raise HudsonException('create[%s] failed' % (name))

    def get_job_config(self, name):
        '''
        Get configuration of existing Hudson job.

        @param name: Name of Hudson job
        @type  name: str
        '''
        get_config_url = self.server + CONFIG_JOB % locals()
        return self.Hudson_open(urllib2.Request(get_config_url))

    def reconfig_job(self, name, config_xml):
        '''
        Change configuration of existing Hudson job.

        @param name: Name of Hudson job
        @type  name: str
        @param config_xml: New XML configuration
        @type  config_xml: str
        '''
        self.get_job_info(name)
        headers = {'Content-Type': 'text/xml'}
        reconfig_url = self.server + CONFIG_JOB % locals()
        self.Hudson_open(urllib2.Request(reconfig_url, config_xml, headers))

    def build_job_url(self, name, parameters=None, token=None):
        '''
        @param parameters: parameters for job, or None.
        @type  parameters: dict
        '''
        if parameters:
            if token:
                parameters['token'] = token
            return self.server + BUILD_WITH_PARAMS_JOB % locals() + '?' + \
                urllib.urlencode(parameters)
        elif token:
            return self.server + BUILD_JOB % locals() + '?' + \
                urllib.urlencode({'token': token})
        else:
            return self.server + BUILD_JOB % locals()

    def build_job(self, name, parameters=None, token=None):
        '''
        @param parameters: parameters for job, or None.
        @type  parameters: dict
        '''
        if not self.job_exists(name):
            raise HudsonException('no such job[%s]' % (name))
        return self.Hudson_open(urllib2.Request(self.build_job_url(name,
                                                                   parameters,
                                                                   token)))

    def get_node_info(self, name):
        try:
            response = self.Hudson_open(urllib2.Request(self.server +
                                                        NODE_INFO % locals()))
            if response:
                return json.loads(response)
            else:
                raise HudsonException('node[%s] does not exist' % name)
        except urllib2.HTTPError:
            raise HudsonException('node[%s] does not exist' % name)
        except ValueError:
            raise HudsonException("Could not parse JSON info for node[%s]" %
                                  name)

    def node_exists(self, name):
        '''
        @param name: Name of Hudson node
        @type  name: str
        @return: True if Hudson node exists
        '''
        try:
            self.get_node_info(name)
            return True
        except HudsonException:
            return False

    def delete_node(self, name):
        '''
        Delete Hudson node permanently.

        @param name: Name of Hudson node
        @type  name: str
        '''
        self.get_node_info(name)
        self.Hudson_open(urllib2.Request(self.server +
                                         DELETE_NODE % locals(), ''))
        if self.node_exists(name):
            raise HudsonException('delete[%s] failed' % (name))

    def create_node(self, name, numExecutors=2, nodeDescription=None,
                    remoteFS='/var/lib/Hudson', labels=None, exclusive=False):
        '''
        @param name: name of node to create
        @type  name: str
        @param numExecutors: number of executors for node
        @type  numExecutors: int
        @param nodeDescription: Description of node
        @type  nodeDescription: str
        @param remoteFS: Remote filesystem location to use
        @type  remoteFS: str
        @param labels: Labels to associate with node
        @type  labels: str
        @param exclusive: Use this node for tied jobs onlu
        @type  exclusive: boolean
        '''
        if self.node_exists(name):
            raise HudsonException('node[%s] already exists' % (name))

        mode = 'NORMAL'
        if exclusive:
            mode = 'EXCLUSIVE'

        params = {
            'name': name,
            'type': NODE_TYPE,
            'json': json.dumps({
                'name': name,
                'nodeDescription': nodeDescription,
                'numExecutors': numExecutors,
                'remoteFS': remoteFS,
                'labelString': labels,
                'mode': mode,
                'type': NODE_TYPE,
                'retentionStrategy':
                {'stapler-class': 'hudson.slaves.RetentionStrategy$Always'},
                'nodeProperties': {'stapler-class-bag': 'true'},
                'launcher': {'stapler-class': 'hudson.slaves.JNLPLauncher'}
            })
        }

        self.Hudson_open(urllib2.Request(self.server +
                                         CREATE_NODE %
                                         urllib.urlencode(params)))
        if not self.node_exists(name):
            raise HudsonException('create[%s] failed' % (name))
'''
if __name__ == '__main__':
    a=Hudson(url='http://10.0.2.204:8080/hudson/')
    test = {'shell': None,
            'start_time': None,
            'mail_address': None,
            'name': None,
            'svn': None}
    #a.delete_job('000011')
    a.create_job('ab_11',build(test))
    #print a.disable_job('000011')
    #print a.get_node_info('205')
'''