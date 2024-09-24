

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value 
        self.children = children
        self.props = props 

    def to_html(self):
        raise NoImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        props_list = "".join([f' {key}="{value}"' for (key, value) in self.props.items()])      
        return props_list

    
    def __repr__(self):
        return f"HTMLNode: {self.tag}, {self.value}, {self.children}, {self.props}"


class LeafNode(HTMLNode):
    def __init__(self, tag, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("No value")
        if self.tag == None:
            return self.value
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()}/>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>" 
    def __repr__(self):
        return f"LeafNode: {self.tag}, {self.value}, {self.props}"

class ParentNode(HTMLNode):
    def __init__(self, tag, children):
        super().__init__(tag, None, children, None)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")
        if self.children is None:
            raise ValueError("Invalid HTML: No children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
            
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"


