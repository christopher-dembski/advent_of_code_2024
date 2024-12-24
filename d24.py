from collections import defaultdict


def parse_input(file_name):
    with open(file_name) as f:
        string = f.read().strip()
    wires, logic_gates = string.split('\n\n')
    return parse_wires(wires), parse_logic_gates(logic_gates)


def parse_wires(string):
    wires = {}
    for line in string.split('\n'):
        name, value = line.split(': ')
        wires[name] = int(value)
    return wires


def parse_logic_gates(string):
    gates = []
    for line in string.split('\n'):
        left_input_gate, gate_type, right_input_gate, _, output_gate = line.split()
        gates.append((left_input_gate, gate_type, right_input_gate, output_gate))
    return gates


def get_gate_output(left_input_value, right_input_value, gate_type):
    if gate_type == 'AND':
        return left_input_value and right_input_value
    if gate_type == 'OR':
        return left_input_value or right_input_value
    if gate_type == 'XOR':
        return left_input_value != right_input_value


def build_graph(gates):
    graph = defaultdict(set)  # gate -> gates_that_are_inputs_to_this_gate_and_must_precede
    for left_input_gate, _, right_input_gate, output_gate in gates:
        graph[left_input_gate].add(output_gate)
        graph[right_input_gate].add(output_gate)
    return graph


def get_nodes_with_no_incoming_edge(graph):
    nodes = set(graph.keys())
    for start_edge, adjacent_edges in graph.items():
        nodes.difference_update(adjacent_edges)
    return nodes


def topoligcal_sort(graph):  # Kahn's Algorithm
    sorted_list = []
    working_list = get_nodes_with_no_incoming_edge(graph)
    while working_list:
        node = working_list.pop()
        sorted_list.append(node)
        for adjacent in set(graph[node]):
            graph[node].remove(adjacent)
            # if no incoming edge
            if not any(adjacent in nodes for nodes in graph.values()):
                working_list.add(adjacent)
    return sorted_list


def get_wire_values(wires, gates):
    wires = dict(wires)  # do not mutate input
    graph = build_graph(gates)
    # output_gate_name -> gate
    gates_table = {gate[-1]: gate for gate in gates}
    sorted_gates = topoligcal_sort(graph)
    for gate in sorted_gates:
        if gate not in gates_table:  # not an output gate, so do not need to compute value
            continue
        left_input_gate, gate_type, right_input_gate, output_gate = gates_table[gate]
        wires[output_gate] = get_gate_output(
            wires[left_input_gate],
            wires[right_input_gate],
            gate_type
        )
    return wires


def get_wire_output(wires):
    result = 0
    z_gates = sorted((gate for gate in wires if gate.startswith('z')), reverse=True)
    for gate in z_gates:
        result *= 2
        result += wires[gate]
    return result


def part_one(wires, gates):
    return get_wire_output(get_wire_values(wires, gates))


if __name__ == '__main__':
    print(part_one(*parse_input('inputs/d24.txt')))
