class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        
        prop_string = ""
        for key in sorted(self.props.keys()):
            value = self.props[key]
            prop_string += f' {key}="{value}"'
        
        return prop_string
    
    def __repr__(self):
        children_preview = f"{len(self.children)} children" if self.children else "no children"
        props_preview = f"{len(self.props)} props" if self.props else "no props"
        
        return f"HTMLNode({self.tag}, {self.value}, {children_preview}, {props_preview})"
    
    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, [], props)
        
    def to_html(self):
        if not self.value:
            raise ValueError
        
        if not self.tag:
            return self.value
                
        html_render = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
        return html_render