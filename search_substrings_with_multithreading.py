import threading
from pathlib import Path
from collections import defaultdict
from pprint import pprint
import timeit


def search_keywords(files, keywords):
    results = defaultdict(list)
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            for keyword in keywords:
                if keyword in content:
                    results[keyword].append(file_path.name)
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
    return results

def thread_function(file_partition, keywords, result_dict, thread_id):
    results = search_keywords(file_partition, keywords)
    # кожний потік повертає свій словник, який додається до глобального списку з ключем номера потоку
    result_dict[thread_id] = results

def multi_threaded_search(file_paths, keywords):
    num_threads = 4
    threads = []
    #  поділити файли порівну, беручи кожний і-ий файл, наприклад якщо 4 потоки, то перший поток отримає файли з індексом
    # 0, 4, 8 і т.д.
    file_partitions = [file_paths[i::num_threads] for i in range(num_threads)]
    thread_results = [{} for _ in range(num_threads)]

    for i in range(num_threads):
        thread = threading.Thread(target=thread_function, args=(file_partitions[i], keywords, thread_results, i))
        threads.append(thread)
        thread.start()

    # чекаємо поки всі потоки завершать виконання
    for thread in threads:
        thread.join()

    # тепер треба злити рзультати за ключовими словами, наприклад якщо потік1 знайшов слово1 в файлі1, а потік2
    # знайшов теж слово1 але в файлі2, то треба отримати {слово1: [файл1, файл2],...}
    final_results = defaultdict(list)
    for thread_result in thread_results:
        for keyword, paths in thread_result.items():
            final_results[keyword].extend(paths)
    return final_results


def main():
    file_paths = list(Path("./data").iterdir())
    keywords = ['behave', 'insult', 'betray', 'Contents', 'cover', 'Frankenstein']
    results = multi_threaded_search(file_paths, keywords)
    # pprint(results)


if __name__=="__main__":
    execution_time = timeit.timeit('main()', globals=globals(), number=100)
    print(f"\nExecution Time: {execution_time} seconds")
    # Execution Time: 1.352014 seconds