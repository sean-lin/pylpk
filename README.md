pylpk
=====

sshd AuthorizedKeysCommand helper for ldap


Install
-----

Install [python-ldap](http://www.python-ldap.org/)

Ubuntu or Debian
```
sudo apt-get install python-ldap
```

Pip
```
sudo pip install python-ldap
```

Download this project

Setup
-----

#### setup pylpk
Create a config file and put it somewhere. There's a sample *etc/pylpk.ini.sample*.
By default the program would read it at */etc/pylpk.ini* but you can change it by ```-f /your/path```

#### setup sshd
Add AuthorizedKeysCommand to your sshd config file, just like 
```
AuthorizedKeysCommand /your/path/to/pylpk.py
```
You may add AuthorizedKeysCommandUser.

Test
-----
After setup, Run the program to test your config
```
./pylpk.py username
```
If the username is correct and his public key was set, the public key would be printed.

__Enjoy It!__
