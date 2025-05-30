
import os
import pytest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'source')))

from compare import compare_with_lists, compare_with_counters, compare_with_counters_only

@pytest.fixture
def sample_data():
    gold_lines = ['line1\n', 'line2\n', 'line3\n'] * 1000
    new_lines = ['line1\n', 'line3\n', 'line4\n'] * 1000
    return gold_lines, new_lines

def test_list_comparison(benchmark, sample_data):
    gold, new = sample_data
    result = benchmark(compare_with_lists, gold, new)
    assert isinstance(result, list)

def test_counter_comparison(benchmark, sample_data):
    gold, new = sample_data
    result = benchmark(compare_with_counters, gold, new)
    assert isinstance(result, list)

def test_counters_only_comparison(benchmark, sample_data):
    gold, new = sample_data
    result = benchmark(compare_with_counters_only, gold, new)
    assert isinstance(result, list)