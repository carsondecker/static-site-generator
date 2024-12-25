from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag=tag, children=children, props=props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("No tag on parent node.")
        if self.children == None:
            raise ValueError("No children on parent node.")
        
        return f"<{self.tag}{self.props_to_html()}>{self.__to_html_helper(self.children)}</{self.tag}>"
        
    def __to_html_helper(self, child_list):
        if len(child_list) == 0:
            return ""
        return child_list[0].to_html() + self.__to_html_helper(child_list[1:])