# chasing-ghg

## Accessing the ECCC Remote Server

We currently have a system running the model on the government servers. To
access the servers, you need an SSC HPC account, for which you must fill out an
account request form. After a couple days of processing, you should receive a
username and password. The username typically takes the form of `abc123` and the
password is a long combination of letters.  

While on a government network (VPN or on-location), connect to the servers by
typing into a terminal (replacing `abc123`  with your username):
```
ssh abc123@hpcr5-in.science.gc.ca
```
On your first connect, it will tell you that:  *The authenticity of host
'hpcr5-in.science.gc.ca (142.98.0.177)' can't be established.* This is normal,
and you should confirm that you wish to connect with `yes`. 

You will then be prompted for a password. Enter the one sent to you in the email
with you username and you should be given access. You should now see in your
terminal:
```
[abc123@hpcr5-in1 ~]$
```
Now to connect to the specific server, you need to SSH once again:
```
ssh abc123@ppp5.science.gc.ca
```
Once again you may be prompted to confirm whether or not you intend to connect
to this host. Type in `yes` and you will have access, this time without asking
for your password. You should now see:
```
[abc001@ppp5login-001 ~]$ 
```

Congratulations! You have successfully connected to the server.

### Test Run Polyphemus

Here are instructions to run an example model with Polyphemus. Copy the
directory `/home/min000/devel/Polyphemus-Example` into your own workspace:
```
cp -r /home/min000/devel/Polyphemus-Example Polyphemus-Example
cd Polyphemus-Example
```
Before running, you’ll need to load the Polyphemus package:
```
. ssmuse-sh -p /fs/ssm/eccc/crd/ccmr/EC-CAS/master/Polyphemus_1.11.1-1
```
This gives access to the pre-compiled “gaussian-deposition” and “plume”
executables. **Important**: this is something you need to run every time you reconnect to the
remote servers or start an interactive compute session described
[here](#performing-complex-computations). 

Then to run the example:
```
python Example.py
```
It should put the results into the `results` subdirectory.

### Setting Up a GUI

Download thinlinc from the software centre on your government laptop. As usual,
ensure that you are on a government network.

Use the following settings to connect:
- Select advanced mode
- **Server**: `hpcr-vis-u2`
- Username/Password: same as science server credentials
- **Fullscreen Mode: OFF** - this is extremely important as otherwise the window
  will open in fullscreen without a way to escape, since all system hotkeys are
  captured by the remote server (alt-tab only switches windows in the remote
  server).
- Auto-updates: OFF

Upon connecting, you will be prompted a couple times with various messages, just
accept them and continue. When asked for a desktop environment, select *gnome*
and not *gnome-classic*. 

### Alternative GUI: VSCode Remote SSH (Recommended)

In VSCode you have the option to connect to a remote server through SSH,
utilizing the Microsoft SSH remote tunnel extension. 

Open the command palette [`ctrl+shift+p`] and type in: *Remote-SSH: Open SSH
Configuration File...* The option should appear once you've typed a few
characters. If you are prompted to select between multiple files, choose the
local one (generally will have you username in the path). Paste in the
following, replacing `<remoteuser\>` with your username in the form of `abc123`,
and local user name (appears in the path `C:/Users/<localuser>`). Note that this
configuration assumes you want to connect to the ppp5 through hpcr5 (double
ssh).

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

Optionally you may omit the `PreferredAuthentications` and `IdentityFile`
options if you do not want to create an ssh key. Creating an ssh key pair allows
you to login to the remote server without logging in multiple times. 

Generate a public and private key using something like OpenSSL (note these paths
are for Windows, adapt them to your platform as necessary). An empty passphrase
is probably fine, but I'm not an expert on this. You may have to regenerate
these keys every once in a while.
```
ssh-keygen -q -b 2048 -f C:\Users\<localuser>\.ssh\keys\ppp5.science.gc.ca_rsa -t rsa
ssh-keygen -q -b 2048 -f C:\Users\<localuser>\.ssh\keys\hpcr5-in.science.gc.ca_rsa -t rsa
```
Navigate to the `keys` folder and copy the contents inside both public key files
(`.pub`) to the remote server. On the remote server, navigate to the file:
```
<remoteuserhome>/.ssh/authorized_keys
```
If it exists, paste the contents of `hpcr5-in.science.gc.ca_rsa.pub` and
`ppp5.science.gc.ca_rsa.pub` to the end of the file (on separate lines).

If it does not exists, you can create one with permissions 600
```
cd .ssh/
touch authorized_keys
chmod 600 authorized_keys
nano authorized_keys
```
Then you can paste in the same contents as above. You should now be able to
connect through SSH without needing to type in the password every time. 


### Transferring Files

Using FileZilla (installed through the software centre), you can connect to the
server using:
- **Host:** sftp://hpcr5-in
- Username/Password: same as science server credentials
- **Port:** 22

### Changing Your Password

In a terminal while connected to the server, type in:
```
passwd
```
Follow the prompted instructions to enter your current and new desired
passwords. Make sure to write it down or save it somewhere in case you forget. 

### Performing Complex Computations

When running more computationally intensive tasks, it is possible to request
more resources from the server using the `qsub` command. You must be connected
to the interactive node ppp5 for this to work. 

For example, this command will create an interactive terminal with 8 cores and
64gb of ram:
```
qsub -I -N interactive -l select=1:ncpus=8:mem=64gb -l walltime=4:0:0
```
The current limit is 80 CPUs and about 182GB of memory for a max 6-hour
wallclock time. Make sure to exit the session with `exit` to free the resources
once finished.


## Troubleshooting

### Connection Errors

The first thing to check if you are unable to connect to the server is to ensure
you are on the government network. You must either be at the office connected
through the ethernet cable, or remotely connected through the VPN. Note that
there is no WiFi in the office. 

### Issues with SSH

#### Corrupted MAC on input

MAC or message authentication code errors are about the authentication
algorithm. You can try adding `-m` to the ssh command with an acceptable
algorithm. `ssh -m hmac-sha2-512` worked for me. To get a list of available
algorithms, run 

```
ssh -Q mac
```
To make the change permanent in the ssh-config, either follow instructions
[here](#alternative-vscode-remote-ssh), or go into `~/.ssh/config` and add (or
whichever algorithm works for you):
```
MACs hmac-sha2-512
```

#### SSH Failed - ECONNRESET
If using vscode, this can be an issue with the remote host server. Navigate to
the remote server using the terminal or whatever means you have available and
delete the `~/.vscode-server/` folder. Alternatively, you can try to delete only
the `./vscode-server/bin/` folder to preserve settings and app data, but I have
not tested this.

### No such file or directory: 'Methane.bin'

If you cannot find this file (assuming this isn't an incorrect path in the
code), chances are the `plume` or `gaussian-deposition` programs are not running
correctly. These are executables compiled by Polyphemus. 

### /usr/bin/python: can't open file 

Either the file you want to run does not exist, the path is wrong, or you are
not in the correct directory. `cd` into the right place first. 

### No module named... the script doesn't run correctly

You did not import the packages into your shell environment. you need to do this every time you reconnect to the server or start a new session. 
```
. ssmuse-sh -p /fs/ssm/eccc/crd/ccmr/EC-CAS/master/Polyphemus_1.11.1-1
```
 
## General Notes

### Weather Data
- Dataset times are usually recorded in UTC
- Weather data from [climate.weather.gc.ca](climate.weather.gc.ca) can be in UTC
  or LST. LST does NOT account for daylight saving time (i.e. always gives EST);
  you need too add an hour for daylight saving time (which we don't need to do).
- Weather from [www.timeanddate.com](www.timeanddate.com/weather) is given in
  local time, adjusting to EDT (UTC-4) in the summer months, and back to EST
  (UTC-5) in the winter months. 

### A Note on Stability Classes (SC)
- Refer to Pasquill's stability class chart to determine the SC
  - use a combination of the weather condition and wind speed
  - note if overcast, it is always SC D
- There appears to have some unquantified delay between changes in solar
  radiation, and a reflected change in SC. This means that for example, as the
  weather transitions from an overcast storm to a sunny day, the SC may take an
  hour or more to go from a SC of D to SC B. 
- Around sunset and sunrise, things also get a little tricky. It would be
  reasonable to use the daytime SC up to an hour after sunset and nighttime SC
  up to an hour after sunrise as it takes some time for the ground to heat
  up/cool down. The one hour figure is merely an anecdotal estimate with no
  rigorous investigation.
- An alternative method to determine SC involves a calculation on the wind
  direction variability. I have no idea how this works, but its something called
  sigma theta. See
  [this](http://hps.ne.uiuc.edu/numug/archive/2003/presentations/paynter.pdf)
  paper's section on stability class for more details. 