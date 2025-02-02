class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    # Defined method for child classes to overwrite, with default error for failed implementation for inherited classes.
    def to_html(self):
        if self.tag is None:
            if self.value is not None:
                return self.value
            if self.children:
                return "".join(child.to_html() for child in self.children)
            return ""
        
        result = f"<{self.tag}>"

        if self.value:
            if isinstance(self.value, HTMLNode):
                result += self.value.to_html()
            else:
                result += self.value

        if self.children:
            for child in self.children:
                result += child.to_html()
        
        result += f"</{self.tag}>"

        return result
    
    # Formats the props receieved from a node. With the necessary spacing. Props is a dictionary, needs converted to string.
    def props_to_html(self):
        # Returns empty string from empty dictionary.
        if not self.props:
            return ""
        
        # Iterates through sorted dictionary keys and creates (and extends) the string. Sorted to preserve consistent ordering.
        prop_string = ""
        for key in sorted(self.props.keys()):
            value = self.props[key]
            prop_string += f' {key}="{value}"'
        
        return prop_string
    
    # When method is called to display simplifies the manner of the return.
    def __repr__(self):
        children_preview = f"{len(self.children)} children" if self.children else "no children"
        props_preview = f"{len(self.props)} props" if self.props else "no props"
        
        return f"HTMLNode({self.tag}, {self.value}, {children_preview}, {props_preview})"
    
    # Checks equality of object properties to check if objects are the same c.f., memory location.
    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

# Lead node is a node without children i.e., not a list etc.
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, [], props)

    # Convert Leafnode to HTML string. Checks that is has a value as all leaf nodes must.
    def to_html(self):
        if self.value is None:
            raise ValueError(f"{self.tag} and props: {self.props}")
        # If no tag, then the line is just standard text and returns the value only.
        if not self.tag:
            return self.value
        
        # Render calls propr_to_html to convert the non-required dictionary of props to suitable string.
        html_render = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return html_render


# Parent node is the opposite, it has no value, only has children and the relevant tags.
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    # Must have a tag to convert to html string.
    def to_html(self):
        if not self.tag:
            raise ValueError
        
        # Checks to see if there are children, children are passed through as a list of nodes. Check both None and erroneous empty list.
        if self.children == None or self.children == []:
            raise ValueError("Parent node must have children")
        
        # Potentially recurssively calls the to_html method on the children to convert into strings which are then embedded.
        children_html = ""
        for child in self.children:
                children_html += child.to_html()

        parent_render = f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
        return parent_render