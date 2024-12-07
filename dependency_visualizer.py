import argparse
import os
from graphviz import Digraph
import xml.etree.ElementTree as ET
import subprocess

"""
Парсинг зависимостей из файла pom.xml.
Возвращает словарь зависимостей.
"""
def get_maven_dependencies():
    result = subprocess.run(
        ["mvn", "dependency:tree"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"Ошибка Maven: {result.stderr}")
    return result.stdout

def parse_dependencies(pom_path):

    tree = ET.parse(pom_path)
    root = tree.getroot()

    # Пространства имен Maven
    namespaces = {'mvn': 'http://maven.apache.org/POM/4.0.0'}

    dependencies = {}
    for dependency in root.findall(".//mvn:dependency", namespaces):
        group_id = dependency.find("mvn:groupId", namespaces).text
        artifact_id = dependency.find("mvn:artifactId", namespaces).text
        version = dependency.find("mvn:version", namespaces).text

        package = f"{group_id}:{artifact_id}:{version}"
        dependencies[package] = []

    return dependencies

"""
Создаёт граф зависимостей и сохраняет его в формате PNG.
"""
def generate_graph(dependencies, output_path):
    dot = Digraph(comment="Dependency Graph")

    for package, deps in dependencies.items():
        dot.node(package, package)  # Главный узел
        for dep in deps:
            dot.edge(package, dep)  # Ребро к зависимостям

    dot.render(output_path, format="png", cleanup=True)

"""
Обрабатывает аргументы командной строки.
"""
def parse_arguments():

    parser = argparse.ArgumentParser(description="Dependency Graph Visualizer")

    parser.add_argument("--graphviz-path", required=True, help="Путь к программе для визуализации графов")
    parser.add_argument("--package", required=True, help="Имя анализируемого пакета")
    parser.add_argument("--output", required=True, help="Путь к файлу с изображением графа зависимостей (png)")
    parser.add_argument("--repository-url", required=True, help="URL-адрес репозитория")

    return parser.parse_args()

def main():
    args = parse_arguments()

    # Проверяем существование Graphviz
    if not os.path.exists(args.graphviz_path):
        raise FileNotFoundError(f"Graphviz не найден по указанному пути: {args.graphviz_path}")

    # Анализ зависимостей
    pom_path = "pom.xml"  # Путь к pom.xml
    if not os.path.exists(pom_path):
        raise FileNotFoundError(f"pom.xml не найден по пути: {pom_path}")

    dependencies = parse_dependencies(pom_path)
    generate_graph(dependencies, args.output)
    print(f"Граф зависимостей сохранён в {args.output}.png")

if __name__ == "__main__":
    main()
