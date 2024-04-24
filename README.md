# chasing-ghg

## Accessing the ECCC Remote Server

We currently have a system running the model on the government servers. To access the servers, you need an SSC HPC account, for which you must fill out an account request form. After a couple days of processing, you should receive a username and password. The username typically takes the form of `abc123` and the password is a long combination of letters.  

While on a government network (VPN or on-location), connect to the servers by typing into a terminal (replacing `abc123`  with your username):
```
ssh abc123@hpcr5-in.science.gc.ca
```
On your first connect, it will tell you that:  *The authenticity of host 'hpcr5-in.science.gc.ca (142.98.0.177)' can't be established.* This is normal, and you should confirm that you wish to connect with `yes`. 

You will then be prompted for a password. Enter the one sent to you in the email with you username and you should be given access. You should now see in your terminal:
```
[abc123@hpcr5-in1 ~]$
```
Now to connect to the specific server, you need to SSH once again:
```
ssh abc123@ppp5.science.gc.ca
```
Once again you may be prompted to confirm whether or not you intend to connect to this host. Type in `yes` and you will have access, this time without asking for your password. You should now see:
```
[abc001@ppp5login-001 ~]$ 
```

Congratulations! You have successfully connected to the server.

### Running Polyphemus

Here are instructions to run an example model with Polyphemus. Copy the directory
`/home/min000/devel/Polyphemus-Example` into your own workspace:
```
cp -r /home/min000/devel/Polyphemus-Example Polyphemus-Example
cd Polyphemus-Example
```
Before running, you’ll need to load the Polyphemus package:
```
. ssmuse-sh -p /fs/ssm/eccc/crd/ccmr/EC-CAS/master/Polyphemus_1.11.1-1
```
This gives access to the pre-compiled “gaussian-deposition” and “plume” executables.

Then to run the example:
```
python Example.py
```
It should put the results into the `results` subdirectory.

### Setting Up a GUI

Download thinlinc from the software centre on your government laptop. As usual, ensure that you are on a government network.

Use the following settings to connect:
- Select advanced mode
- **Server**: `hpcr-vis-u2`
- Username/Password: same as science server credentials
- **Fullscreen Mode: OFF** - this is extremely important as otherwise the window will open in fullscreen without a way to escape, since all system hotkeys are captured by the remote server (alt-tab only switches windows in the remote server).
- Auto-updates: OFF

Upon connecting, you will be prompted a couple times with various messages, just accept them and continue. When asked for a desktop environment, select *gnome* and not *gnome-classic*. 

### Alternative: VSCode Remote SSH

In VSCode you have the option to connect to a remote server through SSH, utilizing the Microsoft SSH remote tunnel extension. 

Open the command palette [`ctrl+shift+p`] and type in: *Remote-SSH: Open SSH Configuration File...* The option should appear once you've typed a few characters. If you are prompted to select between multiple files, choose the local one (generally will have you username in the path). Paste in the following, replacing \<remoteuser\> with your username in the form of abc123, and local user name (appears in the path C:/Users/<localuser>). Note that this configuration assumes you want to connect to the ppp5 through hpcr5 (double ssh).

```
Host ppp5.science.gc.ca
    HostName ppp5.science.gc.ca
    User <remoteuser>
    ProxyJump hpcr5.science.gc.ca
    PreferredAuthentications publickey
    IdentityFile "/Users/<localuser>/.ssh/keys/ppp5.science.gc.ca_rsa"

Host hpcr5.science.gc.ca
    HostName hpcr5-in.science.gc.ca
    User <remoteuser>
    PreferredAuthentications publickey
    IdentityFile "/Users/<localuser>/.ssh/keys/hpcr5-in.science.gc.ca_rsa"
```

Optionally you may omit the `PreferredAuthentications` and `IdentityFile` options if you do not want to create an ssh key. Creating an ssh key pair allows you to login to the remote server without logging in multiple times. 

Generate a public and private key using something like OpenSSL (note these paths are for Windows, adapt them to your platform as necessary)
```
ssh-keygen -q -b 2048 -f C:\Users\<localuser>\.ssh\keys\ppp5.science.gc.ca_rsa -t rsa
ssh-keygen -q -b 2048 -f C:\Users\<localuser>\.ssh\keys\hpcr5-in.science.gc.ca_rsa -t rsa
```
Navigate to the `keys` folder and copy the contents inside both public key files (`.pub`) to the remote server. On the remote server, navigate to the file:
```
<remoteuserhome>/.ssh/authorized_keys
```
If it exists, paste the contents of `hpcr5-in.science.gc.ca_rsa.pub` and `ppp5.science.gc.ca_rsa.pub` to the end of the file (on separate lines).

If it does not exists, you can create one with permissions 600
```
mkdir authorized_keys
chmod 600 authorized_keys
```
Then you can paste in the same contents as above. You should now be able to connect through SSH without needing to type in the password every time. 


### Transferring Files

Using FileZilla (installed through the software centre), you can connect to the server using:
- **Host:** sftp://hpcr5-in
-  Username/Password: same as science server credentials
-  **Port:** 22

### Changing Your Password

Not sure if this is allowed, but you are able to change the password of your science server credentials. 

In a terminal while connected to the server, type in:
```
passwd
```
Follow the prompted instructions to enter your current and new desired passwords.

## Performing Computations

When running more computationally intensive tasks, it is possible to request more resources using the `qsub` command. 

This will create an interactive terminal with 8 cores and 64gb of ram.
```
qsub -I -N interactive -l select=1:ncpus=8:mem=64gb -l walltime=6:0:0
```
The current limit is 80 CPUs and about 182GB of memory for a max 6-hour wallclock time. Make sure to exit the session with `exit` to free the resources once finished.

## Troubleshooting

### Connection Errors

The first thing to check if you are unable to connect to the server is to ensure you are on the government network. You must either be at the office connected through the ethernet cable, or remotely connected through the VPN. 

### No such file or directory: 'Methane.bin'

If you cannot find this file (assuming this isn't an incorrect path in the code), chances are the `plume` or `gaussian-deposition` programs are not running correctly. 
 
## General Notes
- Dataset times are usually recorded in UTC
- Weather data from [climate.weather.gc.ca](climate.weather.gc.ca) can be in UTC or LST. LST does NOT account for daylight saving time (i.e. always gives EST); you need too add an hour for daylight saving time (which we don't need to do).
- Weather from [www.timeanddate.com](www.timeanddate.com/weather) is given in local time, adjusting to EDT (UTC-4) in the summer months, and back to EST (UTC-5) in the winter months. 