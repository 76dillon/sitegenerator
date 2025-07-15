from textnode import TextNode, TextType

def main():
    text_type = TextType.IMAGE
    print(TextNode("this is some text", text_type, "http://yomama.com"))

if __name__ == "__main__":
    main()