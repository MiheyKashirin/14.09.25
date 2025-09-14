import multiprocessing as mp

def collatz(n):
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
    return True

def check_range(start, end, stop_event, report_queue):
    for n in range(start, end):
        if stop_event.is_set():
            return
        collatz(n)
    report_queue.put((start, end))

def worker(task_queue, stop_event, report_queue):
    while not stop_event.is_set():
        try:
            start, end = task_queue.get(timeout=1)
        except:
            break
        check_range(start, end, stop_event, report_queue)

def main(start=1, stop=1000000, chunk=10000, workers=None):
    if workers is None:
        workers = mp.cpu_count()
    manager = mp.Manager()
    task_queue = manager.Queue()
    report_queue = manager.Queue()
    stop_event = manager.Event()
    for i in range(start, stop + 1, chunk):
        task_queue.put((i, min(i + chunk, stop + 1)))
    processes = []
    for _ in range(workers):
        p = mp.Process(target=worker, args=(task_queue, stop_event, report_queue))
        p.start()
        processes.append(p)
    total_chunks = (stop - start + chunk) // chunk
    done_chunks = 0
    while done_chunks < total_chunks:
        report_queue.get()
        done_chunks += 1
        print(f"Прогресс: {done_chunks}/{total_chunks} порций")
    for p in processes:
        p.join()

if __name__ == "__main__":
    main()
