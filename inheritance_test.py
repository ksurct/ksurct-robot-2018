
class OutputComponent(object):
    
    def update(data_dict):
        raise NotImplementedError()
    
class I2CComponent(object):
    
    def __init__(self, i2c_address, i2c_channel):
        self.i2c_address = i2c_address
        self.i2c_channel = i2c_channel
        super().__init__()

class MotorComponent(I2CComponent, OutputComponent):
    
    def __init__(self, i2c_address, i2c_channel, another):
        super().__init__(i2c_address, i2c_channel)
        self.another = another
        print("MotorComponent init")


MotorComponent(0x40, 0, 15)

exit()
########################################################

import asyncio
import time

async def print_time(name, interval):
    last_time = time.time()
    for x in range(10):
        await asyncio.sleep(interval)
        print(name, time.time() - last_time, '\t', time.time())
        last_time = time.time()

async def write_to_a_file_a_bunch(filename, number):
    for x in range(number):
        print('\t ', x, " ", filename)
        await asyncio.sleep(0)
        with open(filename, 'w') as f:
            for x in range(1000000):
                f.write(str(x) + "\n")    
    return True

async def my_coro_1():
    print("starting my_coro_1")
    await asyncio.sleep(1)

    tasks = [
        asyncio.ensure_future(write_to_a_file_a_bunch('file1.log', 100)),
        asyncio.ensure_future(write_to_a_file_a_bunch('file2.log', 100)),
        asyncio.ensure_future(write_to_a_file_a_bunch('file3.log', 100)),
        asyncio.ensure_future(print_time("Timer A", 1)),
        asyncio.ensure_future(print_time("Timer B", 5)),
        # asyncio.ensure_future(print_time("Timer C", 10)),
        # asyncio.ensure_future(print_time("Timer D", 20)),
    ]

    await asyncio.wait(tasks)

def main():
    print("starting main")
    loop = asyncio.get_event_loop()
    
    loop.run_until_complete(my_coro_1())

    loop.close()

if __name__ == '__main__':
    main()
