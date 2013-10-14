'''
VirtualBox

'''

import uuid
import time

from fish import ProgressFish
from vboxapi import VirtualBoxManager

fish = ProgressFish(total=100)
manager = VirtualBoxManager(None, None)
vbox = manager.vbox


def createMachine(name, uuid=None, settings_file=None, groups=[],
                  os_type_id='Debian', flags='', force_overwrite=False):
    ''' Create virtual machine

    Version 4.1.18:

    :param settingsFile: Fully qualified path where the settings file should
                         be created, or NULL for a default folder and file
                         based on the name argument.
    :param name: Machine name.
    :param osTypeId: Guest OS Type ID.
    :param id: Machine UUID (optional).
    :param forceOverwrite: If true, an existing machine settings file will be
                           overwritten.
    :returns: IProgress
    '''
    machine = None
    try:
        machine = vbox.createMachine(settings_file, name, groups, os_type_id,
                                     flags)
    except TypeError:
        machine = vbox.createMachine(settings_file, name, os_type_id, uuid,
                                     force_overwrite)
    return machine


def cloneMachine(fromMachine, toMachine, mode, options):
    ''' Clone a virtual machine.

    :param mode: Clone mode use 1 to to create a full clone and 0 to create a
                 linked one.
    :param options: Options for a cloning operation safe to use a empty list.

    :raises: E_INVALIDARG: target is null.

    :returns: IProgress.
    '''
    progress = fromMachine.cloneTo(toMachine, mode, options)
    return progress


def machines():
    return manager.getArray(vbox, 'machines')


def searchMachine(machine):
    return vbox.findMachine(machine)


def searchUSBBySerial(serial):
    usb_devices = manager.getArray(vbox.host, 'USBDevices')
    for usb in usb_devices:
        if usb.serialNumber == serial:
            return usb.id


def launchMachine(machine):
    session = manager.mgr.getSessionObject(vbox)
    progress = machine.launchVMProcess(session, 'gui', '')
    return (progress, session)


def attachUSBBySerial(machine, serial):
    session = manager.mgr.getSessionObject(vbox)
    machine.lockMachine(session, 1)
    console = session.console
    usb_uuid = searchUSBBySerial(serial)
    console.attachUSBDevice(usb_uuid)
    manager.closeMachineSession(session)


def machineIpAddress(machine):
    return machine.getGuestProperty('/VirtualBox/GuestInfo/Net/0/V4/IP')[0]

if __name__ == '__main__':
    machine_uuid = str(uuid.uuid4())
    flags = 'UUID={0}'.format(machine_uuid)
    #machine = createMachine(None, machine_uuid, [], 'Debian', flags)
    machine = createMachine(machine_uuid, uuid=machine_uuid,
                            settings_file=None, groups=[], os_type_id='Debian',
                            flags=flags, force_overwrite=False)
    fromMachine = searchMachine('987ae866-a4c0-4723-896e-8897fe17f3f0')
    progress = cloneMachine(fromMachine, machine, 1, [])
    while progress.operationPercent < 100:
        fish.animate(amount=progress.operationPercent)
    vbox.registerMachine(machine)
    progress, session = launchMachine(machine)
    while progress.operationPercent < 100:
        fish.animate(amount=progress.operationPercent)
    manager.closeMachineSession(session)
    time.sleep(60)
    attachUSBBySerial(machine, '8A000080Q')
    print machineIpAddress(machine)
