
import matplotlib.pyplot as plt

# Number of distinct words used in the experiments
sizes = [1000, 5000, 10000, 50000, 100000, 500000]

# EXAMPLE DATA ONLY: replace with actual measured times

# Graph 1: Construction time (seconds)
trie_build = [0.01, 0.05, 0.11, 0.65, 1.30, 7.20]
bst_build = [0.01, 0.06, 0.13, 0.80, 1.70, 9.50]
dict_build = [0.005, 0.02, 0.04, 0.25, 0.50, 2.60]

# Graph 2: Search time for 100,000 random words (seconds)
trie_search = [0.02, 0.03, 0.04, 0.05, 0.06, 0.08]
bst_search = [0.02, 0.03, 0.04, 0.06, 0.08, 0.12]
dict_search = [0.01, 0.02, 0.02, 0.03, 0.04, 0.06]

# Graph 3: Lexicographic printing time (seconds)
trie_print = [0.01, 0.05, 0.10, 0.60, 1.20, 6.00]
bst_print = [0.01, 0.04, 0.09, 0.50, 1.00, 5.00]
dict_print = [0.01, 0.04, 0.08, 0.45, 0.90, 4.50]


def draw_graph(title, trie, bst, dictionary, filename):
    plt.figure(figsize=(9, 5))

    plt.plot(sizes, trie, marker="o", label="Trie")
    plt.plot(sizes, bst, marker="s", label="BST")
    plt.plot(sizes, dictionary, marker="^",
             label="Dictionary")

    plt.title(title)
    plt.xlabel("Number of distinct words")
    plt.ylabel("Execution time (seconds)")
    plt.xscale("log")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()

    # Save the graph as an image
    plt.savefig(filename, dpi=300)
    plt.show()
    plt.close()


# Graph 1
draw_graph(
    "Index Construction Time",
    trie_build,
    bst_build,
    dict_build,
    "construction_graph.png"
)

# Graph 2
draw_graph(
    "Search Time for 100,000 Random Words",
    trie_search,
    bst_search,
    dict_search,
    "search_graph.png"
)

# Graph 3
draw_graph(
    "Lexicographic Index Printing Time",
    trie_print,
    bst_print,
    dict_print,
    "printing_graph.png"
)

print("All three graphs generated successfully!")
print("1. construction_graph.png")
print("2. search_graph.png")
print("3. printing_graph.png")
