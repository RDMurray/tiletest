from collections import Counter
import json
import bz2

fn = '32150/22011.json.bz2'

j=json.load(bz2.open(fn, 'rt'))

features = j['features']
types = [item['feature_type'] for item in features]

counts =Counter(types)
print(counts)
