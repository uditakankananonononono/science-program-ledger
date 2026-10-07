"""Exact directed-graph routing units. Standard algorithms, not novelty claims.
All edge costs must be nonnegative finite numbers. No physiology is inferred.
"""
from dataclasses import dataclass
import heapq
import math

@dataclass(frozen=True)
class Edge:
    target: str
    time: float
    exposure: float
    scenario_times: tuple = ()


def validate(graph, start, goal):
    if start not in graph or goal not in graph:
        raise ValueError('start and goal must be graph vertices')
    if any(not isinstance(v, str) for v in graph):
        raise ValueError('vertex identifiers must be strings')
    for edges in graph.values():
        for e in edges:
            if not isinstance(e, Edge) or not isinstance(e.scenario_times, tuple):
                raise ValueError('edges must be Edge objects with tuple scenarios')
            if e.target not in graph:
                raise ValueError('edge target missing from graph')
            for x in (e.time, e.exposure, *e.scenario_times):
                if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or x < 0:
                    raise ValueError('costs must be finite and nonnegative')


def finite_totals(*values):
    if any(not math.isfinite(v) for v in values):
        raise OverflowError('accumulated route cost overflow')


def witness(graph, path, indices):
    return [dict(source=node, edge_index=index, target=graph[node][index].target)
            for node, index in zip(path, indices)]


def exposure_budget_route(graph, start, goal, budget):
    """Minimize total time subject to additive exposure <= budget.

    Pareto label search. Can require exponentially many labels; no scalability
    claim. Returns None if infeasible, or a dict with path and exact cost totals.
    """
    validate(graph, start, goal)
    if not isinstance(budget, (int, float)) or isinstance(budget, bool) or not math.isfinite(budget) or budget < 0:
        raise ValueError('budget must be finite and nonnegative')
    labels = {v: [] for v in graph}
    labels[start].append((0, 0))
    queue = [(0, 0, (start,), ())]
    while queue:
        time, exposure, path, indices = heapq.heappop(queue)
        node = path[-1]
        if (time, exposure) not in labels[node]:
            continue
        if node == goal:
            return dict(path=list(path), time=time, exposure=exposure, edges=witness(graph, path, indices))
        for index, e in enumerate(graph[node]):
            t, r = time + e.time, exposure + e.exposure
            finite_totals(t, r)
            if r > budget:
                continue
            if any(a <= t and b <= r for a, b in labels[e.target]):
                continue
            labels[e.target] = [(a, b) for a, b in labels[e.target] if not (t <= a and r <= b)]
            labels[e.target].append((t, r))
            heapq.heappush(queue, (t, r, path + (e.target,), indices + (index,)))
    return None


def scenario_robust_route(graph, start, goal):
    """Minimize worst total route time across fixed common scenarios.

    Uses vector-valued Pareto labels, not the sum of per-edge worst cases.
    Scenarios are user-supplied assumptions; output is not clinical validation.
    """
    validate(graph, start, goal)
    lengths = {len(e.scenario_times) for edges in graph.values() for e in edges}
    if len(lengths) != 1 or not lengths or next(iter(lengths)) == 0:
        raise ValueError('all edges require the same positive scenario count')
    n = next(iter(lengths))
    zero = (0,) * n
    labels = {v: [] for v in graph}
    labels[start].append(zero)
    queue = [(0, zero, (start,), ())]
    while queue:
        worst, totals, path, indices = heapq.heappop(queue)
        node = path[-1]
        if totals not in labels[node]:
            continue
        if node == goal:
            return dict(path=list(path), scenario_totals=list(totals), worst_time=worst, edges=witness(graph, path, indices))
        for index, e in enumerate(graph[node]):
            new = tuple(a + b for a, b in zip(totals, e.scenario_times))
            finite_totals(*new)
            if any(all(a <= b for a, b in zip(old, new)) for old in labels[e.target]):
                continue
            labels[e.target] = [old for old in labels[e.target] if not all(a <= b for a, b in zip(new, old))]
            labels[e.target].append(new)
            heapq.heappush(queue, (max(new), new, path + (e.target,), indices + (index,)))
    return None


def budgeted_scenario_route(graph, start, goal, budget):
    """Joint deterministic exposure budget and common-scenario minimax time.
    Standard multidimensional Pareto labeling; not a new algorithm.
    """
    validate(graph, start, goal)
    if isinstance(budget, bool) or not isinstance(budget, (int, float)) or not math.isfinite(budget) or budget < 0:
        raise ValueError('budget must be finite and nonnegative')
    lengths = {len(e.scenario_times) for edges in graph.values() for e in edges}
    if len(lengths) != 1 or not lengths or next(iter(lengths)) == 0:
        raise ValueError('all edges require the same positive scenario count')
    n = next(iter(lengths))
    zero = (0,) * n
    labels = {v: [] for v in graph}
    labels[start].append((0, *zero))
    queue = [(0, 0, zero, (start,), ())]
    while queue:
        worst, exposure, totals, path, indices = heapq.heappop(queue)
        node = path[-1]
        if (exposure, *totals) not in labels[node]:
            continue
        if node == goal:
            return dict(path=list(path), exposure=exposure, scenario_totals=list(totals), worst_time=worst, edges=witness(graph, path, indices))
        for index, e in enumerate(graph[node]):
            risk = exposure + e.exposure
            finite_totals(risk)
            if risk > budget:
                continue
            new = tuple(a + b for a, b in zip(totals, e.scenario_times))
            finite_totals(*new)
            vector = (risk, *new)
            if any(all(a <= b for a, b in zip(old, vector)) for old in labels[e.target]):
                continue
            labels[e.target] = [old for old in labels[e.target] if not all(a <= b for a, b in zip(vector, old))]
            labels[e.target].append(vector)
            heapq.heappush(queue, (max(new), risk, new, path + (e.target,), indices + (index,)))
    return None
