#! /usr/bin/python

import telnetlib
import socket
import thread

class PortTester(object):

  thread_count = 0

  def __init__(self, input, log):

      for row in input:
          thread.start_new(self.testPort, (row[0], row[1], log))
          self.thread_count = self.thread_count + 1
      while self.thread_count > 0:
          pass
       
       
  def testPort(self, host, port, log):
      #print 'Testing %s on port %s' % (host, port)
      try:
          connection = telnetlib.Telnet(host, port, 10)
          log.write('%s,%s,pass\n' % (host,port))
          log.flush()
          print('%s:%s pass' %(host, port))
      except:
          log.write('%s,%s,fail\n' % (host,port))
          log.flush()
          print('%s:%s fail' %(host, port))
      self.thread_count = self.thread_count - 1

def main():
    
    output = open('results.txt', 'w')
    default_pass = False
    fallback_pass = False
    
    print("\nAerohive Cloud Reachbility Test")
    print("Written by Daniel O'Rorke")
    print("(c) 2015 Aerohive Networks.\n\n")
    
    print("Testing internet access (aerohive.com:80)")
    PortTester([["aerohive.com","80"]], output)
    
    print ("\nTesting the ability to reach Hive Manager NG servers using default settings.")
    #HMNG servers will not respond to us because our serial number is not registered in their DB!
    #NG_Default_Servers = [['redirector.aerohive.com', '22'],['redirector.aerohive.com', '12222'], ['hmng-prd-ie-cwpm-01.aerohive.com', '12222'], ['hmng-prd-ie-cwps-01.aerohive.com', '12222'], ['hmng-prd-ie-cwps-02.aerohive.com', '12222'], ['hmng-prd-va-cwpm-01.aerohive.com', '12222'], ['hmng-prd-va-cwps-01.aerohive.com', '12222'], ['hmng-prd-va-cwps-02.aerohive.com', '12222']]
    # Port 12222 seems to fail for both UDP and TCP. Not sure why. Need response from CloudOps to get answers.
    NG_Default_Servers = [['redirector.aerohive.com', '22']]
    PortTester(NG_Default_Servers, output)
    udpTestForNG('redirector.aerohive.com', 12222, output)
    
    
    print("\nTesting fallback ports...")
    #HMNG servers will not respond to us because our serial number is not registered in their DB!
    #NG_Fallback_Servers = [['redirector.aerohive.com', '22'],['redirector.aerohive.com', '12222'], ['hmng-prd-ie-cwpm-01.aerohive.com', '443'], ['hmng-prd-ie-cwps-01.aerohive.com', '443'], ['hmng-prd-ie-cwps-02.aerohive.com', '443'], ['hmng-prd-va-cwpm-01.aerohive.com', '443'], ['hmng-prd-va-cwps-01.aerohive.com', '443'], ['hmng-prd-va-cwps-02.aerohive.com', '443']]
    NG_Fallback_Servers = [['redirector.aerohive.com', '22'],['redirector.aerohive.com','443']]
    PortTester(NG_Fallback_Servers, output)
    
    print("\nTesting ID Manager Communication")
    IDM_Servers = [['auth.aerohive.com', '443'], ['auth.aerohive.com', '2083'], ['auth.aerohive.com', '80'], ['idmanager.aerohive.com', '443'], ['idmanager-ca.aerohive.com', '443']]
    PortTester(IDM_Servers, output)
    
    print("\nTesting Update Server Communication")
    Update_Servers = [['hmupdates.aerohive.com', '443']]
    PortTester(Update_Servers, output)
    
    print("\nTesting Update Server Communication")
    Update_Servers = [['hmupdates.aerohive.com', '443']]
    PortTester(Update_Servers, output)

    
    print("\n\nTest complete.")

# This function crafts a UDP test specifically for HiveManager.
# A basic UDB test will fail on 12222.
def udpTestForNG (host, port, log):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print 'Failed to create socket'
        sys.exit()
    #host = input[0] # first element in passed array.
    #port = input[1] # second element in passes array.
    message = "70408000000000000000012c040045000009f61900001f4000380000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
    hexMessage = bytearray(message.decode("hex")) #.decode("hex");
    
    try:
        s.sendto(hexMessage, (host, port))
        # receive data from the client
        s.setblocking(0) # Set to non-blocking.
        s.settimeout(10) # give the server 10 seconds to respond.
        data = s.recvfrom(1024)
        reply = data[0]
        address = data[1]
        # write the result to the log
        log.write('%s,%s,pass\n' % (host,port))
        log.flush()
        print('%s:%s pass Response:%s' %(host, port, reply))
        
    except socket.error, msg:
        print host + ':' + str(port) + ' failed\nError code: ' + str(msg[0]) + '  Message: ' + msg[1]
        # write to the log
        log.write('%s,%s,fail\n' % (host,port))
        log.flush()

if __name__ == '__main__':
  main()
