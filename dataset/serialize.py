import json
from typing import List, Tuple, Dict, Any
from knot.structure import Knot
from moves.move import Move


def knot_to_dict(knot: Knot) -> Dict[str, Any]:
    return {'seq': [list(t) for t in knot.seq]}

def knot_from_dict(d: Dict[str, Any]) -> Knot:
    tokens = [tuple(t) for t in d['seq']]
    return Knot.from_tokens(tokens)

def move_to_dict(move: Move) -> Dict[str, Any]:
    return {'kind': move.kind, 'action': move.action, 'params': move.params}

def move_from_dict(d: Dict[str, Any]) -> Move:
    return Move(kind=d['kind'], action=d['action'], params=d['params'])

def trace_to_list(trace: List[Move]) -> List[Dict[str, Any]]:
    return [move_to_dict(m) for m in trace]

def trace_from_list(data: List[Dict[str, Any]]) -> List[Move]:
    return [move_from_dict(d) for d in data]


def positive_pair_to_dict(start: Knot, end: Knot, trace: List[Move]) -> Dict[str, Any]:
    return {
        'label': 'EQUIVALENT',
        'knot_a': knot_to_dict(start),
        'knot_b': knot_to_dict(end),
        'moves': trace_to_list(trace),
    }

def positive_pair_from_dict(d: Dict[str, Any]) -> Tuple[Knot, Knot, List[Move]]:
    return knot_from_dict(d['knot_a']), knot_from_dict(d['knot_b']), trace_from_list(d['moves'])


def negative_pair_to_dict(result: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'label': result['label'],
        'knot_a_start': knot_to_dict(result['knot_a_start']),
        'knot_a_end': knot_to_dict(result['knot_a_end']),
        'moves_a': trace_to_list(result['moves_a']),
        'knot_b_start': knot_to_dict(result['knot_b_start']),
        'knot_b_end': knot_to_dict(result['knot_b_end']),
        'moves_b': trace_to_list(result['moves_b']),
        'diff': result['diff'],
    }

def negative_pair_from_dict(d: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'label': d['label'],
        'knot_a_start': knot_from_dict(d['knot_a_start']),
        'knot_a_end': knot_from_dict(d['knot_a_end']),
        'moves_a': trace_from_list(d['moves_a']),
        'knot_b_start': knot_from_dict(d['knot_b_start']),
        'knot_b_end': knot_from_dict(d['knot_b_end']),
        'moves_b': trace_from_list(d['moves_b']),
        'diff': d['diff'],
    }


def save_jsonl(records: List[Dict[str, Any]], path: str) -> None:
    """Save a list of already-dict-converted records, one JSON object per line
    (the standard 'JSONL' format for ML datasets — easy to append to, easy
    to stream without loading the whole file into memory)."""
    with open(path, 'w') as f:
        for record in records:
            f.write(json.dumps(record) + '\n')

def load_jsonl(path: str) -> List[Dict[str, Any]]:
    """Load a JSONL file back into a list of raw dicts. Caller is responsible
    for converting each dict back via positive_pair_from_dict / negative_pair_from_dict
    based on the 'label' field, since the two record shapes differ."""
    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records