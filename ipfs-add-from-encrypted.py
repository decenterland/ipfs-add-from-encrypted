#!/usr/bin/env python3
# Takes file in does symmetric encryption with the password you provide
# then  adds it to a running IPFS(ipfs.io) instance.
#
import os
import argparse
import gnupg
import ipfsapi
import tarfile

# Parse command arguments
parser = argparse.ArgumentParser(description='Encrypt file/directory and add it to IPFS')
parser.add_argument('-i','--input', help='File.txt or Directory', required=True)
parser.add_argument('-p','--password', help='Password to encrypt with', required=True)
parser.add_argument('-n','--name', help='Set Encrypted filename')
args = parser.parse_args()

# Set GPG Home directory
gpg = gnupg.GPG(homedir='')
# Set GPG Encoding
gpg.encoding = 'utf-8'
# Get dataToEncrypt full path
dataToEncrypt = (os.path.abspath(args.input))
# Setup tar filename to end with .tar
tarFile = ("{}.tar".format(dataToEncrypt))
# Setup encrypted filename to end with .gpg
encryptedFile = ("{}.gpg".format(dataToEncrypt))
# Setup encrypted tar directory to end with .tar.gpg
tarEncryptedFile = ("{}.tar.gpg".format(dataToEncrypt))

# Setup Renamed File
fileReady = (args.name)
# Setup Renamed Tar File
renamedTar = (args.name)
#
fileReadyOut = ("{}.gpg".format(fileReady))


# Tell module where IPFS instance is located
api = ipfsapi.connect('127.0.0.1', 5001)


def nameSet():
    if args.name:
        os.rename(dataToEncrypt, fileReady)
        
    else:
        os.rename(dataToEncrypt, fileReady)
        
            
def dataTar():
    if os.path.isfile(fileReady):
        return
    else:
        with tarfile.open(tarReady, 'w') as tar:
            tar.dereference=False
            tar.add(tarReady)
            tar.close()

def encryptFile():
    passphrase = (args.password)
    if os.path.isfile(fileReady):
        with open(fileReady, 'rb') as f:
            status = gpg.encrypt(f.read(),
               None,
               encrypt=False,
               symmetric='AES256',
               passphrase=passphrase,
               armor=False,
               output=fileReady + ".gpg")

    else:
        with open(tarReady, 'rb') as f:
            status = gpg.encrypt(f.read(),
               None,
               encrypt=False,
               symmetric='AES256',
               passphrase=passphrase,
               armor=False,
               output=tarReady + ".tar.gpg")

def ipfsFile(encryptedFile):
    try:
        # Add encrypted file to IPFS
        ipfsLoadedFile = api.add(fileReadyOut, wrap_with_directory=True)
        # Return Hash of new IPFS File
        fullHash = (ipfsLoadedFile[1])
        ipfsFile.ipfsHash = fullHash['Hash']
        return(ipfsFile.ipfsHash)
    except:
        # Add encrypted directory to IPFS
        ipfsLoadedFile = api.add(tarReady, wrap_with_directory=True)
        # Return Hash of new IPFS File
        fullHash = (ipfsLoadedFile[1])
        ipfsFile.ipfsHash = fullHash['Hash']
        return(ipfsFile.ipfsHash)
    
def delEncryptedFile():
    if os.path.isfile(encryptedFile):
        os.remove(encryptedFile)
    elif os.path.isfile(tarFile):
        os.remove(tarFile)
        os.remove(tarEncryptedFile)

def main():
    nameSet()
    dataTar()
    encryptFile()
    ipfsFile(encryptedFile)
    print ("File encrypted and added to IPFS with this hash " + ipfsFile(encryptedFile))
    #delEncryptedFile()
    
    
if __name__ == "__main__":    
    main()
