## How to build image
### If you have additional packages --- build emacs by yourself
1. First round
  1. Build to target round1
  1. Start the container and set up the spacemacs with the normal steps. git clone the .emacs.d, then install all packages
  1. copy the /home/sulfred/.emacs.d, .spacemacs, .spacemacs.env to the work directory /SoftwareDev_Docker
  1. exit the container and remove it

```bash
# outside container
$ ./start_dev_env.sh
# inside container
$ git clone https://github.com/syl20bnr/spacemacs $HOME/.emacs.d
$ emacs --insecure
$ cp $HOME/.emacs.d /SoftwareDev_Docker
# outside container
$ mv .emacs.d .spacemacs .spacemacs.env ../additional_scripts
```

1. Second round
  1. Build to target round2
  1. DONE

### Normal build
1. update the BuildImage.sh
1. build it
1. DONE

## How to upload to docker hub
```bash
$ echo "$PASSWORD" | docker login --username <username> --password-stdin docker.io
$ docker push sulfredlee/sf_dev_ubuntu:2.0
```
