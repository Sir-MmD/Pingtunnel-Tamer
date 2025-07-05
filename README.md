# Pingtunnel-Tamer
A simple script to tame Pingtunnel

## What is this?
As you may know, the Pingtunnel project (https://github.com/esrrhs/pingtunnel) has a serious resource usage issue, which can lead to it being terminated by the OS on virtual machines or even crashing dedicated hosts.

You can use this simple Python script to prevent such issues. The script runs Pingtunnel and automatically kills it when CPU or RAM usage exceeds a certain threshold, then restarts it.

## Install requirement
```bash
sudo apt update && apt install python3-pip -y 
```

```bash
pip install psutil
```

## Define CPU or RAM threshold
Open ```pt.py``` and set the values for ```CPU_THRESHOLD``` and ```RAM_THRESHOLD``` according to your needs.

You can also adjust the ```CHECK_INTERVAL```

## Define pingtunnel arguments
Use ```PINGTUNNEL_CMD``` to set your Pingtunnel arguments

## Run
```bash
python3 pt.py
```

## Recommended Thresholds

### Server:

CPU: 95%

RAM: 13%

### Client:

CPU: 95%

RAM: 95%
