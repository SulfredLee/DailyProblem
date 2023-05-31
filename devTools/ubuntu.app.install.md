## Avidemux --- video editor
[installation guide](https://linux.how2shout.com/install-avidemux-on-ubuntu-22-04-lts-jammy-linux/)
### installation
```bash
$ sudo apt update
$ sudo apt install software-properties-common apt-transport-https
$ sudo add-apt-repository ppa:xtradeb/apps
$ sudo apt update
$ sudo apt install avidemux*
```
### run it
```bash
$ avidemux &

```
### upgrade
```bash
$ sudo apt update && sudo apt upgrade
```
### remove
```bash
$ sudo apt remove avidemux*
$ sudo add-apt-repository -r ppa:xtradeb/apps -y
```
