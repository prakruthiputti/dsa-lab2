#Build a complete word index from a file using a dictionary, preserve repeated line numbers, and print words in ASCII lexicographical order.

import re

class Node:
    def __init__(self, line):
        self.line = line
        self.next = None

class LineList:
    def __init__(self):
        self.head = self.tail = None

    def append(self, line):
        new_node = Node(line)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def get_lines(self):
        result = []
        current = self.head
        while current:
            result.append(current.line)
            current = current.next
        return result

index = {}
separators = re.compile(r"[ \t\r\n\f\v.,:;]+")

with open("input.txt", "r") as file:
    for line_no, line in enumerate(file, 1):
        for word in separators.split(line.strip()):
            if word:
                if word not in index:
                    index[word] = LineList()
                index[word].append(line_no)

with open("output.txt", "w") as file:
    for word in sorted(index):
        lines = ", ".join(map(str, index[word].get_lines()))
        file.write(f"{word}: {lines}\n")

print("Index generated successfully.")
print("Distinct words:", len(index))
print("Output saved to output.txt")


#Implement a Trie that supports word insertion, exact search, prefix search, and alphabetical display

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root

        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]

        node.is_end = True

    def search(self, word):
        node = self.root

        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]

        return node.is_end

    def starts_with(self, prefix):
        node = self.root

        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]

        return True

    def display(self):
        def visit(node, prefix):
            if node.is_end:
                print(prefix)

            for ch in sorted(node.children):
                visit(node.children[ch], prefix + ch)

        visit(self.root, "")


trie = Trie()

for word in ["apple", "app", "apply", "bat", "ball"]:
    trie.insert(word)

print("Exact search:", trie.search("app"))
print("Prefix search:", trie.starts_with("ap"))
print("Missing prefix:", trie.starts_with("ca"))

print("All words:")
trie.display()


#Implement a BST that supports insertion, search, deletion, and sorted output.


class Node:
    def __init__(self, word):
        self.word = word
        self.left = None
        self.right = None


def insert(root, word):
    if root is None:
        return Node(word)

    if word < root.word:
        root.left = insert(root.left, word)
    elif word > root.word:
        root.right = insert(root.right, word)

    return root


def search(root, word):
    if root is None:
        return False

    if word == root.word:
        return True

    if word < root.word:
        return search(root.left, word)

    return search(root.right, word)


def minimum(root):
    while root.left:
        root = root.left
    return root


def delete(root, word):
    if root is None:
        return None

    if word < root.word:
        root.left = delete(root.left, word)

    elif word > root.word:
        root.right = delete(root.right, word)

    else:
        if root.left is None:
            return root.right

        if root.right is None:
            return root.left

        successor = minimum(root.right)
        root.word = successor.word
        root.right = delete(root.right, successor.word)

    return root


def inorder(root):
    if root:
        inorder(root.left)
        print(root.word)
        inorder(root.right)


root = None

for word in ["mango", "apple", "orange",
             "banana", "grape"]:
    root = insert(root, word)

print("Before deletion:")
inorder(root)

print("Search mango:", search(root, "mango"))

root = delete(root, "mango")

print("After deleting mango:")
inorder(root)

#Perform 100,000 random searches in Trie, BST, and Dictionary and compare their execution times.

import random
import time
from bisect import bisect_left

words = [
    "apple", "banana", "cherry", "date",
    "grape", "mango", "orange", "pear"
]

dictionary = {word: True for word in words}
trie_words = set(words)
sorted_words = sorted(words)

random.seed(42)
queries = [
    random.choice(words) for _ in range(100_000)
]


def binary_search(items, target):
    position = bisect_left(items, target)

    return (
        position < len(items)
        and items[position] == target
    )


def measure(name, search_function):
    start = time.perf_counter()

    for word in queries:
        search_function(word)

    elapsed = time.perf_counter() - start
    print(f"{name}: {elapsed:.6f} seconds")


measure("Dictionary", lambda word: word in dictionary)
measure("Set lookup", lambda word: word in trie_words)
measure("Binary search", lambda word: binary_search(sorted_words, word))

#Read a file, build three indexes, and compare construction, search, and printing times using a graph
import time
import random
import matplotlib.pyplot as plt

words = [
    "apple", "banana", "cherry",
    "apple", "date", "banana"
]

# Construction
results = {}

start = time.perf_counter()
trie_index = {}
for word in words:
    trie_index.setdefault(word, []).append(word)
results["Dictionary"] = {"construction":
                         time.perf_counter() - start}

start = time.perf_counter()
bst_index = set()
for word in words:
    bst_index.add(word)
results["BST-like set"] = {"construction":
                           time.perf_counter() - start}

start = time.perf_counter()
trie_words = {}
for word in words:
    trie_words[word] = True
results["Trie-like map"] = {"construction":
                            time.perf_counter() - start}

queries = [
    random.choice(words) for _ in range(100_000)
]

search_functions = {
    "Dictionary": lambda w: w in trie_index,
    "BST-like set": lambda w: w in bst_index,
    "Trie-like map": lambda w: w in trie_words
}

for name, search_fn in search_functions.items():
    start = time.perf_counter()

    for word in queries:
        search_fn(word)

    results[name]["search"] = time.perf_counter() - start

methods = list(results)
construction = [results[m]["construction"] for m in methods]
search = [results[m]["search"] for m in methods]

plt.plot(methods, construction, marker="o",
         label="Construction")
plt.plot(methods, search, marker="s",
         label="100,000 searches")

plt.xlabel("Method")
plt.ylabel("Time in seconds")
plt.title("Index Performance Comparison")
plt.legend()
plt.tight_layout()
plt.show()
#Find all words beginning with a given prefix in a text-file index.
import re

index = {}
separators = re.compile(r"[ \t\r\n\f\v.,:;]+")

with open("input.txt", "r") as file:
    for line_no, line in enumerate(file, 1):
        for word in separators.split(line.strip()):
            if word:
                index.setdefault(word, []).append(line_no)

prefix = input("Enter prefix: ")

found = False

for word in sorted(index):
    if word.startswith(prefix):
        print(word, ":", index[word])
        found = True

if not found:
    print("No matching words found")
#Identify and fix the errors in a word-indexing program.
index = {}

with open("input.txt", "r") as file:
    for line_no, line in enumerate(file):
        for word in line.split():
            index[word] = line_no

for word in sorted(index):
    print(word, index[word])
