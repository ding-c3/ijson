import msgpack

sizes = [1000, 1000000, 10000000, 50000000, 100000000, 500000000] # was running into "OSError: [Errno 22] Invalid argument large file"

for data_len in ["short", "long"]:
    if data_len == "short":
        d = 1.23
    else:
        d = 1.2345678901234567890
    for n in sizes:
        data = [d for _ in range(n)]
        ds = {"data": data, "shape": [n, 1], "axes": ["a", "b"], "sourceDimension": 0}
        import json
        with open('data/ds_{}_{}.json'.format(n, data_len), 'w') as outfile:
            json.dump(ds, outfile)
        with open('data/ds_{}_{}.msgpack'.format(n, data_len), 'wb') as outfile:
            packer = msgpack.Packer()
            packed = packer.pack(ds)
            packed_len = len(packed)
            import math
            step_size = 1000000000
            for i in range(math.ceil(packed_len / step_size)):
                outfile.write(packed[i*step_size:(i + 1) * step_size])
            # msgpack.dump(ds, outfile)