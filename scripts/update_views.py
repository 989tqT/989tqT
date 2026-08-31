import urllib.request
import re
import os

SVG_PATH = 'src/b_1.svg'

def get_current_count_from_svg():
    # read existing count from svg so api failure never corrupts the display
    try:
        with open(SVG_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        m = re.search(r'id="visitorCount">([^<]*)</tspan>', content)
        if m:
            return m.group(1).strip()
    except Exception:
        pass
    return "0"

def get_views():
    url = "https://komarev.com/ghpvc/?username=989tqT"
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            svg_data = response.read().decode('utf-8')
            matches = re.findall(r'<text[^>]*>([^<]+)</text>', svg_data)
            if matches:
                count_str = matches[-1].strip()
                if any(c.isdigit() for c in count_str):
                    return count_str
    except Exception as e:
        print(f"komarev fetch failed: {e}")

    # fallback: keep whatever is already in the svg (no corruption)
    fallback = get_current_count_from_svg()
    print(f"both apis failed, keeping current value: {fallback}")
    return fallback

def update_svg():
    count = get_views()
    print(f"visitor count: {count}")

    if not os.path.exists(SVG_PATH):
        print(f"svg not found at {SVG_PATH}")
        return

    with open(SVG_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = re.sub(
        r'id="visitorCount">[^<]*</tspan>',
        f'id="visitorCount">{count}</tspan>',
        content
    )

    with open(SVG_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("svg updated.")

if __name__ == '__main__':
    update_svg()