from socket import socket, AF_INET, SOCK_DGRAM, IPPROTO_UDP, SOL_SOCKET, SO_REUSEADDR, SO_BROADCAST


def unit_index_from_pos(x, y):
    if x < 0 or x > 13:
        return None

    if 0 <= y < 6:
        return y * 13 + x
    elif y < 8:
        i = 6 * 13

        # The center two strands each have two units removed for the bar on the "left"
        if x < 2:
            return None

        i += (y - 6) * 11 + (x - 2)
        return i
    elif y < 14:
        # Remove the 4 that would be above the bar
        return y * 13 + x - 4


class LightArray:
    """Use UDP broadcasts to communicate with the array"""
    def __init__(self, broadcast_addr='255.255.255.255', port=4210, num_units=180):
        self.broadcast_addr = broadcast_addr
        self.broadcast_port = port
        self.num_units = num_units

        self.broadcast_sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        self.broadcast_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.broadcast_sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        self.unit_brightness = [0] * self.num_units
        self.unit_offset = [0] * self.num_units
        self.unit_volume = [0] * self.num_units

    def send_update(self):
        message = []
        for i in range(self.num_units):
            b = int(self.unit_brightness[i] * 0xffff)
            o = int(self.unit_offset[i])
            v = int(self.unit_volume[i] * 0xffff)

            message += [
                0,  # Mode = direct
                # Brightness
                (b >> 8) & 0xff,
                b & 0xff,
                # Offset
                (o >> 8) & 0xff,
                o & 0xff,
                # Volume
                (v >> 8) & 0xff,
                v & 0xff,
                0,
            ]

        assert(len(message) % 8 == 0)
        self.broadcast_sock.sendto(bytes(message), (self.broadcast_addr, self.broadcast_port))

    def set_brightness(self, unit_idx, brightness):
        if unit_idx < 0 or unit_idx > self.num_units:
            raise Exception('Unit index invalid')

        if brightness < 0 or brightness > 1:
            raise Exception('Brightness must be between 0 and 1')

        self.unit_brightness[unit_idx] = brightness

    def set_volume(self, unit_idx, volume):
        if unit_idx < 0 or unit_idx > self.num_units:
            raise Exception('Unit index invalid')

        if volume < 0 or volume > 1:
            raise Exception('Volume must be between 0 and 1')

        self.unit_volume[unit_idx] = volume
