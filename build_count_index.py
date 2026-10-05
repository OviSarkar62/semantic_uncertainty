import glob, json, os, sys
import numpy as np
import pandas as pd

MODEL = sys.argv[1]
STAT_DIR, OUT = 'cluster_stats', 'analysis_out'
KS = [10, 20, 30, 40, 50]
os.makedirs(OUT, exist_ok=True)

def to_index(sizes, K):
    v = np.zeros(K, dtype=int)
    for s in sizes:
        v[K - s] += 1
    return v

def to_sizes(v, K):
    return np.array([K - i for i, c in enumerate(v) for _ in range(int(c))])

STATS = ['num_clusters', 'count_min', 'count_max', 'count_mean', 'count_std',
         'lik_min', 'lik_max', 'lik_mean', 'lik_std', 'discrete_entropy', 'semantic_entropy']
summary = []
for path in sorted(glob.glob(f'{STAT_DIR}/{MODEL}_*.json')):
    ds = os.path.basename(path)[len(MODEL) + 1:-5]
    data = json.load(open(path))
    for K in KS:
        rows = []
        for q, r in enumerate(data, start=1):
            b = r['by_n'].get(str(K))
            if b is None:
                continue
            v = to_index(b['cluster_sizes'], K)
            sizes = to_sizes(v, K)
            assert sizes.sum() == K and len(sizes) == b['num_clusters']
            p = sizes / K
            row = {'question': q, 'id': r['id'], 'is_correct': int(r['is_correct'] > 0.5),
                   'num_clusters': len(sizes)}
            for i, c in enumerate(v):
                row[str(K - i)] = int(c)
            row.update({'count_min': p.min(), 'count_max': p.max(),
                        'count_mean': p.mean(), 'count_std': p.std(),
                        'lik_min': b['lik']['min'], 'lik_max': b['lik']['max'],
                        'lik_mean': b['lik']['mean'], 'lik_std': b['lik']['std'],
                        'discrete_entropy': b['discrete_entropy'],
                        'semantic_entropy': b['semantic_entropy']})
            rows.append(row)
        df = pd.DataFrame(rows)
        df.to_csv(f'{OUT}/count_index_{MODEL}_{ds}_K{K}.csv', index=False)
        for grp, sub in [('all', df), ('correct', df[df.is_correct == 1]), ('wrong', df[df.is_correct == 0])]:
            if len(sub):
                summary.append({'dataset': ds, 'group': grp, 'K': K, 'questions': len(sub),
                                **sub[STATS].mean().to_dict()})
pd.DataFrame(summary).to_csv(f'{OUT}/count_index_summary_by_K_{MODEL}.csv', index=False)

cols = ['question', 'is_correct', 'num_clusters'] + [str(k) for k in range(10, 0, -1)]
print(pd.read_csv(f'{OUT}/count_index_{MODEL}_trivia_qa_K10.csv')[cols].head(8).to_string(index=False))
print('saved tables for', MODEL)
