import math

from model import LockElementithTask
from extract import get_lock_list, get_task_list
from hardcore import BLOCKS
import pydash
from pprint import pprint

# global variables
epsilon = 0.001
schedulable = 0
blk_response_time = []
blocks_list = BLOCKS
task_list = []
for block in blocks_list:
    task_list.append(block[0])


def equalsf(x, y):
    return abs(x - y) < epsilon


# We are not considering task, rather we have blocks
def isSat_eqn2(init_li: float, current_li: float, high_tasks):
    new_li = init_li
    for task in high_tasks:
        new_li += math.ceil(
            current_li / (float(pydash.get(task, "time_period")))
        ) * float(pydash.get(task, "WCET"))

    if equalsf(current_li, new_li):
        return True
    else:
        return False


def computeL_ilk(current_li, prev_li, high_tasks):
    new_li = current_li
    for task in high_tasks:
        new_li += math.ceil(
            current_li / (float(pydash.get(task, "time_period")))
        ) * float(pydash.get(task, "WCET"))
        new_li -= math.ceil(prev_li / (float(pydash.get(task, "time_period")))) * float(
            pydash.get(task, "WCET")
        )
    return new_li


def loop(
    init_li: float, current_li: float, prev_li: float, blk, allblockList, task_number
):
    prio = blk["priority"]
    tasklist = [task[0] for task in allblockList]
    high_tasks = list(filter(lambda x: x["priority"] > prio, tasklist))
    if not isSat_eqn2(init_li, current_li, high_tasks) and current_li < float(
        blk["time_period"]
    ):
        new_l_ilk = computeL_ilk(current_li, prev_li, high_tasks)
        return loop(init_li, new_l_ilk, current_li, blk, allblockList, task_number)
    else:
        if current_li >= float(blk["time_period"]):
            print(f"Unschedulable blk - {blk['type']}")
            return -1
        else:
            return current_li


def worst_case_time_of_bloack(block, allblockList, task_number, block_number):
    if pydash.has(block, "WCRT"):
        return pydash.get(block, "WCRT")
    else:
        cij = pydash.get(block, "WCET")
        L = []
        prio = block["priority"]

        """
        Extra for nested goes here
        """
        # Iterate over all the blocks in allblocklist
        for i in range(len(allblockList)):
            task = allblockList[i]
            if pydash.get(task[0], "priority") <= prio:
                continue
            # Iterate over nst_blocks in allblocklist[i]
            for j in range(len(allblockList[i])):
                # This PART IS REMAINING TO CODE
                if pydash.get(allblockList[i][j], "type") == pydash.get(block, "type"):
                    for nested_lock in pydash.get(block, "nested"):
                        L += [pydash.get(allblockList[i][j], "type")]
        """
        Extra for nested completed here
        """
        
        # task number says index of the task in allblocklist
        # block number says index of the block in allblocklist[task_number]
        for nested_lock in pydash.get(block, "nested"):
            pprint(allblockList[task_number])
            print("\n")
            pprint(block)
            print("###################")
            L += [pydash.get(allblockList[task_number][nested_lock], "type")]
        waiting_time = 0
        for lock in L:
            time = 0
            for i in range(len(allblockList)):
                task = allblockList[i]
                if pydash.get(task[0], "priority") >= prio:
                    continue
                for j in range(len(allblockList[i])):
                    if pydash.get(allblockList[i][j], "type") == lock:
                        time = max(
                            time,
                            worst_case_time_of_bloack(
                                allblockList[i][j], allblockList, i, j
                            ),
                        )
            waiting_time += time

        wcrt = loop(
            cij + waiting_time, cij + waiting_time, 0, block, allblockList, task_number
        )
        pydash.set_(allblockList[task_number][block_number], "WCRT", wcrt)
        return wcrt


def worst_blk_RT(allblockList):
    for i in range(len(allblockList)):
        for j in range(len(allblockList[i])):
            block = allblockList[i][j]
            worst_case_time_of_bloack(block, allblockList, i, j)


# Need to pass block_list which has ig all the locks
all_block_list = []

# ALL BLOCK LIST IS LIST OF ALL THE BLOCKS, BUT FOR A TASK ALL BLOCKS ARE STORED IN THE FORM OF INSIDE LIST, SO ITS NESTED LIST

for block in blocks_list:
    block_list = list(block.values())
    all_block_list += [block_list]

worst_blk_RT(all_block_list)
print('\n')
# pprint(all_block_list)