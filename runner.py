import task1
import task2
import json


result1 = task1.run()
task_2 = task2.Task2()
result2 = task_2.run()

full_result = {"1": result1, "2": result2}
print(json.dumps(full_result, indent=4))
