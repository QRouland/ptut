import random
import string
import hashlib
import sys


sys.path[:0]=['../']
from m.log import *
from m.loadConf import *
from m.login import *


class testConf(object):
    """
    Test on Conf File Loading
    """
    def createConf(self) :
        """
        Create a random conf file named ConfTest.
        Save key ,value in self.assos[].
        """
        print "Create Random Conf File"
        f = open("ConfTest", "w")
        j = random.randint(5,20)
        self.assos = [""]*j
        for i in range (0,j) :
            key=''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(random.randint(1,20)))
            value = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(random.randint(1,20)))
            self.assos[i] = [key,value]
            f.write(key+" "+value+"\n")
        f.close()
        print "Random Conf File Create"


    def testLoadConf(self,LoadConfObject) :
        """
        Test loadValue method LoadConf object
        """
        print "\nTesting All Valid Keys"
        err=0
        for key,value in self.assos :
            confValue = LoadConfObject.loadValue(key)
            if confValue == "error" :
                print "NOK : Error an valid key give return an error"
                err +=1
            if value == confValue :
                print "OK : Succesfull Load Config Value"
            else :
                print " NOK : Value return is not the right value"
                err +=1

        if err>0:
            print "TEST FAIL : all key were not load succesfully"
        else :
            print "TEST SUCESSFULL : all key were load succesfully"



        print "\nTesting invalid keys"
        err = 0
        for i in range(10):
            confValue =  LoadConfObject.loadValue(
            ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(random.randint(1,20))))
            if confValue != "error":
                print "NOK : An value was return"
                err += 1
            else :
                print "OK : return an error"

        if err>0:
            print "TEST FAIL : don't return only error'"
        else :
            print "TEST SUCESSFULL : return only error"


class testLogin(object):
    def createAllowFile(self) :
        """
        Create a allow file named AllowTest.
        Save key ,value in self.assos[].
        """
        print "Create Allow File"
        f = open("AllowTest", "w")
        j = random.randint(5,20)
        self.assos = [""]*j
        for i in range (0,j) :
            name=''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(random.randint(1,20)))
            passwd = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(random.randint(1,20)))
            hashPasswd = hashlib.sha224(passwd).hexdigest()
            self.assos[i] = [name,passwd]
            f.write(name+","+hashPasswd+"\n")
        f.close()
        print "Random Allow File Create"

    def testLogin(self,LoginObject) :
        """
        Test CheckLogin method LoadConf object
        """
        print "\nTesting Valid Login Information "
        err=0
        for name,passwd in self.assos :
            value = LoginObject.checkLogin(name,passwd)
            if value == True:
                print "OK : Return True"
            else :
                print "NOK : Return False"
                err +=1

        if err==0:
            print "TEST SUCESSFULL : All Login Were Succesfull"
        else :
            print "TEST FAIL: All Login  Were Not Succesfull"



        print "\nTesting invalid id and password"
        err = 0
        for i in range(10):
            value =  LoginObject.checkLogin(
            ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(random.randint(1,20))),
            ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(random.randint(1,20))))

            if value == True:
                print "NOK : Return True"
                err += 1
            else :
                print "OK : Return False"

        if err>0:
            print "TEST FAIL : Login Ok With Invalid Information"
        else :
            print "TEST SUCESSFULL :  Login Not Ok With Invalid Information"

        print "\nTesting invalid id and correct password"
        err = 0
        for name,passwd in self.assos :
            name = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(random.randint(1,20)))
            value =  LoginObject.checkLogin(name,passwd)

            if value == True:
                print "NOK : Return True"
                err += 1
            else :
                print "OK : Return False"

        if err>0:
            print "TEST FAIL : Login Ok With Invalid Information"
        else :
            print "TEST SUCESSFULL :  Login Not Ok With Invalid Id"

        print "\nTesting invalid password and correct id"
        err = 0
        for name,passwd in self.assos :
            passwd = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(random.randint(1,20)))
            value =  LoginObject.checkLogin(name,passwd)

            if value == True:
                print "NOK : Return True"
                err += 1
            else :
                print "OK : Return False"

        if err>0:
            print "TEST FAIL : Login Ok With Invalid Information"
        else :
            print "TEST SUCESSFULL :  Login Not Ok With Invalid Password"





if __name__ == "__main__":
    print "START TEST LOADCONFIG METHODS"
    test= testConf()
    test.createConf();
    config = LoadConf("ConfTest")
    test.testLoadConf(config);
    print "\nEND TEST CONFIG FILE LOADING METHODS"
    print "\nSTART TEST LOGIN METHODS"
    test = testLogin()
    test.createAllowFile()
    login = Login("AllowTest")
    test.testLogin(login)
    print "\nEND TEST LOGIN METHODS"

