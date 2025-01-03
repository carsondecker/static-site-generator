from functools import reduce

class HTMLNode:
    def __init__(self, tag=None, value="", children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("HTML node's to_html method is not implemented.")
    
    def props_to_html(self):
        if self.props == None:
            return ""
        res = ""
        for k, v in self.props.items():
            res += f" {k}=\"{v}\""
        return res
    
    def __repr__(self):
        return f"HTMLNode(tag=\"{self.tag}\", value=\"{self.value}\", children=\"{self.children}\", props=\"{self.props_to_html()}\")"