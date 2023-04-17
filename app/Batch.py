import random
class Batch:
    def __init__(self, id, size):
        self.id = id
        self.size = size

    def to_dict(self):
        return {"id": self.id, "size": self.size}
    
    def __str__(self):
        return "batch" + str(self.id)
    
def divide_into_most_equal_sized_batches(total, batch_size):
    if batch_size < 20:
        batch_size = 20
    elif batch_size > 50:
        batch_size = 50
    num_batches, remainder = divmod(total, batch_size)
    batches = [Batch(i, batch_size) for i in range(1, num_batches + 1)]
    if remainder > 0 and remainder < 20:
        items_to_distribute = remainder
        for batch in batches:
            if items_to_distribute == 0:
                break
            if batch.size < 50:
                batch.size += 1
                items_to_distribute -= 1
    elif remainder >= 20:
        batches.append(Batch(num_batches + 1, remainder))
    return batches

def divide_into_random_sized_batches(total):
    splitted_list = split_total_recursively_into_numbers_between_min_and_max(total)
    batches = [Batch(i, splitted_list[i]) for i in range(len(splitted_list))]
    return batches

def split_total_recursively_into_numbers_between_min_and_max(total):
    if total < 2 * 20:
        return [total]
    
    split_point = random.randint(20, min(total - 20, 50))
    first_part = split_total_recursively_into_numbers_between_min_and_max(split_point)
    second_part = split_total_recursively_into_numbers_between_min_and_max(total - split_point)
    
    return first_part + second_part

def divide_into_increasing_batch_sizes():
    return [
        #Batch(1, 50),
        #Batch(2, 49),
        Batch(2, 48),
        Batch(3, 47),
        Batch(3, 46),
        Batch(4, 45),
        Batch(4, 44),
        Batch(5, 43),
        Batch(5, 42),
        Batch(6, 41),
        Batch(6, 40),
        Batch(7, 39),
        Batch(7, 38),
        Batch(8, 37),
        Batch(8, 36),
        Batch(9, 35),
        Batch(9, 34),
        Batch(10, 33),
        Batch(10, 32),
        Batch(11, 31),
        Batch(11, 30),
        Batch(12, 29),
        Batch(12, 28),
        Batch(13, 27),
        Batch(14, 26),
        Batch(15, 25),
        Batch(16, 24),
        Batch(17, 23),
        Batch(18, 22),
        Batch(19, 21),
        Batch(20, 20),
    ]

#def randomize_initial_batches(initial_batches):
#    total = 1000
#    lst = [batch.size for batch in initial_batches]
#    new_lst = []
#
#    for i in range(len(lst)):
#        # calculate the target value for the current element
#        target_value = (total / len(lst))
#        # add a random deviation from the target value to the current element
#        deviation = random.uniform(-0.1, 0.1) * target_value
#        new_value = round(lst[i] + deviation)
#        # ensure the new value is within a reasonable range (>= 1)
#        new_value = max(1, new_value)
#        # add the new value to the new list
#        new_lst.append(new_value)
#        # adjust the total to account for the change in the current element
#        total -= lst[i]
#        total += new_value
#
#    return [Batch(i, new_lst[i]) for i in range(len(new_lst))]

