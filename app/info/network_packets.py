

class NetworkPacketsInfo:
    @property
    def data(self):
        if self._data is None:
            self._data = self.read_data()
        return self._data

    @property
    def total_recevied_bytes(self):
        if self._total_received_bytes is None:
            self._total_received_bytes = 0
            for face in self.data:
                self._total_received_bytes += self.data[face]['recv_bytes']
        return self._total_received_bytes

    @property
    def total_transmitted_bytes(self):
        if self._total_transmitted_bytes is None:
            self._total_transmitted_bytes = 0
            for face in self.data:
                self._total_transmitted_bytes += self.data[face]['trans_bytes']
        return self._total_transmitted_bytes

    def __init__(self):
        self._data = None
        self._total_received_bytes = None
        self._total_transmitted_bytes = None

    def read_data(self):
        with open("/proc/net/dev", "r") as fp:
            lines = fp.readlines()

        columnLine = lines[1]
        _, receiveCols, transmitCols = columnLine.split("|")

        receiveCols = ["recv_" + a for a in receiveCols.split()]
        transmitCols = ["trans_" + a for a in transmitCols.split()]
        cols = receiveCols + transmitCols

        faces = {}
        for line in lines[2:]:
            if line.find(":") < 0:
                continue
            face, data = line.split(":")
            face = face.strip()
            faceData = dict(zip(cols, [int(e) for e in data.split()]))
            faces[face] = faceData

        return faces
