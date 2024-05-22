import re

paragraph = """To determine the color seasons of each hexadecimal color code, let's analyze them individually:

1. #BF3A30:
   - This color is a rich, deep red with a slight brown undertone.
   - It aligns well with the Autumn palette due to its warm and deep tones.

2. #C68176:
   - This color is a muted, warm pink with a touch of brown.
   - It also fits within the Autumn palette, featuring warm and earthy tones.

3. #B97271:
   - Another warm color, this time leaning towards a dusty rose or muted terracotta.
   - It continues to align with the Autumn palette's range of warm, earthy hues.

4. #623343:
   - This color is deep and rich, with strong red undertones leaning towards brown.
   - Similar to the first color, it fits well within the Autumn palette's range of deep, earthy tones.

5. #CF8D98:
   - This color is a soft, muted pink with cool undertones.
   - It aligns with the cool and light tones typically found in the Summer palette.

Based on this analysis:
- #BF3A30, #C68176, #B97271, and #623343 correspond to the Autumn color palette.
- #CF8D98 corresponds to the Summer color palette."""

# Splitting the paragraph into two parts based on the last sentence
split_paragraph = paragraph.split("Based on this analysis:")

# Displaying the split paragraph
print("First part:")
print(split_paragraph[0])
print("\nSecond part:")
print("Based on this analysis:" + split_paragraph[1])

analysis = split_paragraph[1]

# Extract color-season pairs
color_season_pairs = re.findall(r'#(?:[0-9a-fA-F]{3}){1,2}\b|\bAutumn\b|\bSummer\b|\bSpring\b|\bWinter\b', analysis)

# Create a dictionary to store color codes for each season
season_color_mapping = {'Autumn': [], 'Summer': [], 'Spring': [], 'Winter': []}

# Iterate through pairs and update the color mapping
current_colors = []
for item in color_season_pairs:
    if item.startswith("#"):
        current_colors.append(item.lstrip('#'))
    else:
        if current_colors:
            season_color_mapping[item] = current_colors
            current_colors = []

# Print output
for season, color_codes in season_color_mapping.items():
    if color_codes:
        print(f"{season}: {', '.join(['#' + color_code for color_code in color_codes])}")
    else:
        print(f"{season}: None")
