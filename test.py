import unittest
import os
from dependency_visualizer import parse_dependencies, generate_graph

class TestDependencyVisualizer(unittest.TestCase):
    def setUp(self):
        # Создаём тестовый pom.xml
        self.test_pom = "test_pom.xml"
        with open(self.test_pom, "w") as f:
            f.write("""
            <project xmlns="http://maven.apache.org/POM/4.0.0">
                <dependencies>
                    <dependency>
                        <groupId>org.example</groupId>
                        <artifactId>example-dependency</artifactId>
                        <version>1.0</version>
                    </dependency>
                </dependencies>
            </project>
            """)

    def tearDown(self):
        # Удаляем тестовые файлы
        if os.path.exists(self.test_pom):
            os.remove(self.test_pom)
        if os.path.exists("test_graph.png"):
            os.remove("test_graph.png")

    def test_parse_dependencies(self):
        dependencies = parse_dependencies(self.test_pom)
        self.assertIn("org.example:example-dependency:1.0", dependencies)

    def test_generate_graph(self):
        dependencies = {"org.example:example-dependency:1.0": []}
        output_path = "test_graph"
        generate_graph(dependencies, output_path)
        self.assertTrue(os.path.exists(f"{output_path}.png"))

if __name__ == "__main__":
    unittest.main()
