import sys

test_file = open(sys.argv[1])
train_file = open(sys.argv[2])

test_prompts = {}

for line in test_file.readlines():
    line  = line.strip('\n')
    line  = line.split('\t')[0]
    test_prompts[line] = 0

for line in train_file.readlines():
    line  = line.strip('\n')
    if test_prompts.has_key(line):
        test_prompts[line] += 1

for key in test_prompts.keys():
    if test_prompts[key] > 0:
        print(str(key) + '\t' +  str(test_prompts[key]))
