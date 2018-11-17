import ijson.backends.yajl2_cffi as ijson
import json
try:
    import tracemalloc
except:
    pass
import time
import cProfile
import msgpack


def time_it(f):
    start_time = time.time()
    f()
    print("time: %s seconds " % (time.time() - start_time))


def time_breakdown(f):
    profile = cProfile.Profile()
    profile.enable()
    f()
    profile.disable()
    profile.print_stats(sort=1)


def mem_profile(f):
    tracemalloc.start()
    f()
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')
    mem_tuple = tracemalloc.get_traced_memory()
    print("memory: current = {0:.2f} MiB and peak = {1:.2f} MiB".format(mem_tuple[0] / (1024 * 1024) , mem_tuple[1] / (1024 * 1024)))
    print("[ Top 3 ]")
    for stat in top_stats[:3]:
        print(stat)
    tracemalloc.stop()


def get_stdin():
    return sys.stdin.buffer


def do_profile(f, profile):
    if profile == "mem":
        mem_profile(f)
    elif profile == "time_breakdown":
        time_breakdown(f)
    else:
        time_it(f)


def test_simple_ijson(profile):
    ds = []
    def load_json():
        objects = ijson.items(get_stdin(), "")
        ds.append(next(objects))
        # with  open(self.file_name, "rb") as f:
        #     objects = ijson.items(f, "")
        #     # parser = ijson.common.parse(ijson.backends.yajl2_cffi.basic_parse(f, buf_size=1024*1024))
        #     # objects = ijson.common.items(parser, "")
        #     ds.append(next(objects))

    do_profile(load_json, profile)


def test_simple_json(profile):
    ds = []
    def load_json():
        ds.append(json.load(get_stdin()))
        # with  open(self.file_name, "rb") as f:
        #     ds.append(json.load(f))

    do_profile(load_json, profile)


def test_msgpack(profile):
    ds = []
    def load_msgpack():
        # ds.append(msgpack.load(get_stdin()))
        unpacker = msgpack.Unpacker(get_stdin(), raw=False)
        x = next(unpacker)
        ds.append(x)
    do_profile(load_msgpack, profile)


if __name__ == '__main__':
    import sys
    profile = sys.argv[2]
    if sys.argv[1] == "ijson":
        test_simple_ijson(profile)
    elif sys.argv[1] == "msgpack":
        test_msgpack(profile)
    else:
        test_simple_json(profile)