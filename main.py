import threading
import queue
import datetime

class Producer:
    def __init__(self, buffer, max_count, lock, log_file):
        self.buffer = buffer
        self.max_count = max_count
        self.counter = 1
        self.lock = lock
        self.log_file = log_file

    def produce_numbers(self):
        while self.counter <= self.max_count:
            number = self.counter
            self.buffer.put(number)
            self.log_data("Produced", number)
            self.counter += 1

    def log_data(self, process, number):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = f"{current_time} | {process} | Number: {number}\n"
        with self.lock:
            with open(self.log_file, 'a') as file:
                file.write(data)

class Consumer:
    def __init__(self, buffer, lock, log_file):
        self.buffer = buffer
        self.lock = lock
        self.log_file = log_file

    def consume_numbers(self):
        while True:
            number = self.buffer.get()
            self.log_data("Consumed", number)
            self.buffer.task_done()

    def log_data(self, process, number):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = f"{current_time} | {process} | Number: {number}\n"
        with self.lock:
            with open(self.log_file, 'a') as file:
                file.write(data)



buffer = queue.Queue(maxsize=10)
lock = threading.Lock()

log_file = "buffer_logs.txt"

producer = Producer(buffer, max_count=100, lock=lock, log_file=log_file)
consumer = Consumer(buffer, lock=lock, log_file=log_file)

# Create a thread for producing numbers
producer_thread = threading.Thread(target=producer.produce_numbers)

# Create a thread for consuming numbers
consumer_thread = threading.Thread(target=consumer.consume_numbers)

# Start the threads
producer_thread.start()
consumer_thread.start()

# Wait for the producer to finish
producer_thread.join()

# Wait for the consumer to finish
buffer.join()
consumer_thread.join()

print("Producer and consumer threads have finished.")
