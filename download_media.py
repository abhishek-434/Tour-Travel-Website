import os
import urllib.request

# Ensure target directories exist
os.makedirs('media/destinations', exist_ok=True)
os.makedirs('media/packages', exist_ok=True)
os.makedirs('media/blog', exist_ok=True)
os.makedirs('media/gallery', exist_ok=True)

IMAGES = {
    'media/destinations/bali.jpg': 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=800&q=80',
    'media/destinations/swiss.jpg': 'https://images.unsplash.com/photo-1486916856992-e4db22c8df33?auto=format&fit=crop&w=800&q=80',
    'media/destinations/kenya.jpg': 'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?auto=format&fit=crop&w=800&q=80',
    'media/packages/pkg_bali.jpg': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?auto=format&fit=crop&w=800&q=80',
    'media/packages/pkg_swiss.jpg': 'https://images.unsplash.com/photo-1502784444187-359ac186c5bb?auto=format&fit=crop&w=800&q=80',
    'media/packages/pkg_kenya.jpg': 'https://images.unsplash.com/photo-1516426122078-c23e76319801?auto=format&fit=crop&w=800&q=80',
    'media/blog/blog_safari.jpg': 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=800&q=80',
    'media/blog/blog_budget.jpg': 'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=800&q=80',
    'media/gallery/g_1.jpg': 'https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?auto=format&fit=crop&w=800&q=80',
    'media/gallery/g_2.jpg': 'https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?auto=format&fit=crop&w=800&q=80',
    'media/gallery/g_3.jpg': 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=800&q=80',
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

print("Downloading high-quality travel images from Unsplash...")
for path, url in IMAGES.items():
    try:
        print(f"Downloading {path}...")
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response, open(path, 'wb') as out_file:
            out_file.write(response.read())
        print(f"-> Saved: {path}")
    except Exception as e:
        print(f"-> Error downloading {path}: {e}")

print("Media setup finished.")
