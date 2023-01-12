# analytics-setup
setup for analytics server for dashboard logging - to be deleted once contents copied into David's analytics repo

## Adding another public key

1. [get public key from private key info](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/describe-keys.html#retrieving-the-public-key)

```
ssh-keygen -y -f /path_to_key_pair/my-key-pair.pem
```

2. Log into server using amazon dashboard (or directly if have existing auithorized pem on hand)

```
nano .ssh/authorized_keys ##add public key on new line
```

Add a space and the name of the public key e.g.

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQClKsfkNkuSevGj3eYhCe53pcjqP3maAhDFcvBS7O6V
hz2ItxCih+PnDSUaw+WNQn/mZphTk/a/gU8jEzoOWbkM4yxyb/wB96xbiFveSFJuOp/d6RJhJOI0iBXr
lsLnBItntckiJ7FbtxJMXLvvwJryDUilBMTjYtwB+QhYXUMOzce5Pjz5/i8SeJtjnV3iAoG/cQk+0FzZ
qaeJAAHco+CY/5WrUBkrHmFJr6HcXkvJdWPkYQS3xqC0+FmUZofz221CBt5IMucxXPkX4rWi+z7wB3Rb
BQoQzd8v7yeb7OzlPnWOyN0qFU0XA246RA8QFYiCNYwI3f05p6KLxEXAMPLE example-key
```

## Setting up the session host

### install golang

```
$ cd ~/sources/go
$ wget https://go.dev/dl/go1.19.5.linux-amd64.tar.gz
$ which go #check if already installed
$ sudo rm -rf /usr/local/go && tar -C /usr/local -xzf go1.19.5.linux-amd64.tar.gz #if a version is installed, remove it, and then install
$ cp /etc/profile ~/etc.profile.old #safety copy!
$ sudo /etc/profile #add line at end: export PATH=$PATH:/usr/local/go/bin
$ diff ~/etc/profile.old /etc/profile #check change is ok
$ source /etc/profile #make change take effect in current session (this might remove syntax highlighting)
$ echo $PATH #check path updated 
$ rm ~/etc.profile.old #we don't need this anymore (assuming you are confident previous edits were ok)
$ go version #verify installation successful
go version go1.19.5 linux/amd64
```

### clone repo

```
$ cd ~/sources
$ git clone https://github.com/practable/relay.git
$ cd relay
$ go mod tidy
$ cd cmd/session
$ go build
$ sudo cp session /usr/local/bin
$ which session 
/usr/local/bin/session
```

Now let's get some files from the [spinner-amax](https://github.com/practable/spinner-amax) repo, that we use for setting up session host on the experiments as systemd services.

We need:

#### session.service (to go in `/etc/systemd/system`)

```
[Unit]
Description=session host streaming service
After=network.target
[Service]
Restart=on-failure
ExecStart=/usr/local/bin/session-relay host

[Install]
WantedBy=multi-user.target session-rules.service
```

#### session-rules.service (to go in `/etc/systemd/system`)
```
[Unit]
Description=apply session host streaming rules
After=network.target session.service
Wants=session.service
PartOf=session.service

[Service]
Type=oneshot
ExecStartPre=/bin/sleep 10
ExecStart=/usr/local/bin/session-rules

[Install]
WantedBy=multi-user.target
```

#### session-rules (to go in /usr/local/bin)
This is the version for a spinner, with two streams (the logging streams are not connected to the hardware). We will modify this to have streams for each spinner's logging stream, since we are only interested in collecting analytics from the logging streams and not the video and data streams.
```
#!/bin/sh
videoTokenFile="/etc/practable/video.token"
videoAccessFile="/etc/practable/video.access"
dataTokenFile="/etc/practable/data.token"
dataAccessFile="/etc/practable/data.access"

videoToken=$(cat "$videoTokenFile")
videoAccess=$(cat "$videoAccessFile")
dataToken=$(cat "$dataTokenFile")
dataAccess=$(cat "$dataAccessFile")

curl -X POST -H "Content-Type: application/json" -d '{"stream":"video","destination":"'"${videoAccess}"'","id":"0","token":"'"${videoToken}"'"}' http://localhost:8888/api/destinations
curl -X POST -H "Content-Type: application/json" -d '{"stream":"data","destination":"'"${dataAccess}"'","id":"1","token":"'"${dataToken}"'"}' http://localhost:8888/api/destinations 
```



### Procedure for systemd setup of session

```
sudo su
cd /etc/systemd/system
nano session.service #copy in contents above
systemctl enable session
systemctl start session

```

### Producedure for systemd setup of session-rules

#### Write session-rules script 

We need a connection for every spinner in the range spin30-spin41
```
#!/bin/sh
spin30AccessFile="/etc/practable/spin30.access"
spin31AccessFile="/etc/practable/spin31.access"
spin32AccessFile="/etc/practable/spin32.access"
spin33AccessFile="/etc/practable/spin33.access"
spin34AccessFile="/etc/practable/spin34.access"
spin35AccessFile="/etc/practable/spin35.access"
spin36AccessFile="/etc/practable/spin36.access"
spin37AccessFile="/etc/practable/spin37.access"
spin38AccessFile="/etc/practable/spin38.access"
spin39AccessFile="/etc/practable/spin39.access"
spin40AccessFile="/etc/practable/spin40.access"
spin41AccessFile="/etc/practable/spin41.access"

spin30TokenFile="/etc/practable/spin30.token"
spin31TokenFile="/etc/practable/spin31.token"
spin32TokenFile="/etc/practable/spin32.token"
spin33TokenFile="/etc/practable/spin33.token"
spin34TokenFile="/etc/practable/spin34.token"
spin35TokenFile="/etc/practable/spin35.token"
spin36TokenFile="/etc/practable/spin36.token"
spin37TokenFile="/etc/practable/spin37.token"
spin38TokenFile="/etc/practable/spin38.token"
spin39TokenFile="/etc/practable/spin39.token"
spin40TokenFile="/etc/practable/spin40.token"
spin41TokenFile="/etc/practable/spin41.token"

spin30Access=$(cat "$spin30AccessFile")
spin31Access=$(cat "$spin31AccessFile")
spin32Access=$(cat "$spin32AccessFile")
spin33Access=$(cat "$spin33AccessFile")
spin34Access=$(cat "$spin34AccessFile")
spin35Access=$(cat "$spin35AccessFile")
spin36Access=$(cat "$spin36AccessFile")
spin37Access=$(cat "$spin37AccessFile")
spin38Access=$(cat "$spin38AccessFile")
spin39Access=$(cat "$spin39AccessFile")
spin40Access=$(cat "$spin40AccessFile")
spin41Access=$(cat "$spin41AccessFile")

spin30Token=$(cat "$spin30TokenFile")
spin31Token=$(cat "$spin31TokenFile")
spin32Token=$(cat "$spin32TokenFile")
spin33Token=$(cat "$spin33TokenFile")
spin34Token=$(cat "$spin34TokenFile")
spin35Token=$(cat "$spin35TokenFile")
spin36Token=$(cat "$spin36TokenFile")
spin37Token=$(cat "$spin37TokenFile")
spin38Token=$(cat "$spin38TokenFile")
spin39Token=$(cat "$spin39TokenFile")
spin40Token=$(cat "$spin40TokenFile")
spin41Token=$(cat "$spin41TokenFile")


curl -X POST -H "Content-Type: application/json" -d '{"stream":"spin30","destination":"'"${spin30Access}"'","id":"0","token":"'"${spin30Token}"'"}' http://localhost:8888/api/destinations
curl -X POST -H "Content-Type: application/json" -d '{"stream":"spin31","destination":"'"${spin31Access}"'","id":"0","token":"'"${spin31Token}"'"}' http://localhost:8888/api/destinations
curl -X POST -H "Content-Type: application/json" -d '{"stream":"spin32","destination":"'"${spin32Access}"'","id":"0","token":"'"${spin32Token}"'"}' http://localhost:8888/api/destinations
curl -X POST -H "Content-Type: application/json" -d '{"stream":"spin33","destination":"'"${spin33Access}"'","id":"0","token":"'"${spin33Token}"'"}' http://localhost:8888/api/destinations
curl -X POST -H "Content-Type: application/json" -d '{"stream":"spin34","destination":"'"${spin34Access}"'","id":"0","token":"'"${spin34Token}"'"}' http://localhost:8888/api/destinations
curl -X POST -H "Content-Type: application/json" -d '{"stream":"spin35","destination":"'"${spin35Access}"'","id":"0","token":"'"${spin35Token}"'"}' http://localhost:8888/api/destinations
curl -X POST -H "Content-Type: application/json" -d '{"stream":"spin36","destination":"'"${spin36Access}"'","id":"0","token":"'"${spin36Token}"'"}' http://localhost:8888/api/destinations
curl -X POST -H "Content-Type: application/json" -d '{"stream":"spin37","destination":"'"${spin37Access}"'","id":"0","token":"'"${spin37Token}"'"}' http://localhost:8888/api/destinations
curl -X POST -H "Content-Type: application/json" -d '{"stream":"spin38","destination":"'"${spin38Access}"'","id":"0","token":"'"${spin38Token}"'"}' http://localhost:8888/api/destinations
curl -X POST -H "Content-Type: application/json" -d '{"stream":"spin39","destination":"'"${spin39Access}"'","id":"0","token":"'"${spin39Token}"'"}' http://localhost:8888/api/destinations
curl -X POST -H "Content-Type: application/json" -d '{"stream":"spin40","destination":"'"${spin40Access}"'","id":"0","token":"'"${spin40Token}"'"}' http://localhost:8888/api/destinations
curl -X POST -H "Content-Type: application/json" -d '{"stream":"spin41","destination":"'"${spin41Access}"'","id":"0","token":"'"${spin41Token}"'"}' http://localhost:8888/api/destinations
```

```
nano /usr/local/bin/session-rules #copy in above contents
chmod +x /usr/local/bin/session-rules #make executable
```

#### Generate tokens we need 

go to our admin machine and the clone of [spinner-amax](https://github.com/practable/spinner-amax) and copy the configure scripts in `sbc/scripts` - we will need to edit them to create logging tokens....




#### Enable service

```
nano session-rules.service #copy in contents above
systemctl enable session-rules
systemctl start session-rules
```
