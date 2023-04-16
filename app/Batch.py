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

def recursive_split(total, min_value=20, max_value=50):
    if total < 2 * min_value:
        return [total]
    
    split_point = random.randint(min_value, min(total - min_value, max_value))
    first_part = recursive_split(split_point, min_value, max_value)
    second_part = recursive_split(total - split_point, min_value, max_value)
    
    return first_part + second_part

def create_random_batches(total):
    random_numbers_list = recursive_split(total)
    batches = [Batch(i, random_numbers_list[i]) for i in range(len(random_numbers_list))]
    return batches

