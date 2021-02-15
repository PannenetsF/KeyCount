import argparse
import asyncio, evdev
import json
import time 

parser = argparse.ArgumentParser("keycount")
parser.add_argument('--devices', type=str, default='3', help='target devices event numbers, devided by \'-\'')
parser.add_argument('--file', type=str, default='./file.json', help='data file')
args = parser.parse_args()

KEYINPUT = 1 
KEYUP = 0 
KEYDOWN = 1

def load_keys(args):
    try:
        key_dir = open(args.file, 'r')
    except:
        key_dir = open(args.file, 'w')
        dic = {} 
        for i in range(240):
            dic[str(i)] = 0
        key_dir.write(json.dumps(dic))
        key_dir.close()
        key_dir = open(args.file, 'r')
    key_dict = key_dir.read()
    key_dir.close()
    key_dict = json.loads(key_dict)
    return key_dict


def save_keys(key_dict, args):
    key_json = json.dumps(key_dict)
    key_dir = open(args.file, 'w')
    key_dir.write(key_json)
    key_dir.close()

def check_time(start, end, args):
    if end - start > args.time:
        return True
    else:
        return False

async def save_event(device):
    async for event in device.async_read_loop():
        if event.type == KEYINPUT and event.value == KEYUP:
            global key_dict
            key_dict[str(event.code)] += 1
            save_keys(key_dict, args)
            print(event.code, key_dict[str(event.code)], sep=':')

if __name__ == '__main__':
    devices = ['/dev/input/event'+i for i in args.devices.rsplit('-')]
    devices = [evdev.InputDevice(dev) for dev in devices]
    key_dict = load_keys(args)
    for dev in devices:
        asyncio.ensure_future(save_event(dev))
    loop = asyncio.get_event_loop()
    loop.run_forever()