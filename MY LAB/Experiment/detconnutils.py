# -*- coding: utf-8 -*-
"""
Created on Tue Oct 04 13:21:27 2016

@author: jk5430
"""

from __future__ import division
import __init__
import socket
import json

class ResultSet(object):
    '''
    Takes the full result set (with settings) and makes it nice and simple
    '''
    def __init__(self, raw_results, setup = None):
        self._raw_results = raw_results
        
        #Get setup
        if str(raw_results[0]['type']) == 'setup':
            self.setup = DetectorResult(raw_results[0])
        elif setup['type'] == 'setup':
            self.setup = DetectorResult(setup)
            raw_results.insert(0, setup)
        else:
            raise RuntimeError('Setup isn\'t the first type of result: Some\
            thing went wrong!!')
        
        #Check to see if the bounced setup is ok
        if setup != None:
            self._checkSetupMatch(setup)
        self.results = [DetectorResult(i, raw_results[0]) for i in raw_results[1:]]
        self._buildMembers()
        
         
    def _checkSetupMatch(self, setup):
        '''
        Raise an error if the setups aren't the same
        '''
        omitted = ['connected_users', 'connected_platforms', 'connected_active_channels']
        
        '''
        Both channel_delay_ns and input_threshold_volts contain others info, so if they change in the
        time you send and receive the setup, you'll get an error
        Not sure of best fix here, so omitting these two also...
        '''
        omitted.extend(['channel_delay_ns', 'input_threshold_volts'])        
        
        for key, val in self.setup._raw_result.iteritems():
            if (key not in omitted):
                if (key not in setup):
                    raise RuntimeError('Uh-oh, the keys in sent and received setups don\'t match')
                elif(val != setup[key]):
                    print key, val, setup[key]
                    raise RuntimeError('Uh-oh, some of the values in sent and received setups don\'t match')
    
    def __str__(self):
        outstr = ''
        for it, val in enumerate(self.results):
            outstr += str(it) + ': ' + str(val) + '\n'
        return outstr
    
    def _buildMembers(self):
        '''
        Builds members to access direct lists of all of the member 
        variables of all of the results. eg, to get a list of counts from 
        all channels (ordered by channel), call self.counts() - ie to get the
        counts from channel n from all results call self.counts()[n-1]
        '''
        try:
            for key, val in vars(self.results[0]).iteritems():
                if str(key)[0] != '_':
                    if isinstance(val, list):
                        execstr = 'self.' + str(key) + ' = zip(*[i.'+str(key)+' for i in self.results])'
                    else:
                        execstr = 'self.' + str(key) + ' = [i.'+str(key)+' for i in self.results]'
                    
                    exec execstr
        except IndexError:
            print self.results
                
    def __iter__(self):
        i = 0
        while i < len(self.results):
            yield self.results[i]
            i += 1
                    
            

