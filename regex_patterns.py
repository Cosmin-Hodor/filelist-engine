import re

# Regular Expression Patterns
RE_PATTERNS = {
    'validator': re.compile(r"name='validator'\svalue='(.*?)'\s\/>"),
    'all_results': re.compile(r"<div\sclass='torrentrow'>[\S\s]*?<div\sclass='clearfix'><\/div>\s*<\/div>"),
    'id': re.compile(r"id=(\d+)"),
    'name': re.compile(r"title='(.*?)'"),
    'size': re.compile(r"<font\sclass='small'>([\d.]+)<br\s\/>(\w+)"),
    'seeders': re.compile(r"<font\scolor=\#\w{6}>(\d+)"),
    'leechers': re.compile(r"vertical-align:middle;display:table-cell;'><b>(\d+)"),
    'next_page': re.compile(r"<a href='\?search=[\S]+<font class='small'>&raquo;")
}