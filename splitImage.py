from bs4 import BeautifulSoup

# Sample HTML content
html_content = """
<li class="active" selected="" soldout="" title="#03" onmouseover="relatedOption(79355)" onmouseout="relatedOption(79355)">
    <a href="javascript:;" onclick="ky.loading();window.location.replace('https://www.konvy.com/4u2/4u2-for-you-too-shimmer-blush-5g-03-bride-to-be-79355.html')" title="#03" class="ky-d ky-pointer">
        <img class="ky-w100" src="https://s2.konvy.com/static/team_related/2023/0217/16766003492328.jpg" alt="#03">
    </a>
</li>
<li soldout="" title="#04" onmouseover="relatedOption(79356)" onmouseout="relatedOption(79355)">
    <a href="javascript:;" onclick="ky.loading();window.location.replace('https://www.konvy.com/4u2/4u2-for-you-too-shimmer-blush-5g-04-light-espresso-79356.html')" title="#04" class="ky-d ky-pointer">
        <img class="ky-w100" src="https://s2.konvy.com/static/team_related/2023/0217/16766003488982.jpg" alt="#04">
    </a>
</li>
<li soldout="" title="#07" onmouseover="relatedOption(79359)" onmouseout="relatedOption(79355)">
    <a href="javascript:;" onclick="ky.loading();window.location.replace('https://www.konvy.com/4u2/4u2-for-you-too-shimmer-blush-5g-07-soft-mood-79359.html')" title="#07" class="ky-d ky-pointer">
        <img class="ky-w100" src="https://s2.konvy.com/static/team_related/2023/0217/16766003433924.jpg" alt="#07">
    </a>
</li>
<li soldout="" title="#09" onmouseover="relatedOption(79361)" onmouseout="relatedOption(79355)">
    <a href="javascript:;" onclick="ky.loading();window.location.replace('https://www.konvy.com/4u2/4u2-for-you-too-shimmer-blush-5g-09-wine-me-79361.html')" title="#09" class="ky-d ky-pointer">
        <img class="ky-w100" src="https://s2.konvy.com/static/team_related/2023/0217/16766003408227.jpg" alt="#09">
    </a>
</li>
"""

# Parse HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Find all img tags within li tags
image_links = [img['src'] for li in soup.find_all('li') for img in li.find_all('img')]

# Print the image links
for link in image_links:
    print(link)
