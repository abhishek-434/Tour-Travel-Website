import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tour_travel.settings')
django.setup()

from core.models import GalleryImage

gallery_items = [
    {
        'image': 'gallery/cappadocia_valley.jpg',
        'caption': 'Drifting at Dawn Over Göreme Fairy Chimneys',
        'tourist_name': 'Sebastian & Mia Cruz',
        'location': 'Cappadocia, Turkey'
    },
    {
        'image': 'gallery/amalfi_coast.jpg',
        'caption': 'Terracotta Cliffs & Lemon Groves of Positano',
        'tourist_name': 'Lady Eleanor Kensington',
        'location': 'Amalfi Coast, Italy'
    },
    {
        'image': 'gallery/kyoto_temple.jpg',
        'caption': 'Quiet Reflection at Yasaka Pagoda',
        'tourist_name': 'Kenji & Sarah Sato',
        'location': 'Kyoto, Japan'
    },
    {
        'image': 'gallery/patagonia_glacier.jpg',
        'caption': 'Granite Horns of Torres del Paine',
        'tourist_name': 'Mateo Fernandez',
        'location': 'Patagonia, Chile'
    },
    {
        'image': 'gallery/santorini_sunset.jpg',
        'caption': 'Golden Hour Across the Aegean Caldera',
        'tourist_name': 'Elena Rostova',
        'location': 'Oia, Santorini'
    },
    {
        'image': 'gallery/morocco_riad.jpg',
        'caption': 'Hand-Carved Stucco in a Courtyard Riad',
        'tourist_name': 'Camille Laurent',
        'location': 'Marrakech, Morocco'
    },
    {
        'image': 'gallery/dolomites_lakes.jpg',
        'caption': 'Still Waters of Lago di Braies at Sunrise',
        'tourist_name': 'Lukas Weber',
        'location': 'Dolomites, Italy'
    },
    {
        'image': 'gallery/iceland_aurora.jpg',
        'caption': 'Dancing Northern Lights Over Black Sand Beaches',
        'tourist_name': 'Dr. Henrik Lindqvist',
        'location': 'Vík, Iceland'
    },
    {
        'image': 'gallery/maldives_villa.jpg',
        'caption': 'Timber Overwater Sanctuary & Coral Reefs',
        'tourist_name': 'Victoria Sterling',
        'location': 'Baa Atoll, Maldives'
    },
    {
        'image': 'gallery/swiss_chalet.jpg',
        'caption': 'Wildflower Meadows Beneath the High Alps',
        'tourist_name': 'Marcus Thorne',
        'location': 'Grindelwald, Switzerland'
    },
    {
        'image': 'gallery/vietnam_halong.jpg',
        'caption': 'Limestone Pillars in Emerald Waters',
        'tourist_name': 'Li Wei & Amanda Chen',
        'location': 'Ha Long Bay, Vietnam'
    },
    {
        'image': 'gallery/peru_machupicchu.jpg',
        'caption': 'Morning Clouds Lifting from the Sun Gate',
        'tourist_name': 'Carlos Mendoza',
        'location': 'Cusco & Machu Picchu, Peru'
    },
    {
        'image': 'gallery/norway_fjords.jpg',
        'caption': 'Cascading Waterfalls of Geirangerfjord',
        'tourist_name': 'Freja Nygård',
        'location': 'Sunnmøre, Norway'
    },
    {
        'image': 'destinations/elephant.jpg',
        'caption': 'Gentle Giants Crossing the Mara at Sunset',
        'tourist_name': "Dr. David O'Connor",
        'location': 'Masai Mara, Kenya'
    },
    {
        'image': 'gallery/paris.png',
        'caption': 'Autumn Twilight over the Pont Alexandre III',
        'tourist_name': 'Julien Moreau',
        'location': 'Paris, France'
    },
    {
        'image': 'gallery/rome.jpg',
        'caption': 'The Colosseum Travertine Bathed in Dawn Gold',
        'tourist_name': 'Marcus Vance',
        'location': 'Rome, Italy'
    },
    {
        'image': 'gallery/barcelona.jpg',
        'caption': 'Stained Glass Illumination Inside Sagrada Família',
        'tourist_name': 'Clara Fernandez',
        'location': 'Barcelona, Spain'
    },
    {
        'image': 'gallery/lisbon.jpg',
        'caption': 'Vintage Tram Climbing the Alfama Cobblestones',
        'tourist_name': 'Tiago Silva',
        'location': 'Lisbon, Portugal'
    },
    {
        'image': 'gallery/manali.jpg',
        'caption': 'Ancient Cedar Groves in Morning Himalayan Mist',
        'tourist_name': 'Aarav Sharma',
        'location': 'Himachal Pradesh, India'
    },
    {
        'image': 'gallery/bali.jpg',
        'caption': 'Emerald Terraces of Tegallalang',
        'tourist_name': 'Sophia Thorne',
        'location': 'Ubud, Bali'
    },
]

GalleryImage.objects.all().delete()
for item in gallery_items:
    GalleryImage.objects.create(**item)

count = GalleryImage.objects.count()
print(f"Successfully added {count} authentic gallery images!")

