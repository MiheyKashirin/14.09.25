import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def cache_decorator(func):
    def wrapper(n):
        if r.get(str(n)) is not None:
            print("Берем из кеша")
            return int(r.get(str(n)))
        result = func(n)
        r.set(str(n), result)
        return result
    return wrapper

@cache_decorator
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

if __name__ == "__main__":
    print("Первый вызов fibonacci(15):")
    print(fibonacci(15))

    print("\nВторой вызов fibonacci(10):")
    print(fibonacci(10))

    print("\nПервый вызов fibonacci(5):")
    print(fibonacci(6))
