import platform


class PlatformInfo:
    @classmethod
    def read(cls):
        freedesktop_info = platform.freedesktop_os_release()
        return {
            'system': platform.system(),
            'processor': platform.processor(),
            'platform': platform.platform(),
            'machine': platform.machine(),
            'release': platform.release(),
            'pretty_name': freedesktop_info['PRETTY_NAME'],
            # 'version': platform.version(),
        }
