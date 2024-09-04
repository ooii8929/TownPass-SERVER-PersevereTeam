import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

def safe_extract(lst, index, default=''):
    try:
        return lst[index].strip()
    except IndexError:
        return default

def scrape_artwork_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    content_div = soup.find('div', class_='editorPanel --right content')
    
    if not content_div:
        return None
    
    # Extract all paragraphs
    paragraphs = content_div.find_all('p')
    
    # Extract artist info
    artist_info = paragraphs[1].text.strip().split('\n') if len(paragraphs) > 1 else []
    artist_name = safe_extract(artist_info, 0)
    artist_name_en = safe_extract(artist_info, 1)
    artist_years = safe_extract(artist_info, 2)
    
    # Extract artwork info
    artwork_info = paragraphs[1].text.strip().split('\n') if len(paragraphs) > 1 else []
    artwork_title = safe_extract(artwork_info, 4)
    artwork_title_en = safe_extract(artwork_info, 5)
    artwork_year = safe_extract(artwork_info, 6)
    artwork_medium = safe_extract(artwork_info, 7)
    artwork_collection = safe_extract(artwork_info, 8)
    artwork_id = safe_extract(artwork_info, 9)
    
    # Extract description
    description_elem = content_div.find('span', class_='fc-text')
    description = description_elem.text.strip() if description_elem else ''
    
    # Create a dictionary with the extracted information
    artwork_data = {
        "artist": {
            "name": artist_name,
            "name_en": artist_name_en,
            "years": artist_years
        },
        "artwork": {
            "title": artwork_title,
            "title_en": artwork_title_en,
            "year": artwork_year,
            "medium": artwork_medium,
            "collection": artwork_collection,
            "id": artwork_id
        },
        "description": description
    }
    
    return artwork_data

def scrape_all_artworks(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all artist list items
    artist_items = soup.find_all('div', class_='artistList-item')
    
    all_artworks = []
    
    for item in artist_items:
        # Extract the artist name
        artist_name = item.find('h6').text.strip()
        
        # Extract the link
        link = urljoin(url, item.find('a')['href'])
        
        # Scrape detailed information for this artwork
        artwork_info = scrape_artwork_info(link)
        
        if artwork_info:
            artwork_info['page_url'] = link
            all_artworks.append(artwork_info)
        
        print(f"Processed: {artist_name}")
    
    return all_artworks

# URL of the main page with all artworks
main_url = "https://www.chimeimuseum.org/special-exhibition/65812c83b6dc6/65d4062828005"

# Scrape information for all artworks
all_artwork_info = scrape_all_artworks(main_url)

if all_artwork_info:
    # Convert the data to JSON
    json_data = json.dumps(all_artwork_info, ensure_ascii=False, indent=2)

    # Print the JSON data
    print(json_data)

    # Save the JSON data to a file
    with open('all_artwork_info.json', 'w', encoding='utf-8') as f:
        json.dump(all_artwork_info, f, ensure_ascii=False, indent=2)
    
    print(f"Scraped information for {len(all_artwork_info)} artworks.")
else:
    print("Failed to scrape artwork information.")