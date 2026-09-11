"""Validation structurelle R7 Q8_0, stdlib, sans mmap/poids/GPU/réseau.

Code 0: tous valides; code 1: au moins un échec. Ne certifie pas les octets
par hash ni la qualité numérique. Lit au maximum 16 Mio de métadonnées.
"""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import struct

CACHE = Path.home() / 'Library/Caches/popsim-modeles'
SCALARS = {0:'B', 1:'b', 2:'H', 3:'h', 4:'I', 5:'i', 6:'f', 7:'?', 10:'Q', 11:'q', 12:'d'}


class Reader:
    def __init__(self, stream):
        self.f = stream

    def read(self, n):
        if n < 0 or self.f.tell() + n > 16 * 1024**2:
            raise ValueError('métadonnées hors budget 16 Mio')
        b = self.f.read(n)
        if len(b) != n:
            raise ValueError('en-tête tronqué')
        return b

    def unpack(self, fmt):
        return struct.unpack('<' + fmt, self.read(struct.calcsize('<' + fmt)))[0]

    def string(self):
        return self.read(self.unpack('Q')).decode('utf-8')

    def value(self, kind, depth=0):
        if kind in SCALARS:
            return self.unpack(SCALARS[kind])
        if kind == 8:
            return self.string()
        if kind == 9 and depth == 0:
            sub, n = self.unpack('I'), self.unpack('Q')
            if n > 200000:
                raise ValueError('tableau trop grand')
            # Ne conserve pas le vocabulaire; petites tables conservées.
            vals = [] if n <= 64 else None
            for _ in range(n):
                v = self.value(sub, depth + 1)
                if vals is not None:
                    vals.append(v)
            return vals if vals is not None else {'count': n}
        raise ValueError(f'type de métadonnée refusé: {kind}')


def inspect(path):
    path = Path(path)
    size = path.stat().st_size
    with path.open('rb') as f:
        r = Reader(f)
        if r.read(4) != b'GGUF' or r.unpack('I') != 3:
            raise ValueError('GGUF v3 little-endian requis')
        count, kv = r.unpack('Q'), r.unpack('Q')
        if count != 355:
            raise ValueError(f'{count} tenseurs, attendu 355')
        if not 1 <= kv <= 256:
            raise ValueError('nombre de métadonnées invalide')
        meta = {}
        for _ in range(kv):
            key = r.string()
            if key in meta:
                raise ValueError('métadonnée dupliquée')
            meta[key] = r.value(r.unpack('I'))
        for key, expected in {'general.architecture':'olmo2', 'general.file_type':7,
                              'olmo2.block_count':32, 'olmo2.embedding_length':4096}.items():
            if meta.get(key) != expected:
                raise ValueError(f'{key}: {meta.get(key)!r}, attendu {expected!r}')
        alignment = meta.get('general.alignment', 32)
        if not isinstance(alignment, int) or alignment < 1 or alignment > 4096 or alignment & (alignment-1):
            raise ValueError('alignement invalide')
        tensors = {}
        ranges = []
        types = Counter()
        for _ in range(count):
            name, nd = r.string(), r.unpack('I')
            if name in tensors or not 1 <= nd <= 4:
                raise ValueError('tenseur dupliqué ou dimensions invalides')
            dims = [r.unpack('Q') for _ in range(nd)]
            typ, offset = r.unpack('I'), r.unpack('Q')
            if any(d == 0 or d > 1000000 for d in dims) or offset % alignment:
                raise ValueError(f'{name}: dimensions/alignement invalides')
            # Procédé R7: matrices Q8_0, vecteurs de normalisation F32.
            if (nd == 1 and typ != 0) or (nd > 1 and typ != 8):
                raise ValueError(f'{name}: quantification {typ} inattendue')
            if typ == 8 and dims[0] % 32:
                raise ValueError(f'{name}: bloc Q8_0 incomplet')
            nbytes = math.prod(dims) * 4 if typ == 0 else math.prod(dims) // 32 * 34
            tensors[name] = dims
            ranges.append((offset, offset+nbytes, name))
            types['F32' if typ == 0 else 'Q8_0'] += 1
        for name, dims in {'token_embd.weight':[4096,100278], 'output.weight':[4096,100278],
                           'output_norm.weight':[4096]}.items():
            if tensors.get(name) != dims:
                raise ValueError(f'{name}: absent ou forme incorrecte')
        expected_names = {'token_embd.weight', 'output.weight', 'output_norm.weight'}
        layer_shapes = {'ffn_down':[11008,4096], 'ffn_gate':[4096,11008],
                        'ffn_up':[4096,11008], 'post_attention_norm':[4096],
                        'post_ffw_norm':[4096], 'attn_k_norm':[4096], 'attn_q_norm':[4096],
                        'attn_k':[4096,4096], 'attn_q':[4096,4096],
                        'attn_v':[4096,4096], 'attn_output':[4096,4096]}
        for layer in range(32):
            for suffix, shape in layer_shapes.items():
                name = f'blk.{layer}.{suffix}.weight'
                expected_names.add(name)
                if tensors.get(name) != shape:
                    raise ValueError(f'{name}: absent ou forme incorrecte')
        if set(tensors) != expected_names:
            raise ValueError('ensemble de tenseurs incorrect')
        if sum(math.prod(d) for d in tensors.values()) != 7298011136:
            raise ValueError('nombre de paramètres incorrect')
        data_start = (f.tell()+alignment-1)//alignment*alignment
        end = 0
        for begin, stop, name in sorted(ranges):
            if begin < end or data_start + stop > size:
                raise ValueError(f'{name}: chevauchement ou fichier tronqué')
            if begin != (end+alignment-1)//alignment*alignment:
                raise ValueError(f'{name}: trou inattendu entre tenseurs')
            end = stop
        if not 0 <= size - (data_start+end) < alignment:
            raise ValueError('taille finale incohérente')
        return {'path':str(path), 'status':'PASS', 'bytes':size, 'tensors':count,
                'types':dict(types), 'data_offset':data_start,
                'metadata_bytes_read':f.tell(), 'scope':'structure seulement, sans hash des poids'}


def validate(path):
    try:
        return inspect(path)
    except (OSError, ValueError, UnicodeError, struct.error) as exc:
        return {'path':str(path), 'status':'FAIL', 'error':str(exc)}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('files', nargs='*', type=Path)
    args = ap.parse_args()
    paths = args.files or [CACHE/'gguf'/f'Olmo-3-7B-{k}-Q8_0.gguf' for k in ('base','sft','dpo','rlvr')]
    results = [validate(p) for p in paths]
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return int(any(r['status'] != 'PASS' for r in results))


if __name__ == '__main__':
    raise SystemExit(main())
