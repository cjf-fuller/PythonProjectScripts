# -*- coding: utf-8 -*-
"""
Created on Tue Oct 04 13:21:27 2016

@author: jk5430
"""

from __future__ import division
import __init__


from detconnutils import DetSocket, DetectorResult, ResultSet



class DetectorConnection(object):
    '''
    Class through which to interact with the detector server written by EJ
    Tries to connect to the server when initialising the class
    '''
    def __init__(self, host = "det.phy.bris.ac.uk", port = 8080):
        #mysocket class, as below
        self.sock = DetSocket()
        self.host = host
        self.port = port
        
        #Defualt setup creates setup structure with sensible values
        self.setup = {}
        self._channels = []
        self._connected = 0        
        
        '''
        Ummed and ahhed about connecting in the init of the class, but went
        for it because it gets its setup from the server (which essentially)
        defines what needs to go into the setup dictionary and overwrites 
        any changes the user might have made before connecting.
        '''
        self.connect()
        self._default_setup()
        
    def connect(self):
        self.sock.connect(self.host, self.port)
        
    def close(self):
        self.sock.close()
        
    def _default_setup(self):
        '''
        Builds a default setup structure from the server with bit of modification
        '''
        
        #This bit is here just in case things have changed on the server (like
        #added functionality) so that this shouldn't break
        self.setup = self.get_server_setup()
        #print 'Received settings from server:'
        #print DetectorResult(self.setup)

        self.setup["user_name"] = "cf"
        self.setup["user_platform"] = "python_27"
        
    def set_poll_time(self, poll_time):
        self.setup["poll_time"] = poll_time
    
    def get_server_setup(self):
        '''
        Gets the server setup
        '''
        self.sock.send('setup')
        setup = self.sock.recv(0, 5.0)
        return setup[0]
            
    def add_channels(self, channels, input_threshold_volts, delays):
        '''
        Activate or update a list detector channels.
        Channels is a list of channel integers.
        Input_threshold_volts is a list whose length must be length of channels
        Delays is a list of ns delays whose length must be length of channels
        '''
        
        for (channel, iv, dl) in zip(channels, input_threshold_volts, delays):
            if channel not in self._channels:
                self._channels.append(channel)
                self.setup["active_channels"] += (1 << (channel - 1))
            
            '''
            WARNING!!! HACK AHEAD!!!!
            Sometimes channel_delay_ns comesback from the server the 
            incorrect length, so have to set it up here, which sucks
            '''
            if len(self.setup["channel_delay_ns"]) != 16:
                self.setup["channel_delay_ns"] = [0 for i in xrange(16)]
            '''
            HACK ENDS HERE
            '''
            
            self.setup["channel_delay_ns"][channel - 1] = dl
            self.setup["input_threshold_volts"][channel - 1] = iv
        
    def remove_channels(self, channels):
        '''
        Removes a specific channels from being requested.
        Should be a list with channel numbers
        '''
        for channel in channels:
            if channel in self._channels:
                self._channels.remove(channel)
                self.setup["active_channels"] -= (1 << (channel - 1))
                
                '''
                Remove any coincidence channels that rely on this singles 
                channel
                '''
                coin_tbd = []                
                for coin in self.setup["coincidence_channels"]:
                    coin_list = [it + 1 for it, val in enumerate('{0:016b}'.format(coin)[::-1]) if int(val) == 1]
                    if channel in coin_list:
                        coin_tbd.append(coin_list)
                for coin in set(tuple(x) for x in coin_tbd):
                    print 'WARNING: this caused coincidence ' + str(coin) + \
                    ' to be removed.'
                    self.remove_coincidence(list(coin))
            else:
                self.close()
                raise ValueError("Channel " + str(channel) + " not active! Something went wrong...")
                
    def add_coincidence(self, channels, coincidence_window_ns):
        '''
        Adds a (currently pairwise) coincidence channel, with a given 
        coincidence window
        '''
        #check whether the channels are actually on:
        if all([i in self._channels for i in channels]):
            co_channel_mask = sum(1 << (chan - 1) for (chan) in channels)
            
            if co_channel_mask not in self.setup["coincidence_channels"]:
                self.setup["coincidence_channels"].append(co_channel_mask)
                self.setup["coincidence_windows_ns"].append(coincidence_window_ns)
            else:
                self.setup["coincidence_windows_ns"][self.setup["coincidence_channels"].index(co_channel_mask)] = coincidence_window_ns
        else:
            print 'WARNING: Cannot add coincidence channels as singles not activated for all channels. Please use add_channels for this'''
            
    def add_histogram(self, channels, histogram_window_ns):
        '''
        Adds a (currently pairwise) histogram channel, with a given 
        histogram window
        '''
        #check whether the channels are actually on:
        if all([i in self._channels for i in channels]):
            co_channel_mask = sum(1 << (chan - 1) for (chan) in channels)
            self.setup["histogram_channels"] = co_channel_mask
            self.setup["histogram_windows_ns"] = histogram_window_ns
        else:
            print 'WARNING: Cannot add histogram channels as singles not activated for all channels. Please use add_channels for this'''            
    
    def remove_coincidence(self, channels):
        '''
        Adds a (currently pairwise) coincidence channel, with a given 
        coincidence window
        '''
        co_channel_mask = sum(1 << (chan - 1) for (chan) in channels)
        if co_channel_mask in self.setup["coincidence_channels"]:
            ind = self.setup["coincidence_channels"].index(co_channel_mask)
            self.setup["coincidence_channels"].remove(co_channel_mask)
            self.setup["coincidence_windows_ns"].pop(ind)
        else:
            self.close()
            raise ValueError("Coincidences " + str(channels) + " not active! Something went wrong...")

    def set_user_details(self, userName):
        '''
        Sets the user's details.
        
        TODO: Add in authentication, the ability to get locks, etc
        '''
        self.setup["user_name"] = userName
        
    def get_results(self, n = 1, raw_results = False, timeout = 35.0): #5
        '''
        Sends setup to the server and waits for n successful results.
        This is then processed into a sensible output format
        Timeout is per message
        List of raw dictionaries returned if with keyword argument raw_results
        = True
        '''
        
        #Sends the setup to the socket
        self.sock.send_setup(self.setup)
        results = self.sock.recv(n, timeout)
        if raw_results == True:
            return results
        else:
            return ResultSet(results, self.setup)
    
    def stream_results(self, n = 1, raw_results = False, timeout = 35.0):
        '''
        Like get results, but doesn't send setup before (or wait to receive it)
        so it might be quicker to receive data. Initial tests indicate this
        may not be the case :)
        '''
        results = self.sock.recv(n, timeout, stream = True)
        if raw_results == True:
            return results
        else:
            return ResultSet(results, self.setup)
        
        
if __name__ == '__main__':
    pass