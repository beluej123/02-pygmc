import logging

from .device import BaseDevice
from .device_rfc1201 import DeviceRFC1201
from .device_rfc1801 import DeviceRFC1801

logger = logging.getLogger("pygmc.device")

device_map = {
    "GMC-280": DeviceRFC1201,
    "GMC-300": DeviceRFC1201,
    "GMC-320": DeviceRFC1201,
    "GMC-500": DeviceRFC1801,
    "GMC-600": DeviceRFC1801,
    # seemed like bigger number would use newer rfc spec until GMC-800
    # listed as RFC1201 in https://www.gqelectronicsllc.com/GMC-800UserGuide.pdf
    "GMC-800": DeviceRFC1201,
}


def auto_get_device(connection):
    """
    Auto get device class

    Parameters
    ----------
    connection

    Returns
    -------

    """
    cmd = b"<GETVER>>"
    connection.reset_buffers()
    result = connection.get(cmd).decode("utf8")
    logger.debug(f"Device={result}")
    base_version = result[0:7]

    if base_version not in device_map:
        logger.warning(f"Unable to auto assign device to Device={result}")
        logger.warning("Assuming newer device. Manually specify device if incorrect.")
        return DeviceRFC1801(connection)

    return device_map[base_version](connection)
