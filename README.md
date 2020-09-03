![Linux](https://img.shields.io/badge/-Linux-grey?logo=linux)
![Usage](https://img.shields.io/badge/Usage-FEFF%20input%20files%20generator-blue)
![Python](https://img.shields.io/badge/Python-v3.6%5E-orange?logo=python)

## Index

* [Description](#description)
* [Features](#features)
* [Installation](#installation)

## Description

**FEFF input files generator** is a cli application for generating input files for 
[FEFF9](http://feff.phys.washington.edu/feffproject-feff.html) program. 
Input files are generated for atom-doped samples in a crystal structure 
with defects such as 
* substitutions, 
* implants, 
* antisites, 
* substitutionsetc.


## Features

* Automatic generation of project folders.
* Automatic start of the calculation using the generated SLURM script.
* Do calculation on the remote host by using ssh protocol.
* Wide possibilities of choosing the way of placing the wanted atom / atoms in the target crystal structure.
* Ability to filter atoms by tag / ipot / coordinates / distance.
* Separate configuration file
* WebUI menu for changing base config options.

# 
## Installation

### 1. Create Virtual Python Environment and Install Python3 interpreter
Additional information on https://www.python.org/downloads/
and 
[Creation of virtual environments](https://docs.python.org/3/library/venv.html)

or simple way to create subfolder venv (with python packages) inside the current directory:

    $ python -m venv venv

### 2. Clone this repository into your directory

    $ mkdir feff_generate_input_files && cd feff_generate_input_files
    
    
    $ git clone https://github.com/xyz-man/feff_generate_input_files.git
        or
    $ git clone -b develop https://github.com/xyz-man/feff_generate_input_files.git

### 3. Install requirements


    $ pip install -r requirements.txt

  
 ### 4. Setup password-free ssh configuration to connect on remote server
 On your localhost execute the next command to generate a pair of authentication keys. Do not enter a passphrase:
    
    $ ssh-keygen -t rsa
    Generating public/private rsa key pair.
    Enter file in which to save the key (/home/a/.ssh/id_rsa): 
    Created directory '/home/a/.ssh'. 
    Enter passphrase (empty for no passphrase): 
    Enter same passphrase again: 
    Your identification has been saved in /home/a/.ssh/id_rsa.
    Your public key has been saved in /home/a/.ssh/id_rsa.pub.
    
 Then copy `id_rsa.pub` to remote host by using certain `User Login` and `IP-address`
 In example remote host has `10.88.0.245` ip-address and the remote host user login is: `wien2k`
 
    $ ssh-copy-id -i ~/.ssh/id_rsa.pub wien2k@10.88.0.245
    /usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/localhostuser/.ssh/id_rsa.pub"
    The authenticity of host '10.88.0.245 (10.88.0.245)' can't be established.
    ECDSA key fingerprint is SHA256:WZ34iul54wKqqS5XhBG8N/sfthtH26q5GoPOjcdgOFw.
    Are you sure you want to continue connecting (yes/no)? yes
    /usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
    /usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
    wien2k@10.88.0.245's password: 
    
    Number of key(s) added: 1
    
    Now try logging into the machine, with:   "ssh 'wien2k@10.88.0.245'"
    and check to make sure that only the key(s) you wanted were added.
    
 ### 5. Setup password-free NFS share folder for project directories
 On your localhost and remote host install nfs client service:
        
        $apt-get install nfs-common
 
On the NFS server, edit `/etc/exports` and add the local and remote host access permission
by changing the `10.88.0.1/24` IP pool:

    $ cat /etc/exports 
    # /etc/exports: the access control list for filesystems which may be exported
    #               to NFS clients.  See exports(5).
    #
    # Example for NFSv2 and NFSv3:
    # /srv/homes       hostname1(rw,sync,no_subtree_check) hostname2(ro,sync,no_subtree_check)
    #
    # Example for NFSv4:
    # /srv/nfs4        gss/krb5i(rw,sync,fsid=0,crossmnt,no_subtree_check)
    # /srv/nfs4/homes  gss/krb5i(rw,sync,no_subtree_check)
    #
    /mnt/nfsv4/nfs_share    10.88.0.1/24(rw,no_root_squash,no_subtree_check,crossmnt,fsid=0)
    
On NFS-client machine (localhost or remote host) 

print the nfs mount folders exported by NFS-server _(Ex.: nfs server ip-address is `10.88.0.251`)_:

    $# showmount -e 10.88.0.251
    Export list for 10.88.0.251:
    /mnt/nfsv4/nfs_share 10.88.0.1/24

edit /etc/fstab and write line with mount NFS share options:

    $ #10.88.0.251:/mnt/nfsv4/nfs_share    /mnt/nfsv4/abel_share   nfs4   soft,intr,rsize=8192,wsize=8192   0   0
      10.88.0.251:/    /mnt/nfsv4/abel_share   nfs4   soft,intr,rsize=8192,wsize=8192   0   0
      
 or execute mount command:
 
    $ mount.nfs4 10.88.0.251:/ /mnt/nfsv4/abel_share -o rw
    
 
directory `/mnt/nfsv4/abel_share` was created earlier on localhost and remote host by using:
 
    $ mkdir -p /mnt/nfsv4/abel_share

You can use another folder name.

If NFS is configured correctly on client hosts, the `mount` command shows that you have mounted an NFS share::

    $ /home/wien2k# mount
    sysfs on /sys type sysfs (rw,nosuid,nodev,noexec,relatime)
    proc on /proc type proc (rw,nosuid,nodev,noexec,relatime)
    udev on /dev type devtmpfs (rw,relatime,size=10240k,nr_inodes=2315885,mode=755)
    .....
    10.88.0.251:/ on /mnt/nfsv4/abel_share type nfs4 (rw,relatime,vers=4,rsize=8192,wsize=81
    92,namlen=255,soft,proto=tcp,timeo=600,retrans=2,sec=sys,clientaddr=10.88.0.245,minorver
    sion=0,local_lock=none,addr=10.88.0.251)
    
### 6. Setup configuration file
 Open `cfg/config.py` file and edit needed variables.  
 
### 7. License

**FEFF input files generator** has been created under the **GNU GPLv3 license**