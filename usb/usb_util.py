'''
USB code to interact with device and get information.

'''

import usb.core
import usb.util
import logging

logger = logging.getLogger(__name__)


def getDevicesInfo():
    ''' Get information of USB connected devices.

    :returns: A list of dictonaries representing device informations

    :raises: DeviceUSBException
    '''
    devices = []

    for device in usb.core.find(find_all=1):
        try:
            device_data = {
                'vendorId': device.idVendor,
                'productId': device.idProduct,
                'bus': device.bus,
                'address': device.address,
                'strings': [],
            }
            # Check for string info in this range
            for n in range(9):
                try:
                    device_data['strings'].append(usb.util.get_string(device,
                                                                      256, n))
                except usb.core.USBError:
                    # Let is pass
                    pass
            devices.append(device_data)
        except usb.core.USBError as error:
            # TODO: Raises USB exception here
            logger.warning(error)
    return devices


def searchBySerial(serialNumber):
    ''' Search for device using serial number.

    :param serialNumber: Device serial number

    :returns: A dictionary representing device informations

    :raises: DeviceNotFount
    '''
    for device in getDevicesInfo():
        if serialNumber in device['strings']:
            # TODO: Raises a device not found exception here
            return device


def searchByProductId(productId):
    ''' Search for device unsing product ID.

    :param productID: Device product ID

    :returns: A dictionary representing device informations

    :raises: DeviceNotFount
    '''
    for device in getDevicesInfo():
        if productId == device['productId']:
            # TODO: Raises a device not found exception here
            return device


def searchByVendorId(vendorId):
    ''' Search for device unsing vendor ID

    :param vendorID: Device vendor ID

    :returns: A dictionary representing device informations

    :raises: DeviceNotFount
    '''
    for device in getDevicesInfo():
        if vendorId == device['vendorId']:
            # TODO: Raises a device not found exception here
            return device
