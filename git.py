
import os
import zlib

from graphviz import Digraph


def clearMessage(message):
    # b'Adding readme'
    return message.decode("utf-8")


def clearParents(dt):
    "b'parent 2ac228697173ab1e6381ed608c73fd022af11a4b'"
    # каждую запись такого вида разбиваем по пробелам, берем хеш как второй элемент
    # добавляем в список, предварительно декодировав его
    # возвращаем список
    return [parent.split(b" ")[-1].decode("utf-8") for parent in dt if parent.startswith(b"parent")]


def deserialize(data):
    # нас интересуют следующие поля:
    # parent, message
    dt = data.split(b"\n")  # Разбиваем на строки
    # Удаляем пустые строку
    dt.remove(b"")
    dt.remove(b'')
    # информация с сообщением - последнее поле
    roughMessage = dt[-1]
    # оно выглядит так:
    # b'Adding readme'
    parents = clearParents(dt)  # чистые хеши родителей
    message = clearMessage(roughMessage)  # чистый текст сообщения
    return [parents, message]

def buildGraph(path_to_rep, graph):
    digraph = Digraph(comment=f'Git Log for {path_to_rep}')
    digraph.attr('node', shape='octagon')
    for node in graph:
        for parent in node[1]:
            digraph.edge(parent, node[0], label=node[2])
    digraph.render(f'{path_to_rep}.gv', view=True)


unpack = zlib.decompressobj()
graph = []
path_to_rep = "D:\\ConfigPr5\\ThirdTask\\bare_repo\\.git"  # Путь к репозиторию
os.chdir("D:\\ConfigPr5\\ThirdTask\\bare_repo\\.git")  # Переходим в папку с репозиторием
for path, directories, files in os.walk("../../Downloads"):  # Проходим по всем файлам
    if files:
        for file in files:
            with open(path + "\\" + file, "rb") as f:
                data = zlib.decompress(f.read())
                if data[:6] == b"commit":
                    commit_id = path[-2:] + file
                    parents, message = deserialize(data)
                    graph.append([commit_id, parents, message])
                f.close()
os.chdir("D:\\ConfigPr5")
buildGraph(path_to_rep, graph)
