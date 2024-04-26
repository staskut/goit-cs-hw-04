import multiprocessing
from collections import defaultdict
from pathlib import Path
from pprint import pprint
import timeit

from search_substrings_with_multithreading import search_keywords


def worker_function(file_partition, keywords, queue):
    results = search_keywords(file_partition, keywords)
    # замість додавання в загальний словник як в випадку з потоками, тут процеси "спілкуються" через чергу
    queue.put(results)

def multi_processing_search(file_paths, keywords):
    num_processes = 4
    processes = []
    # файли поділені так само - і-тий процес отримує кожний і-тий файл, наприклад 0, 4, 8 і тд
    file_partitions = [file_paths[i::num_processes] for i in range(num_processes)]
    # черга пуста, використовується тільки для сбору результатів
    queue = multiprocessing.Queue()

    for i in range(num_processes):
        # кожному процесу даємо свої файли, ключові слова і загальну чергу для запису результатів пошуку
        process = multiprocessing.Process(target=worker_function, args=(file_partitions[i], keywords, queue))
        processes.append(process)
        process.start()

    # чекаємо поки всі процеси закінчать виконання
    for process in processes:
        process.join()

    # в кінці так само як з потоками збираємо все в один словник
    final_results = defaultdict(list)
    for _ in processes:
        results = queue.get()
        for keyword, paths in results.items():
            final_results[keyword].extend(paths)

    return final_results

def main():
    file_paths = list(Path("./data").iterdir())
    keywords = ['behave', 'insult', 'betray', 'Contents', 'cover', 'Frankenstein']
    results = multi_processing_search(file_paths, keywords)
    # pprint(results)

if __name__=="__main__":
    execution_time = timeit.timeit('main()', globals=globals(), number=100)
    print(f"\nExecution Time: {execution_time} seconds")
    # Execution Time: 5.3568655839999995 seconds

    # судячи з результату, мультипроцесинг в цьому випадку не відповідає складності завдання і додаткові витрати часу
    # перевершують потенціальне прискорення