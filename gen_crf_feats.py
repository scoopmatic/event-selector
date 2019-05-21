import json
from collections import Counter

val_path = "../data-processing/selection_val.jsonl"
train_path = "../data-processing/selection_train.jsonl"

val_out = open("crf_val.tsv",'w')
train_out = open("crf_train.tsv",'w')

for path, out in [(val_path, val_out), (train_path, train_out)]:
    seqs = []
    last_game = None
    for line in open(path):
        feats = json.loads(line.strip())
        if last_game != feats['game']:
            try:
                seqs[-1].sort()
            except:
                pass
            seqs.append([])
            last_game = feats['game']
        label = feats['reported']
        seqs[-1].append((int(feats['event_idx'][1:]), feats['input'], label))


    input_seqs = []
    output_seqs = []
    for i, seq in enumerate(seqs):
        seq_input = []
        seq_output = []
        for idx, feats, label in seq:
            features = []
            # Break up sequence of features
            for feat in feats.split(';'):
                key, value = feat.split('=')
                key = key.strip()
                value = value.strip().lower()

                if key in ['player', 'assist', 'team', 'home', 'guest']: # Omit
                    continue #61.65 teams, 64.36 players, 62.98 all, none 65.6
                # Break up features with sequential values
                if key == 'abbrevs':
                    if ',' in value:
                        for pi, part in enumerate(value.split(',')):
                            features.append((part.strip(), 'true'))
                    else:
                        features.append((value.strip(), 'true'))
                elif ',' in value:
                    for pi, part in enumerate(value.split(',')):
                        part = part.replace('-', '\u2013').strip()
                        if '\u2013' in part:
                            for pii, subpart in enumerate(part.split('\u2013')):
                                try:
                                    num = int(''.join([c for c in subpart if c.isdigit()]))
                                    features.append(("%s%d-%d" % (key,pi,pii), num))
                                except ValueError:
                                    features.append((part.strip().split()[-1], key))
                                    break
                        else:
                            if key == 'goaltype':
                                features.append((part.strip(), key))
                            else:
                                features.append((part.strip().split()[-1], key))

                elif '\u2013' in value:
                    part1, part2 = value.split('\u2013')
                    part1 = part1.strip()
                    if part1.isdigit():
                        part1 = int(part1)
                    features.append((key+'1', part1))
                    part2 = part2.strip()
                    if part2.isdigit():
                        part2 = int(part2)
                    features.append((key+'2', part2))
                elif '.' in value and value.split('.')[0].strip().isdigit():
                    part1, part2 = value.split('.')
                    weight = int(part1.strip()) + int("%.2d" % int(part2.strip()))/60
                    features.append((key, weight))
                elif '+' in value:
                    tot = 0
                    for pi, part in enumerate(value.split('+')):
                        features.append((key+str(pi), int(part)))
                        tot += int(part)
                    features.append((key+'_tot', tot))
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        try:
                            value = float(value)
                        except ValueError:
                            pass
                    if key in ['player', 'assist', 'goaltype']:
                        key, value = str(value).split()[-1], key
                    if key == 'minutes':
                        key+="0"
                    features.append((key, value))


            seq_input.append(dict(features))
            seq_output.append(str(label))

        input_seqs.append(seq_input)
        output_seqs.append(seq_output)

    for i, seq in enumerate(input_seqs):
        for j, elem in enumerate(seq):
            print(output_seqs[i][j], end="\t", file=out)
            for key, value in elem.items():
                weight = ""
                if type(value) is int or type(value) is float:
                    weight = ':'+str(value)
                    value = 'true'
                print("%s=%s%s" % (key, value, weight), end="\t", file=out)
            print(file=out)
        print(file=out)

    out.close()
