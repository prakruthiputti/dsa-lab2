
import tkinter as tk
from tkinter import filedialog, messagebox
import time
import random


class DictionaryIndex:
    def __init__(self):
        self.data = {}

    def add(self, word, line):
        if word not in self.data:
            self.data[word] = []
        self.data[word].append(line)

    def search(self, word):
        return self.data.get(word)

    def words_sorted(self):
        return sorted(self.data.keys())


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
        title="Save Dictionary Index",
        initialfile="dictionary_output.txt",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")]
    )

    if not output_file:
        root.destroy()
        return

    try:
        occurrences = read_input(input_file)
        index = DictionaryIndex()

        start = time.perf_counter()
        for word, line in occurrences:
            index.add(word, line)
        build_time = time.perf_counter() - start

        words = index.words_sorted()

        search_words = [
            random.choice(words) if words else "missingword"
            for _ in range(100_000)
        ]

        start = time.perf_counter()
        for word in search_words:
            index.search(word)
        search_time = time.perf_counter() - start

        start = time.perf_counter()
        with open(output_file, "w", encoding="ascii",
                  errors="replace") as file:
            for word in words:
                file.write(
                    f"{word}: {', '.join(map(str, index.search(word)))}\n"
                )
        print_time = time.perf_counter() - start

        print("\nPYTHON DICTIONARY RESULTS")
        print("Total occurrences:", len(occurrences))
        print("Distinct words:", len(words))
        print(f"Construction time: {build_time:.6f} seconds")
        print(f"100,000 searches: {search_time:.6f} seconds")
        print(f"Printing time: {print_time:.6f} seconds")
        print("Output saved to:", output_file)

        messagebox.showinfo(
            "Success", "Dictionary index generated successfully!"
        )

    except (OSError, UnicodeError) as error:
        messagebox.showerror("File Error", str(error))

    finally:
        root.destroy()


if __name__ == "__main__":
    main()
