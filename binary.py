
import tkinter as tk
from tkinter import filedialog, messagebox
import time
import random


class Node:
    def __init__(self, word, line):
        self.word = word
        self.lines = [line]
        self.left = None
        self.right = None


class BSTIndex:
    def __init__(self):
        self.root = None

    def add(self, word, line):
        if self.root is None:
            self.root = Node(word, line)
            return

        current = self.root

        while True:
            if word == current.word:
                current.lines.append(line)
                return

            if word < current.word:
                if current.left is None:
                    current.left = Node(word, line)
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = Node(word, line)
                    return
                current = current.right

    def search(self, word):
        current = self.root

        while current is not None:
            if word == current.word:
                return current.lines
            elif word < current.word:
                current = current.left
            else:
                current = current.right

        return None

    def words_sorted(self):
        result = []

        def inorder(node):
            if node is None:
                return
            inorder(node.left)
            result.append(node.word)
            inorder(node.right)

        inorder(self.root)
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
        title="Save BST Index",
        initialfile="bst_output.txt",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")]
    )

    if not output_file:
        root.destroy()
        return

    try:
        occurrences = read_input(input_file)
        bst = BSTIndex()

        start = time.perf_counter()
        for word, line in occurrences:
            bst.add(word, line)
        build_time = time.perf_counter() - start

        words = bst.words_sorted()

        search_words = [
            random.choice(words) if words else "missingword"
            for _ in range(100_000)
        ]

        start = time.perf_counter()
        for word in search_words:
            bst.search(word)
        search_time = time.perf_counter() - start

        start = time.perf_counter()
        with open(output_file, "w", encoding="ascii",
                  errors="replace") as file:
            for word in words:
                file.write(
                    f"{word}: {', '.join(map(str, bst.search(word)))}\n"
                )
        print_time = time.perf_counter() - start

        print("\nBINARY SEARCH TREE RESULTS")
        print("Total occurrences:", len(occurrences))
        print("Distinct words:", len(words))
        print(f"Construction time: {build_time:.6f} seconds")
        print(f"100,000 searches: {search_time:.6f} seconds")
        print(f"Printing time: {print_time:.6f} seconds")
        print("Output saved to:", output_file)

        messagebox.showinfo(
            "Success", "BST index generated successfully!"
        )

    except (OSError, UnicodeError, RecursionError) as error:
        messagebox.showerror("Error", str(error))

    finally:
        root.destroy()


if __name__ == "__main__":
    main()
