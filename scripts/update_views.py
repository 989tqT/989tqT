import urllib.request
import re
import os

def get_views():
    url = "https://komarev.com/ghpvc/?username=989tqT"
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            svg_data = response.read().decode('utf-8')
            matches = re.findall(r'<text[^>]*>([^<]+)</text>', svg_data)
            if matches:
                count_str = matches[-1].strip()
                if any(char.isdigit() for char in count_str):
                    return count_str
    except Exception as e:
        print(f"Error fetching from Komarev: {e}")
    
    url_u8 = "https://u8views.com/api/v1/github/profiles/989tqT/views/day-week-month-total-count.svg"
    req_u8 = urllib.request.Request(
        url_u8, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    try:
        with urllib.request.urlopen(req_u8) as response:
            svg_data = response.read().decode('utf-8')
            matches = re.findall(r'<text[^>]*>([^<]+)</text>', svg_data)
            if matches:
                count_str = matches[-1].strip()
                return count_str
    except Exception as e:
        print(f"Error fetching from u8views: {e}")
        
    return "1,337"  

def update_svg():
    count = get_views()
    print(f"Current visitors count: {count}")
    
    svg_path = 'src/b_1.svg'
    if not os.path.exists(svg_path):
        svg_path = 'o:/etc/me/989tqT/src/b_1.svg'
        
    with open(svg_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    new_content = re.sub(
        r'id="visitorCount">[^<]*</tspan>',
        f'id="visitorCount">{count}</tspan>',
        content
    )
    
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print("Successfully updated visitors count!")

if __name__ == '__main__':
    update_svg()