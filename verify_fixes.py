import re

def check_file(filename):
    print(f"Checking {filename}...")
    with open(filename, 'r') as f:
        content = f.read()
    
    # Check for margin usage
    margin_count = content.count("margin=(20, 20)") + content.count("margin=(10, 10)")
    print(f"  - Margin parameters found: {margin_count}")
    
    # Check for increased spacing in Slide 2
    slide2_spacing = re.search(r"y_pos \+= 220", content)
    slide2_offset = re.search(r"y_pos \+ 90", content)
    
    if slide2_spacing:
        print(f"  - Slide 2 item spacing increased to 220: YES")
    else:
        print(f"  - Slide 2 item spacing increased to 220: NO")
        
    if slide2_offset:
        print(f"  - Slide 2 meaning offset increased to 90: YES")
    else:
        print(f"  - Slide 2 meaning offset increased to 90: NO")

    # Check for increased spacing in Slide 3
    slide3_spacing = re.search(r"y_pos \+= 200", content)
    slide3_offset = re.search(r"y_pos \+ 80", content)
    
    if slide3_spacing:
        print(f"  - Slide 3 item spacing increased to 200: YES")
    else:
        print(f"  - Slide 3 item spacing increased to 200: NO")
        
    if slide3_offset:
        print(f"  - Slide 3 meaning offset increased to 80: YES")
    else:
        print(f"  - Slide 3 meaning offset increased to 80: NO")

check_file('video_generator.py')
check_file('generate_special_video.py')
