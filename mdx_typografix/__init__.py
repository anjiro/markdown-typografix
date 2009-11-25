# -*- coding: utf-8 -*-
import markdown
import re

def makeExtension(configs=None) :
    return TypografixExtension(configs=configs)
    
def is_block(node):
    return node.tag not in (
        'a', 'abbr', 'acronym', 'address',
        'b', 'bdo', 'big', 'br', 'button',
        'caption', 'cite', 'code',
        'del', 'dfn', 'em',
        'i', 'img', 'input', 'ins',
        'kbd', 'label', 'legend', 'q',
        's', 'samp', 'script', 'small', 'span',
        'strike', 'strong', 'sub', 'sup',
        'tt', 'u', 'var')
    
class TypografixExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        md.treeprocessors.add('typografix', TypografixProcessor(), '_end')
    
class TypografixProcessor(markdown.treeprocessors.Treeprocessor):
    def fix_text(self, node, attr, fix_widow):
        text = getattr(node, attr)
        if not text:
            return None
        nbsp = u'\xa0'
        output = []
        splitter = re.compile(ur'\s*(\.\.\.|---|--|[\s.,;!?:"«»([)\]-])\s*')
        parts = splitter.split(text)
        for i in range(0, len(parts)-2, 2):
            before, sep, after = parts[i], parts[i+1], parts[i+2]

            if len(before):
                output.append(before)
                
            if sep == '...':
                sep = u'\u2026' # ellipsis
            elif sep == '---':
                sep = u'\u2014' # em dash
            elif sep == '--':
                sep = u'\u2013' # en dash
            elif sep == '"':
                if self.odd_quote:
                    sep = u'»'
                else:
                    sep = u'«'
            elif sep in '\t\n\r\f\v':
                sep = ' '
            
            if sep == u'«':
                self.odd_quote = True
            elif sep == u'»':
                self.odd_quote = False
            
            if sep in u';!?:»':
                output.append(nbsp)
            elif sep in u'«([\u2014\u2013':
                output.append(' ')
            
            if sep != ' ' or len(after) or len(before):
                output.append(sep)
            
            if len(after):
                if sep in u'.,;!?:»)]\u2026\u2014\u2013':
                    output.append(' ')
                elif sep in u'«':
                    output.append(nbsp)
        
        if len(parts[-1]):
            output.append(parts[-1])

        last_cut = None
        own_cuts = 0
        for i in range(len(output)):
            if output[i] == ' ':
                own_cuts += 1
                last_cut = i
        self.cuts += own_cuts
        if fix_widow and self.cuts > 1 :
            if own_cuts == 0:
                self.previous_output[self.previous_last_cut] = nbsp
                setattr(self.previous_node, self.previous_attr, ''.join(self.previous_output))
                pass
            else:
                output[last_cut] = nbsp
                
        if own_cuts > 0:
            self.previous_output = output
            self.previous_last_cut = last_cut
            self.previous_node = node
            self.previous_attr = attr
            
        setattr(node, attr, ''.join(output))
        
    def run(self, node, can_fix_widow=True):
        self.odd_quote = False
        if is_block(node):
            self.cuts = 0
        children = node.getchildren()
        tail_is_empty = (not node.tail or len(node.tail.strip('\t\n\r\f\v')) == 0)
        if len(children) == 0:
            self.fix_text(node, 'text', tail_is_empty and can_fix_widow)
        else:
            self.fix_text(node, 'text', is_block(children[0]))
            for i in range(len(children)-1):
                self.run(children[i], is_block(children[i+1]))
            self.run(children[-1], tail_is_empty and can_fix_widow)
        if is_block(node):
            self.cuts = 0
        self.fix_text(node, 'tail', can_fix_widow)
        return node

