def get_lock_list():
    lock_blocks = []

    with open('locks.txt', 'r') as file:
        lines = file.readlines()

        block = {}
        for line in lines:
            line = line.strip()
            
            if line.startswith("Line No:"):
                if block:
                    lock_blocks.append(block)
                block = {}
                
                # Extracting values from the line
                block["line_no"] = int(line.split(":")[1].strip())
            elif line.startswith("Task Name:"):
                block["task_name"] = line.split(":")[1].strip()
            elif line.startswith("Lock Name:"):
                block["lock_name"] = line.split(":")[1].strip()
            elif line.startswith("Number of Occurrences:"):
                block["number_occur"] = int(line.split(":")[1].strip())
            elif line.startswith("Prior:"):
                block["prior"] = int(line.split(":")[1].strip())
            elif line.startswith("WCET:"):
                block["wcet"] = float(line.split(":")[1].strip())
        
        # Adding the last block to lock_blocks
        if block:
            lock_blocks.append(block)

    # Print lock_blocks
    # for block in lock_blocks:
    #     print("Line No:", block["line_no"])
    #     print("Task Name:", block["task_name"])
    #     print("Lock Name:", block["lock_name"])
    #     print("Prior:", block["prior"])
    #     print("Number of Occurrences:", block["number_occur"])
    #     print("WCET:", block["wcet"])
    #     print()
    return lock_blocks


def get_task_list():
    tasks = []

    with open('tasks.txt', 'r') as file:
        lines = file.readlines()

        task = {}
        for line in lines:
            line = line.strip()
            
            if line.startswith("Task Name:"):
                if task:
                    tasks.append(task)
                task = {}
                
                # Extracting values from the line
                task["tname"] = line.split(":")[1].strip()
            elif line.startswith("File Name:"):
                task["fname"] = line.split(":")[1].strip()
            elif line.startswith("Priority:"):
                task["priority"] = int(line.split(":")[1].strip())
            elif line.startswith("periodicity:"):
                task["periodicity"] = int(line.split(":")[1].strip())
            elif line.startswith("WCET:"):
                task["wcet"] = float(line.split(":")[1].strip())
        
        # Adding the last task to tasks
        if task:
            tasks.append(task)

    # Print tasks
    for task in tasks:
        print("Task Name:", task["tname"])
        print("File Name:", task["fname"])
        print("Priority:", task["priority"])
        print("Periodicity:", task["periodicity"])
        print("WCET:", task["wcet"])
        print()
    return tasks