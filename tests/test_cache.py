from systems.cache import LRUCache


def test_lru_cache_evicts_least_recently_used_item():
    cache = LRUCache[str, int](capacity=2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1

    cache.put("c", 3)

    assert cache.get("b") is None
    assert cache.get("a") == 1
    assert cache.get("c") == 3
