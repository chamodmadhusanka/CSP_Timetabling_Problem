from copy import deepcopy
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]


def read_file(filename):
    with open(filename, 'r') as fo:
        subjects = []
        time_slots = []
        rows = fo.readlines()
        for i in range(len(rows) - 1):
            line = rows[i].strip().split(',')
            subjects.append(tuple(line[:2]))
            time_slots.append(line[2:])
        rooms = rows[-1].strip().split(',')
        return subjects, time_slots, rooms


def find_subject_not_assigned(solution_assign, temp_subs):
    for temp in temp_subs:
        if temp[0] not in solution_assign:
            return temp


def is_used(solution_assign, temp_subs):
    used_timeslots = []
    used_rooms = []

    for key, value in solution_assign.items():
        if (key, 'c') in temp_subs:
            if value[0] in used_timeslots:
                return False
            else:
                used_timeslots.append(value[0])

        if (value[0], value[1]) in used_rooms:
            return False
        else:
            used_rooms.append((value[0], value[1]))
    return True


def get_assign(solution_assign, temp_subs, time_slots, rooms):
    # if all the subjects get assigned timeslots and rooms, return it
    if len(solution_assign) == len(temp_subs):
        return solution_assign

    temp = find_subject_not_assigned(solution_assign, temp_subs)
    vacant_slots = time_slots[temp_subs.index(temp)]

    for time_slot in vacant_slots:
        for room in rooms:
            next_assign = deepcopy(solution_assign)
            next_assign[temp[0]] = (time_slot, room)
            if is_used(next_assign, temp_subs):
                solution_assign[temp[0]] = (time_slot, room)
                result = get_assign(solution_assign, temp_subs, time_slots, rooms)
                if result:
                    return result
                solution_assign.pop(temp[0])
    return False


def write_to_file(filename, assign_t_r):
    with open(filename, 'w') as fo:
        for key, value in assign_t_r.items():
            fo.write(key + ',' + value[0] + ',' + value[1] + '\n')


if __name__ == '__main__':
    subjects, time_slots, rooms = read_file(input_file)
    assign_t_r = get_assign({}, subjects, time_slots, rooms)
    write_to_file(output_file, assign_t_r)
