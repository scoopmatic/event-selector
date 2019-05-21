import numpy as np
import collections
preds = open("crf_val.pred").read().split('\n')

def majority(mx):
    return max(sum(mx[0]),sum(mx[1]))/sum(sum(mx))

def accuracy(mx):
    return (mx[0][0]+mx[1][1])/sum(sum(mx))

def precision(mx):
    return mx[1][1]/(mx[0][1]+mx[1][1])

def recall(mx):
    return mx[1][1]/(mx[1][0]+mx[1][1])

def f1(mx):
    return 2*(precision(mx)*recall(mx))/(precision(mx)+recall(mx))


confmx = collections.defaultdict(lambda: np.zeros((2,2)))
for i, line in enumerate(open("crf_val.tsv")):
    line = line.strip()
    if not line:
        labels.append('')
        continue
    fields = line.split('\t')
    label = fields[0]
    labels.append(label)
    evtype = [f for f in fields[1:] if f.startswith('type=')][0]
    confmx[evtype][int(label)][int(preds[i])] += 1

totmx = np.zeros((2,2))
for evtype in sorted(confmx):
    print(evtype.split('=')[-1])
    print("   prior:  %.1f%%" % (100*majority(confmx[evtype])))
    print("   acc:    %.1f%%" % (100*accuracy(confmx[evtype])))
    print("   prec:   %.1f%%" % (100*precision(confmx[evtype])))
    print("   recall: %.1f%%" % (100*recall(confmx[evtype])))
    print("   f1:     %.1f%%" % (100*f1(confmx[evtype])))
    print()
    totmx += confmx[evtype]

print("Overall")
print("   prior:  %.1f%%" % (100*majority(totmx)))
print("   acc:    %.1f%%" % (100*accuracy(totmx)))
print("   prec:   %.1f%%" % (100*precision(totmx)))
print("   recall: %.1f%%" % (100*recall(totmx)))
print("   f1:     %.1f%%" % (100*f1(totmx)))
