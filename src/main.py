from textnode import TextNode
from htmlnode import HTMLNode
from htmlnode import LeafNode

def main():
    leaf = LeafNode("a","This is a link", {
            "href": "https://www.google.com",
            "target": "_blank",
        })
    leaf2 = '<a href="https://www.google.com" target="_blank">This is a link</a>'
    print(f"Got:      {repr(leaf.to_html())}")
    print(f"Expected: {repr(leaf2)}")

    print("Length of got:", len(leaf.to_html()))
    print("Length of expected:", len(leaf2))
    print("Strings equal?:", leaf.to_html() == leaf2)

# Compare character by character
    got = leaf.to_html()
    for i, (c1, c2) in enumerate(zip(got, leaf2)):
        if c1 != c2:
            print(f"Difference at position {i}: {repr(c1)} vs {repr(c2)}")

if __name__ == "__main__":
	main()