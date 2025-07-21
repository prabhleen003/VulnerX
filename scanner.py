import requests

HEADERS = {'User-Agent': 'Mozilla/5.0 (VulnScanner)'}

def scan_sql_injection(url):
    res = []
    for p in ["'", "' OR '1'='1", '" OR "1"="1']:
        u = f"{url}?id={p}"
        try:
            r = requests.get(u, headers=HEADERS, timeout=10)
            if any(e in r.text.lower() for e in ['sql syntax', 'mysql', 'syntax error']):
                res.append(('error', f"Possible SQL Injection at {u}"))
            else:
                res.append(('info', f"No SQLi at {u}"))
        except Exception as ex:
            res.append(('warning', f"Error at {u}: {ex}"))
    return res

def scan_xss(url):
    p = "<script>alert('XSS')</script>"
    u = f"{url}?q={p}"
    try:
        r = requests.get(u, headers=HEADERS, timeout=10)
        if p in r.text:
            return [('error', f"Possible XSS at {u}")]
        return [('info', f"No XSS at {u}")]
    except Exception as ex:
        return [('warning', f"Error at {u}: {ex}")]

def scan_path_traversal(url):
    u = f"{url}?file=../../etc/passwd"
    try:
        r = requests.get(u, headers=HEADERS, timeout=10)
        if "root:x:" in r.text:
            return [('error', f"Possible Path Traversal at {u}")]
        return [('info', f"No Path Traversal at {u}")]
    except Exception as ex:
        return [('warning', f"Error at {u}: {ex}")]

def scan_directory_listing(base):
    res = []
    paths = ['/', '/uploads/', '/files/', '/backup/', '/images/']
    for p in paths:
        u = base.rstrip('/') + p
        try:
            r = requests.get(u, headers=HEADERS, timeout=10)
            if "Index of /" in r.text:
                res.append(('error', f"Directory listing ENABLED at {u}"))
            else:
                res.append(('info', f"Directory listing NOT enabled at {u}"))
        except Exception as ex:
            res.append(('warning', f"Error at {u}: {ex}"))
    return res

