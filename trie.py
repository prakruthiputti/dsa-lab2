
import tkinter as tk
from tkinter import filedialog, messagebox
import time
import random


class TrieNode:
    def __init__(self):
        self.children = {}
        self.lines = []


class TrieIndex:
    def __init__(self):
        self.root = TrieNode()

    def add(self, word, line):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.lines.append(line)

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return None
            node = node.children[char]
        return node.lines if node.lines else None

    def words_sorted(self):
        result = []

        def visit(node, prefix):
            if node.lines:
                result.append(prefix)
            for char in sorted(node.children):
                visit(node.children[char], prefix + char)

        visit(self.root, "")
        return result


def read_input(filename):
    separators = set(" \t\r\n\f\v.,:;")
    occurrences = []

    with open(filename, "r", encoding="ascii",
              errors="replace") as file:
        for line_no, line in enumerate(file, 1):
            word = ""

            for char in line:
                if char in separators:
                    if word:
                        occurrences.append((word, line_no))
                        word = ""
                else:
                    word += char

            if word:
                occurrences.append((word, line_no))

    return occurrences


def main():
    root = tk.Tk()
    root.withdraw()

    input_file = filedialog.askopenfilename(
        title="Select Input Text File",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )

    if not input_file:
        root.destroy()
        return

    output_file = filedialog.asksaveasfilename(
        title="Save Trie Index",
        initialfile="trie_output.txt",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")]
    )

    if not output_file:
        root.destroy()
        return

    try:
        occurrences = read_input(input_file)

        trie = TrieIndex()

        start = time.perf_counter()
        for word, line in occurrences:
            trie.add(word, line)
        build_time = time.perf_counter() - start

        words = trie.words_sorted()

        search_words = [
            random.choice(words) if words else "missingword"
            for _ in range(100_000)
        ]

        start = time.perf_counter()
        for word in search_words:
            trie.search(word)
        search_time = time.perf_counter() - start

        start = time.perf_counter()
        with open(output_file, "w", encoding="ascii",
                  errors="replace") as file:
            for word in words:
                file.write(
                    f"{word}: {', '.join(map(str, trie.search(word)))}\n"
                )
        print_time = time.perf_counter() - start

        print("\nTRIE INDEX RESULTS")
        print("Total occurrences:", len(occurrences))
        print("Distinct words:", len(words))
        print(f"Construction time: {build_time:.6f} seconds")
        print(f"100,000 searches: {search_time:.6f} seconds")
        print(f"Printing time: {print_time:.6f} seconds")
        print("Output saved to:", output_file)

        messagebox.showinfo(
            "Success", "Trie index generated successfully!"
        )

    except (OSError, UnicodeError) as error:
        messagebox.showerror("File Error", str(error))

    finally:
        root.destroy()


if __name__ == "__main__":
    main()
