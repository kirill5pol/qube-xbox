# Setup instructions for Paralells or VirtualBox
Install Ubuntu 18.04 or 19.10 from https://ubuntu.com/download/desktop your virtual machine (VM).


## USB connection
Once installed make sure that all USB drivers are working for VM.
- In Paralells this should work out of the box, when a pop-up come up, simply connect to the Paralells VM rather than to your machine
- In VirtualBox:
    + in the main window select the distribution (don't click start)
    + Click on 'Settings' (top bar)
    + Select the 'Ports' tab, then select the 'USB' sub-tab
    + Enable USB Controller and select 'USB 3.0 (xHCI) Controller'
    + Plug in (to your mac) the Quanser Qube and have it turned on
    + Once you click on the USB icon with a green plus sign, the Quanser should show up, click on that and you should be done


## Software installation
Boot up the VM, plug in the Qube to both a power outlet and the VM, then run the following commands in the terminal:

```bash
sudo apt install git
sudo apt install python3-pip
cd ~
mkdir code
cd code
git clone https://github.com/quanser/hil_sdk_linux_x86_64.git
sudo chmod a+x ./hil_sdk_linux_x86_64/setup_hil_sdk ./hil_sdk_linux_x86_64/uninstall_hil_sdk
sudo ./hil_sdk_linux_x86_64/setup_hil_sdk
git clone https://github.com/BlueRiverTech/quanser-openai-driver.git
cd quanser-openai-driver
pip3 install -e .
python tests/test.py --env QubeSwingupEnv --control flip
```

The Qube should now use a classical controller to flip itself upright.


## Xbox Controller
Note: this is currently only supported with a wired Xbox controller and only on Paralells.

Plug in the Xbox controller and run the following commands in terminal:

```bash
cd ~
cd code
git clone https://github.com/kirill5pol/qube-xbox.git
cd qube-xbox
python3 demo-conference.py
```

#### Warning
After pressing one of the `ABXY` buttons, the Qube should switch to a certain mode. The Qube should light up in the same color as the button that was pressed. If this is not the case try to restart/re-plugin any of the following: Qube, Xbox controller, the virtual machine, your computer.

