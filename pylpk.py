#!/usr/bin/env python
import os,sys
import optparse
import ConfigParser

import ldap

_CONFIG_SECTION = 'LDAP'

def get_option():
    usage = "usage: %prog [options] user"
    parser = optparse.OptionParser(usage = usage)
    parser.add_option('-f', '--config', dest='config',
            help = 'config filename', metavar='FILE', default='/etc/pylpk.ini')
    opt, args = parser.parse_args()
    if len(args) != 1:
        parser.print_help()
        sys.exit(-1)
    return opt, args[0]

def load_config(filename):
    config = ConfigParser.ConfigParser()
    config.read(filename)
    
    if not config.has_section(_CONFIG_SECTION):
        sys.stderr.write("Section %s has not been found in config %s\n" % (_CONFIG_SECTION, filename))
        sys.exit(-1)
  
    out = {}
    out['port'] = int(config.get(_CONFIG_SECTION, 'port', False, {_CONFIG_SECTION: {'port': 389}}))

    for i in ['host', 'base', 'ssh_public_key', 'auth_passwd', 'auth_user']:
        if config.has_option(_CONFIG_SECTION, i):
            out[i] = config.get(_CONFIG_SECTION, i, True)
    
    for i in ['host', 'base', 'ssh_public_key']:
        if i not in out:
            sys.stderr.write("Option %s has not been found in config %s\n" % (i, filename))
            sys.exit(-1)
    
    return out

_FILTER_TEMPLATE = 'cn=%s' 
def get_public_key(cfg, user_name):
    try: 
        ldap_conn = ldap.open(cfg['host'])
    except ldap.LDAPError, error_message:
        sys.stderr.write("LDAP Connect Fail: %s\n" % error_message)
        return

    if 'auth_user' in cfg:
        ldap_conn.simple_bind_s(cfg['auth_user'], cfg['auth_passwd'])
    
    search_filter = _FILTER_TEMPLATE % user_name
    query_set = ldap_conn.search_s(
        cfg['base'], 
        ldap.SCOPE_SUBTREE,
        search_filter,
        [cfg['ssh_public_key']] 
        )
    try:
        dn, entry = query_set[0]
        return entry[cfg['ssh_public_key']][0]
    except (IndexError, KeyError):
        pass

def main():
    opt, user_name = get_option()
    config = load_config(opt.config)

    pk = get_public_key(config, user_name)
    if pk:
        print pk
    
if __name__ == '__main__':
    main()
