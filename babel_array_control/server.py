import json
from lights import LightArray
from behavior import BabelBehavior


class ArrayServerException(Exception):
    pass


class ArrayServer:
    def __init__(self):
        self.light_array = LightArray()

        self.direct_mode = False

        # Pass ourselves in so the behavior controller can call the server to update the array
        self.behavior_babel = BabelBehavior(self)
        self.behavior_babel.start()

    def handle_behavior_request(self, request):
        if not self.direct_mode:
            return self.handle_request(request)

    def handle_request(self, request):
        try:
            request = json.loads(request)
        except json.JSONDecodeError:
            raise ArrayServerException('Failed to parse JSON')

        if request is not None and 'command' in request:
            command = request['command']

            if command == 'on':
                self.direct_mode = False
            elif command == 'off':
                self.direct_mode = True

                for i in range(180):
                    self.light_array.set_brightness(i, 0)
                for i in range(180):
                    self.light_array.set_volume(i, 0)

                self.light_array.send_update()
            elif command == 'is_on':
                return not self.direct_mode
            elif command == 'getConnectedLights':
                # TODO
                return []
            elif command == 'setMode':
                mode = request['mode']

                if mode == 'direct':
                    self.direct_mode = True
                elif mode == 'babel':
                    self.direct_mode = False
                else:
                    raise ArrayServerException('Unrecognized mode')
            elif command == 'blit':
                if 'brightness' not in request:
                    raise ArrayServerException('Array of brightness values between 0 and 1 required')

                if 'volume' not in request:
                    raise ArrayServerException('Array of volume values between 0 and 1 required')

                try:
                    for i, v in enumerate(request['brightness']):
                        self.light_array.set_brightness(i, v)
                    for i, v in enumerate(request['volume']):
                        self.light_array.set_volume(i, v)

                    self.light_array.send_update()
                except Exception as e:
                    print(e)
                    raise ArrayServerException(str(e))
            else:
                raise ArrayServerException('Unrecognized command')
        else:
            raise ArrayServerException('Failed to parse JSON')
