import os.path, sys, subprocess, argparse
'''
Might have to install argparse if not python 2.7.X or newer. :-( 
Stupid Centos 5 boxen. 
)/  
Y\_/
 /~\

Usage to quickly check for keys using Bash:
[ -f "/root/.ssh/id_rsa.pub" ] && echo "True" ||  echo "False"

Usage to quickly check for keys using Python:
python -c "import os.path; print(os.path.isfile('/root/.ssh/id_rsa.pub'))"

If keys exist might want to use different path or user. Change PRIV_SSH_* as needed.

Usage:
python create_keys.py -uroot -sip/fqdn 

'''
PRIV_SSH_DIR = '/root/.ssh'
PRIV_SSH_FILE = '/root/.ssh/id_rsa.pub'
PLATFORM = sys.platform

def print_pubkey():
    f = open(PRIV_SSH_FILE, 'r')
    pubkey = f.read()
    print(pubkey)

def create_keys():
    '''
    ssh-keygen will also check if keys exist and allow you to type y or no to overwrite.
    :return:
    '''
    subprocess.call('ssh-keygen -t rsa', shell=True)

def check_pubkey():
    if "id_rsa" in os.listdir(PRIV_SSH_DIR):
        return True
    else:
        return False

def push_pubkey(user,host):
    '''
    There is an option to use ssh-copy-id -i which allows use of identity file, however no output is produced.
    '''
    os.chdir(PRIV_SSH_DIR)
    if check_pubkey():
        if PLATFORM == "linux2": # this is most linux systems now days that run in DC's.
            print(PLATFORM)
            if "ssh-copy-id" in os.listdir("/usr/bin/"):
                print("SSH key found. Pushing key to remote server")
                command = "ssh-copy-id %s@%s" % (user, host)
                subprocess.call(command, shell=True)
            else:
                print("ssh-copy-id required for Mac Users. Use --help for more information. Or brew install it.")
    else:
        print("A SSH key is required. Run script again with action set as Gen")


def main():
    parser = argparse.ArgumentParser(description="This script usses ssh-keygen & ssh-copy-id.")
    parser.add_argument("action", choices=["Gen", "Push", "Both"], help="Gen will Generate, Push will Push, Both will Gen and Push, Action to be performed")
    parser.add_argument("-u", "--user", help="SSH username")
    parser.add_argument("-s", "--host", help="IP or FQDN of server")
     args = parser.parse_args()

    if (args.action == "Gen"):
        create_keys()
    elif (args.action == "Push"):
        if args.user and args.host:
            push_key(args.user, args.host)
        else:
            print("-u and -s are required for action Push. Use -h for Help.")
    elif (args.action == "Both"):
        create_keys()
        if args.user and args.host:
            push_pubkey(args.user, args.host)
        else:
            print("-u and -s are required for action Push. Use -h for Help.")
    print_pubkey()


if __name__ == "__main__":
    main()


