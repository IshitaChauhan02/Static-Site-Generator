import re

class Page:
    """
    Page class:
        A standard class used for pages. Stores the pages'
        information in the value dict and includes function
        for parsing template.
    """
    def __init__(self, values, template):
        with open(f"app/templates/{template}.html", 'r') as file:
            template_content = file.read()
        
        self.values = {
            'template': template_content
        }
        self.values.update(values)
        self.parsed = ""
        self.html = ""

    def to_template(self):
        self.html = self.values['template']
        self.values['params'] = re.findall(r'\|(.*?)\|', self.html)
        for param in self.values['params']:
            if param in self.values:
                self.html = self.html.replace(f"|{param}|", self.values[param])
        return self.html


class Post(Page):
    """
    Specific Post Class:
        A specific class used for posts. Includes a basic
        markdown parser and the ID (address) of each
        post. Each post should be stored in a custom group
        in order to be repeated.
    """
    def __init__(self, values, template, markdown):
        super().__init__(values, template)
        with open(f"app/md-files/{markdown}", 'r') as file:
            markdown_content = file.read().split("\n")
        
        self.markdown = list(filter(None, markdown_content))
        self.values.update({
            'id': markdown[:-3]
        })
        self.parse_markdown()

    def parse_markdown(self):
        self.values.update({
            'title': self.markdown[0].replace("#" * self.markdown[0].count("#"), "").strip(),
            'date': self.markdown[1].replace("#" * self.markdown[1].count("#"), "").strip(),
            'desc': self.markdown[2],
            'content': ""
        })

        for line in range(len(self.markdown)):
            if self.markdown[line][0] == "#":
                self.values['content'] += "<h{}>{}</h{}>".format(
                    self.markdown[line].count("#"),
                    self.markdown[line].replace("#" * self.markdown[line].count("#"), "").strip(),
                    self.markdown[line].count("#")
                )
            elif self.markdown[line][0] == "!":
                self.values['content'] += '<img src="{}" alt="{}">'.format(
                    re.search(r'\((.*?)\)', self.markdown[line]).group(1),
                    re.search(r'\[(.*?)\]', self.markdown[line]).group(1)
                )
            elif self.markdown[line][0] == "-":
                if line == 0 or self.markdown[line - 1][0] != "-":
                    self.values['content'] += "<ul>"
                self.values['content'] += "<li>{}</li>".format(self.markdown[line][1:].strip())
                if line == len(self.markdown) - 1 or self.markdown[line + 1][0] != "-":
                    self.values['content'] += "</ul>"
            else:
                line_content = self.markdown[line]
                if re.search(r'\[', line_content):
                    line_content = re.sub(
                        r'\[(.*?)\]\((.*?)\)',
                        r'<a href="\2">\1</a>',
                        line_content
                    )
                if re.search(r'\*\*', line_content):
                    line_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line_content)
                if re.search(r'__', line_content):
                    line_content = re.sub(r'__(.*?)__', r'<strong>\1</strong>', line_content)
                if re.search(r'\*', line_content):
                    line_content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', line_content)
                if re.search(r'_', line_content):
                    line_content = re.sub(r'_(.*?)_', r'<em>\1</em>', line_content)
                self.values['content'] += "<p>{}</p>".format(line_content)

# Example usage (assuming relevant files exist)
# post = Post({'additional': 'value'}, 'template_name', 'markdown_file.md')
# print(post.to_template())
