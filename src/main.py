from textnode import TextNode
from htmlnode import HTMLNode

def main():
    #Dummy_test = TextNode('This is a text node', 'bold', 'https://www.boot.dev')
    #print(repr(Dummy_test))
    Dummy_HTML_test = HTMLNode('h1','title',None,None)
    print(repr(Dummy_HTML_test))


if __name__ == "__main__":
	main()