class DetectorResult(object):
    '''
    Self populating class that takes the detector results dictionary and auto-
    populates the members of the class. 
    Can also trim irrelevant data based on a particular setup
    '''
    def __init__(self, raw_result_dict, setup = None, trim = True):
        
        self._raw_result = raw_result_dict
        self._autopopulate(raw_result_dict)
        if setup != None:
            self._filterInput(setup)

    def _autopopulate(self, raw_result_dict):
        
        #This filter should probably be here
        self._acceptableTerms = ['type', 
                                 'tick_resolution',
                                 'user_platform',
                                 'active_channels',
                                 'coincidence_channels',
                                 'histogram_channels',
                                 'user_name',
                                 'input_threshold_volts',
                                 'coincidence_windows_ns',
                                 'connected_platforms',
                                 'connected_users',
                                 'timetag_unit_ok',
                                 'counts',
                                 'coincidence',
                                 'time',
                                 'channel_delay_ns',
                                 'connected_active_channels',
                                 'delta_time',
                                 'span_time',
                                 'waterloo_data_mode',
                                 'histogram_counts',
                                 'histogram_windows_ns',
                                 'slide_co_all_mask',
                                 'slide_co_move_mask',
                                 'slide_co_width']
        
        
        for key, value in raw_result_dict.iteritems():
            if str(key) == 'error':
                self._throwErr(key, value)
            elif key in self._acceptableTerms:
                if isinstance(value, str) == True or isinstance(value, unicode):
                    execstr = 'self.' + str(key) + ' = \'' + value + '\''
                else:
                    execstr = 'self.' + str(key) + ' = ' + str(value)
                exec execstr
                '''
                May be a bit of a bug or I just don't understand, but it seems
                to come back as many empty lists and one not empty. So I got rid
                of the empties
                '''
                if key == 'histogram_counts':
                    temp = []
                    [temp.extend(i) for i in self.histogram_counts if len(i) != 0]
                    self.histogram_counts = temp
                    
    def _filterInput(self, setup):
        if self.type == 'counts':
            self.channels = [it + 1 for it, val in enumerate('{0:016b}'.format(setup['active_channels'])[::-1]) if int(val) == 1]
            self.counts = [val for it, val in enumerate(self.counts) if (it + 1) in self.channels]
            self.coincidence_channels = [[it + 1 for it, val in enumerate('{0:016b}'.format(i)[::-1]) if int(val) == 1] for i in setup['coincidence_channels']]
            self.histogram_channels = [it + 1 for it, val in enumerate('{0:016b}'.format(setup['histogram_channels'])[::-1]) if int(val) == 1]

    def _throwErr(self, key, val):
        '''
        This may be expanded if need be
        '''
        raise UserWarning(str(val))
        
    
    def __repr__(self):
        return str(vars(self))
        
    
    def __str__(self):
        returnstr = 'DetectorResult:\n'
        for key, val in vars(self).iteritems():
            if str(key)[0] != '_':
                returnstr += '\t' + str(key) + ' = ' + str(val)+'\n'
        return returnstr
        

class DetSocket(object):
    '''demonstration class only
    - coded for clarity, not efficiency
    '''
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self._connected = 0
        self.need_setup = 1

    def send_setup(self, setup):
        #print "------------------- sending setup ----------------------"
#        print self.current_setup
        message = json.dumps(setup)
        self.send(message)
        #print message
        #print "--------------------------------------------------------"
 
    def connect(self, host, port):
        try:
            self.sock.connect((host, port))
            self._connected = 1
        except socket.error, v:
            self._connected = 0
            raise socket.error, v

    def send(self, msg):
        if self._connected == 0:
            raise RuntimeError("socket connection broken")
        else:
            totalsent = 0
            while totalsent < len(msg):
                sent = self.sock.send(bytes(msg[totalsent:]))
                if sent == 0:
                    raise RuntimeError("socket connection broken")
                totalsent = totalsent + sent

    def recv(self, n_messages, timeout, stream = False):
        '''
        This will listen for n messages AFTER receiving the setup bounce back
        from the server - ie you know that what you recieve is after any 
        changes have been made
        '''
        if self._connected == 0:
            raise RuntimeError("socket connection broken")
        else:
            chunks = []
            mess_recd = 0
            if stream:
                found_setup = 1
                n_messages -= 1
            else:
                found_setup = 0
            while mess_recd < (n_messages+1):
                self.sock.settimeout(timeout)
                chunk = self.sock.recv(2048)
                self.sock.settimeout(None)
                if chunk == '':
                    raise RuntimeError("socket connection broken")
                done = 0
                end = 0
                # Look for { ... } pairs, and consider them to be complete messages
                while not done:
                    start = chunk.find('{', end);
                    if (start >= 0):
                        end = chunk.find('}', start)
                        if (end >= 0):
                            json_str = chunk[start:end+1]
                            json_data = json.loads(json_str)
                            if json_data["type"] == "setup":
                                '''
                                This is needed as I think it spits a setup to
                                everyone if ANYONE makes a setup request
                                '''
                                if found_setup == 0:
                                    chunks.append(json_data)
                                found_setup = 1
                            elif found_setup == 1:
                                mess_recd += 1
                                chunks.append(json_data)
                        else:
                            done = 1
                    else:
                        done = 1
            
            #Probably not the best idea ever, but if you get too many messages,
            #trim it!
            return chunks[:n_messages+1]

    def close(self):
        self.sock.close()
        self._connected = 0        
    
if __name__ == '__main__':
    pass