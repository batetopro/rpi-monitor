import platform


class PlatformInfo:
    @classmethod
    def read_serial(cls):
        cpuserial = "0000000000000000"

        try:
            with open('/proc/cpuinfo', 'r') as fp:
                for line in fp.readlines():
                    if line.startswith('Serial'):
                        cpuserial = line[10:26]
        except Exception:
            cpuserial = "ERROR000000000"

        return cpuserial

    @classmethod
    def read(cls):
        freedesktop_info = platform.freedesktop_os_release()
        return {
            'serial_number': cls.read_serial(),
            'system': platform.system(),
            'processor': platform.processor(),
            'platform': platform.platform(),
            'machine': platform.machine(),
            'release': platform.release(),
            'pretty_name': freedesktop_info['PRETTY_NAME'],
            # 'version': platform.version(),
        }
