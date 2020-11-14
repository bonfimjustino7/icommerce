# TODO melhorar rotina para retornar o valor se baseando também no pai
def get_value_graph(graph: dict, key):
    for k in graph.keys():
        if k == key:
            return graph[k]

        if isinstance(graph[k], dict):
            path = get_value_graph(graph[k], key)
            if path:
                return path

        if isinstance(graph[k], list) or isinstance(graph[k], tuple):
            for item in graph[k]:
                if item == key:
                    return item

                if isinstance(item, dict):
                    path = get_value_graph(item, key)
                    if path:
                        return path

    return None


def clean_description(name):
    name_clean = name.split('#')
    if len(name_clean[0]) > 20:
        name_clean = name_clean[0]
    else:
        name_clean = name

    return name_clean