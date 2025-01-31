import unittest
from delimiter import extract_markdown_images, extract_markdown_links

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
    
    def test_extract_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_extract_img_plain_text(self):
        text = "This is plain text with no markdown"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])
    
    def test_extract_link_plain_text(self):
        text = "This is plain text with no markdown"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])
    
    def test_extract_img_with_link(self):
        text = "This is a link [to google](https://google.co.uk)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_extract_link_with_img(self):
        text = "This is a img ![to google](https://google.co.uk)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])
    
    def test_extract_link_and_img(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        result2 = extract_markdown_images(text)
        self.assertEqual(result, [("to boot dev", "https://www.boot.dev")])
        self.assertEqual(result2, [("to youtube", "https://www.youtube.com/@bootdotdev")])

if __name__ == "__main__":
    unittest.main()