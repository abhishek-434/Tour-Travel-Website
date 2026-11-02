import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tour_travel.settings')
django.setup()

from django.contrib.auth.models import User
from tours.models import Category, Destination, TourPackage, TourItinerary
from core.models import GalleryImage, Testimonial

def run():
    print("------------------------------------------------------------------")
    print("Populating Wanderlust Boutique Destinations, Packages & Assets...")
    print("------------------------------------------------------------------")

    # 1. Create or Update Admin User 'tour'
    admin_user, created = User.objects.get_or_create(username='tour')
    admin_user.set_password('tour@1234')
    admin_user.email = 'tour@wanderlust.com'
    admin_user.first_name = 'Tour'
    admin_user.last_name = 'Admin'
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.is_active = True
    admin_user.save()
    print(f"-> Admin User 'tour' {'created' if created else 'updated'} with full superuser privileges.")

    # 2. Categories
    cat_luxury, _ = Category.objects.get_or_create(slug='luxury', defaults={'name': 'Luxury Escapes', 'icon': 'bi-gem'})
    cat_cultural, _ = Category.objects.get_or_create(slug='cultural', defaults={'name': 'Cultural', 'icon': 'bi-bank'})
    cat_adventure, _ = Category.objects.get_or_create(slug='adventure', defaults={'name': 'Adventure', 'icon': 'bi-compass'})
    cat_nature, _ = Category.objects.get_or_create(slug='nature', defaults={'name': 'Nature & Wildlife', 'icon': 'bi-tree'})

    # 3. Add 5 New Destinations
    destinations_data = [
        {
            'name': 'Rome & Tuscany, Italy',
            'slug': 'rome-tuscany-italy',
            'hero_image': 'destinations/rome.jpg',
            'description': (
                "From the golden travertine stones of the Colosseum to the rolling cypress hills of the Val d'Orcia, "
                "Rome and Tuscany offer a sensory celebration of classical antiquities, Renaissance villas, "
                "and private biodynamic olive oil estates."
            ),
            'attractions': "Vatican Secret Archives, Roman Forum at Dawn, Val d'Orcia Cypress Roads, Chianti Private Vineyards, San Gimignano Towers",
            'best_time_to_visit': "April to June, September to October",
            'weather_info': "18°C - 26°C, Mild Golden Mediterranean Sun",
            'featured': True,
        },
        {
            'name': 'Barcelona & Costa Brava, Spain',
            'slug': 'barcelona-costa-brava',
            'hero_image': 'destinations/barcelona.jpg',
            'description': (
                "Catalonia pulses with architectural wonder and maritime grace. Wander through Gaudí's radiant stone facades, "
                "savor private tapas tastings in historic Gothic alleys, and retreat to secluded pine-fringed coves along the rugged Costa Brava."
            ),
            'attractions': "Sagrada Família Private Access, Park Güell at Sunset, Gothic Quarter Hidden Patios, Cadaqués Fishing Village, Cap de Creus Coves",
            'best_time_to_visit': "May to June, September to November",
            'weather_info': "20°C - 27°C, Gentle Coastal Breeze",
            'featured': True,
        },
        {
            'name': 'Paris & Loire Valley, France',
            'slug': 'paris-loire-valley',
            'hero_image': 'destinations/paris.png',
            'description': (
                "Parisian romance seamlessly merged with regal Renaissance sanctuaries. Experience private after-hours Louvre access, "
                "artisan perfume workshops in Le Marais, and weekend stays in historic fairytale châteaux flanked by Loire river vineyards."
            ),
            'attractions': "Louvre Private Evening Pass, Château de Chenonceau, Montmartre Secret Vineyards, Seine Wooden Boat Cruise, Sancerre Wine Caves",
            'best_time_to_visit': "April to October",
            'weather_info': "16°C - 24°C, Pleasant Temperate Climate",
            'featured': True,
        },
        {
            'name': 'Lisbon & Sintra, Portugal',
            'slug': 'lisbon-sintra-portugal',
            'hero_image': 'destinations/lisbon.jpg',
            'description': (
                "Bathed in Atlantic golden light, Lisbon captivates with terra-cotta rooftops, hand-painted azulejo tiles, and soulful fado echoes. "
                "Just beyond lies mystical Sintra, where romanticist palaces rise above lush, misty eucalyptus forests."
            ),
            'attractions': "Pena Palace Romanticist Gardens, Alfama Fado Taverns, Belém Tower Sunset, Cabo da Roca Atlantic Cliffs, Quinta da Regaleira",
            'best_time_to_visit': "March to June, September to November",
            'weather_info': "19°C - 26°C, Warm Atlantic Sunshine",
            'featured': True,
        },
        {
            'name': 'Himalayan Foothills & Manali, India',
            'slug': 'himalayan-foothills-manali',
            'hero_image': 'destinations/manali.jpg',
            'description': (
                "Crisp mountain air, towering deodar cedar groves, and ancient timber temples beneath snow-draped Himalayan crests. "
                "A secluded alpine sanctuary tailored for meditative quiet, organic apple orchard stays, and high-altitude valley exploration."
            ),
            'attractions': "Solang Valley Alpine Glades, Naggar Castle & Roerich Estate, Old Manali Cedar Forests, Jogini Waterfall Trails, Rohtang High Pass",
            'best_time_to_visit': "March to June (Blooming Valleys), September to November (Golden Autumn)",
            'weather_info': "10°C - 22°C, Crisp Alpine Climate",
            'featured': True,
        },
    ]

    dest_objects = {}
    for data in destinations_data:
        dest, d_created = Destination.objects.update_or_create(
            slug=data['slug'],
            defaults=data
        )
        dest_objects[data['slug']] = dest
        print(f"-> Destination: {dest.name} ({'Created' if d_created else 'Updated'})")

    # 4. Add 5 Tour Packages
    packages_data = [
        {
            'title': 'Eternal Rome Antiquities & Tuscan Vineyard Retreat',
            'slug': 'rome-tuscany-vineyard-retreat',
            'destination': dest_objects['rome-tuscany-italy'],
            'category': cat_luxury,
            'cover_image': 'packages/rome.jpg',
            'price': 4200.00,
            'discount_price': 3850.00,
            'duration_days': 8,
            'duration_nights': 7,
            'available_seats': 8,
            'difficulty': 'easy',
            'best_season': 'Spring & Autumn',
            'included_services': "7 Nights in 5-star Heritage Villa & Tuscan Estate\nPrivate Chauffeur & VIP Airport Fast-track\nPrivate After-hours Vatican & Colosseum Access\nDaily Farm-to-Table Tuscan Breakfast & 3 Wine Tastings\nDedicated Wanderlust 24/7 Concierge",
            'excluded_services': "International Airfare\nPersonal Shopping and Discretionary Tips",
            'featured': True,
            'is_active': True,
            'itineraries': [
                (1, "Arrival in the Eternal City", "Check-in at our historic palazzo hotel near the Piazza Navona. Welcome aperitivo and rooftop dinner overlooking the Roman domes.", "Private Mercedes-Benz transfer, Rooftop welcome dinner"),
                (2, "Imperial Antiquities at Dawn", "Bypass all public queues for private dawn entry into the Colosseum and Roman Forum led by an esteemed archaeologist.", "Sunrise Forum tour, Private espresso salon"),
                (3, "Journey into the Val d'Orcia", "Scenic chauffeured drive into the rolling Tuscan countryside. Check-in to our converted 17th-century vineyard estate.", "Cypress road photography, Estate wine tasting"),
                (4, "Chianti Vintage Harvesting & Truffle Hunt", "Morning private truffle hunting through oak woodlands followed by a hand-crafted pasta workshop with the estate chef.", "Truffle hunt, Master cooking class, Chianti pairing"),
            ]
        },
        {
            'title': 'Catalonian Modernism & Costa Brava Hidden Coves',
            'slug': 'barcelona-costa-brava-coves',
            'destination': dest_objects['barcelona-costa-brava'],
            'category': cat_cultural,
            'cover_image': 'packages/barcelona.jpg',
            'price': 3450.00,
            'discount_price': 3100.00,
            'duration_days': 7,
            'duration_nights': 6,
            'available_seats': 10,
            'difficulty': 'easy',
            'best_season': 'May to October',
            'included_services': "6 Nights Luxury Boutique Lodgings (Barcelona & Begur)\nPrivate Gaudí Architectural Curator\nChartered Catamaran Cruise with Mediterranean Tapas\nAll Local Organic Winery and Olive Oil Tastings\n100% Carbon-Neutral Travel Offsetting",
            'excluded_services': "International Flights\nPersonal Spa Treatments",
            'featured': True,
            'is_active': True,
            'itineraries': [
                (1, "The Modernist Pulse of Barcelona", "Arrival and private transfer to our boutique hotel in the Eixample district. Sunset stroll and tapas welcome in the Gothic Quarter.", "Private transfer, Gourmet tapas crawl"),
                (2, "Gaudí in Intimate Detail", "Early-access private tour of the Sagrada Família and Casa Batlló with our resident architectural historian.", "Private Sagrada Família pass, Rooftop wine reception"),
                (3, "Coastal Sanctuary in Begur", "Drive along pine-scented coastal roads to Costa Brava. Settle into a clifftop luxury retreat overlooking turquoise waters.", "Scenic coastal transit, Seafood feast"),
                (4, "Chartered Catamaran Secret Coves", "Spend the day sailing secluded coves only reachable by boat. Snorkeling, paddleboarding, and onboard cava lunch.", "Private catamaran charter, Sunset cove anchorage"),
            ]
        },
        {
            'title': 'Parisian Artistry & Loire Fairytale Châteaux',
            'slug': 'paris-loire-valley-chateaux',
            'destination': dest_objects['paris-loire-valley'],
            'category': cat_luxury,
            'cover_image': 'packages/paris.png',
            'price': 4900.00,
            'discount_price': 4500.00,
            'duration_days': 9,
            'duration_nights': 8,
            'available_seats': 6,
            'difficulty': 'easy',
            'best_season': 'April to October',
            'included_services': "8 Nights in 5-Star Paris Boutique Hotel & Private Loire Castle\nVIP Louvre After-Hours Tour & Musée d'Orsay Access\nPrivate High-Speed First-Class Rail Transfers\nDaily Michelin-Caliber Breakfasts & 2 Degustation Dinners\nDedicated French Travel Concierge",
            'excluded_services': "International Airfare\nDiscretionary Gratuities",
            'featured': True,
            'is_active': True,
            'itineraries': [
                (1, "Arrival in the City of Light", "Chauffeured pickup from Paris CDG. Check-in at our boutique hotel on the Left Bank. Evening Seine cruise on an electric mahogany runabout.", "VIP airport fast-track, Private Seine cruise"),
                (2, "Masterpieces in Tranquility", "Exclusive after-hours private access to the Louvre galleries followed by lunch at an artisan bistro in Saint-Germain.", "Private Louvre gallery tour, Pastry atelier"),
                (3, "Transfer to the Valley of the Kings", "First-class journey south into the Loire Valley. Check-in to our private turreted castle surrounded by formal gardens.", "First-class rail, Castle arrival salon"),
                (4, "Chambord & Sancerre Vineyard Tasting", "Private visit to Château de Chambord, followed by cellar tasting with the winemakers of organic Sancerre estates.", "Château private tour, Underground cellar tasting"),
            ]
        },
        {
            'title': 'Lisbon Golden Light & Mystical Sintra Palaces',
            'slug': 'lisbon-sintra-palaces',
            'destination': dest_objects['lisbon-sintra-portugal'],
            'category': cat_cultural,
            'cover_image': 'packages/lisbon.jpg',
            'price': 2850.00,
            'discount_price': None,
            'duration_days': 6,
            'duration_nights': 5,
            'available_seats': 8,
            'difficulty': 'easy',
            'best_season': 'Spring & Autumn',
            'included_services': "5 Nights in Renovated Palace Hotels (Chiado & Sintra)\nPrivate Vintage Tram Tour and Fado Evening Dinner\nExclusive Early Entry to Sintra National Palaces\nAtlantic Coastal Wine and Seafood Experience\nZero Booking Fees & Verified Concierge Assistance",
            'excluded_services': "Transatlantic Airfare\nPersonal Souvenirs",
            'featured': True,
            'is_active': True,
            'itineraries': [
                (1, "Welcome to the Seven Hills", "Arrival in Lisbon. Settle into our converted 18th-century palácio hotel in Chiado with views across the Tagus river.", "Private transfer, Sunset port wine reception"),
                (2, "Azulejos, Tram 28 & Intimate Fado", "Private morning ceramic tile painting workshop with master artisans, followed by an evening dinner in a historic Alfama fado house.", "Artisan workshop, Traditional candlelit fado dinner"),
                (3, "Ascent into Mystical Sintra", "Chauffeured drive to the forested mountains of Sintra. Private early access to the whimsical Pena Palace and Quinta da Regaleira gardens.", "Pena Palace private entry, Spiral well exploration"),
                (4, "Atlantic Winds of Cabo da Roca", "Drive to the westernmost edge of continental Europe. Fresh seafood lunch in Cascais and sea salt tasting.", "Wild coastline tour, Cascais oyster & seafood pairing"),
            ]
        },
        {
            'title': 'Himalayan Cedar Silence & Ancient Monasteries',
            'slug': 'himalayan-cedar-silence-manali',
            'destination': dest_objects['himalayan-foothills-manali'],
            'category': cat_adventure,
            'cover_image': 'packages/manali.jpg',
            'price': 2400.00,
            'discount_price': 2150.00,
            'duration_days': 7,
            'duration_nights': 6,
            'available_seats': 6,
            'difficulty': 'moderate',
            'best_season': 'April to June & Sept to Nov',
            'included_services': "6 Nights in Handcrafted Timber Chalet & Luxury Apple Orchard Lodge\nPrivate 4x4 Alpine Mountain Transit\nDaily Morning Hatha Yoga and Forest Meditation Sessions\nOrganic Mountain Cuisine (All Breakfasts, Lunches, and Dinners)\nHigh-Altitude Native Mountain Guide",
            'excluded_services': "Domestic Flights to Kullu\nPersonal Trekking Gear",
            'featured': True,
            'is_active': True,
            'itineraries': [
                (1, "Arrival in the Valley of the Gods", "Scenic transfer from Kullu airport to our hand-built deodar timber chalet. Herbal welcome tea and sunset Himalayan orientation.", "Private 4x4 transfer, Evening cedar bonfire"),
                (2, "Ancient Timber Temples & Apple Glades", "Gentle hike through old-growth cedar forests to the 16th-century wooden pagoda temple of Hadimba and Naggar Castle.", "Heritage architecture walk, Organic orchard lunch"),
                (3, "Solang Alpine Meadows & Meditation", "Ascend to tranquil alpine pastures for guided mindfulness and breathwork against glacier-capped peaks.", "Mountain meditation, Meadow picnic"),
                (4, "High Rohtang Pass & Tibetan Monasteries", "Early journey across the high pass offering sweeping panoramic views of the Pir Panjal mountain range.", "High altitude pass excursion, Monastery butter lamp ceremony"),
            ]
        },
    ]

    for p_data in packages_data:
        itineraries = p_data.pop('itineraries')
        pkg, p_created = TourPackage.objects.update_or_create(
            slug=p_data['slug'],
            defaults=p_data
        )
        print(f"-> Package: {pkg.title} ({'Created' if p_created else 'Updated'})")

        # Itineraries
        TourItinerary.objects.filter(package=pkg).delete()
        for day_num, day_title, day_desc, day_acts in itineraries:
            TourItinerary.objects.create(
                package=pkg,
                day_number=day_num,
                title=day_title,
                description=day_desc,
                activities=day_acts
            )
        print(f"   + Added {len(itineraries)} itinerary days for {pkg.title}")

    # 5. Populate Gallery Images
    gallery_data = [
        {'image': 'gallery/paris.png', 'caption': 'Autumn Twilight over the Seine', 'tourist_name': 'Camille Laurent', 'location': 'Paris, France'},
        {'image': 'gallery/rome.jpg', 'caption': 'Morning Light at the Colosseum', 'tourist_name': 'Marcus Vance', 'location': 'Rome, Italy'},
        {'image': 'gallery/barcelona.jpg', 'caption': 'Sagrada Família Stained Glass Glow', 'tourist_name': 'Elena Rostova', 'location': 'Barcelona, Spain'},
        {'image': 'gallery/lisbon.jpg', 'caption': 'Golden Hour on Vintage Tram 28', 'tourist_name': 'Julien Moreau', 'location': 'Lisbon, Portugal'},
        {'image': 'gallery/manali.jpg', 'caption': 'Mist Rising Over Ancient Deodar Pines', 'tourist_name': 'Aarav Sharma', 'location': 'Himachal Pradesh, India'},
        {'image': 'gallery/bali.jpg', 'caption': 'Emerald Dawn on Tegallalang Rice Terraces', 'tourist_name': 'Sophia Thorne', 'location': 'Ubud, Bali'},
        {'image': 'gallery/g_1.jpg', 'caption': 'Alpine Reflection on Riffelsee Lake', 'tourist_name': 'Lukas Weber', 'location': 'Zermatt, Switzerland'},
        {'image': 'gallery/g_2.jpg', 'caption': 'Sunset Safari Across the Mara Plains', 'tourist_name': "Dr. David O'Connor", 'location': 'Masai Mara, Kenya'},
        {'image': 'gallery/g_3.jpg', 'caption': 'Secret Turquoise Cove on Costa Brava', 'tourist_name': 'Amara Diallo', 'location': 'Begur, Spain'},
    ]

    GalleryImage.objects.all().delete()
    for g in gallery_data:
        GalleryImage.objects.create(**g)
    print(f"-> Added {len(gallery_data)} curated Gallery Images.")

    # 6. Populate Testimonials
    testimonials_data = [
        {
            'client_name': 'Lady Eleanor Kensington',
            'client_designation': 'Art Curator & Historian, London',
            'testimonial_text': "The Tuscan vineyard estate organized by Wanderlust was pure poetry. Private cellar tastings, zero crowds, and deeply restful evenings under cypress trees. Unforgettable.",
            'rating': 5,
            'featured': True,
        },
        {
            'client_name': 'Arjun & Priya Singhania',
            'client_designation': 'Architects, Mumbai',
            'testimonial_text': "Our Himalayan mountain passage in Manali was spiritual and restorative. The pine log chalets and private morning meditation masters exceeded every expectation.",
            'rating': 5,
            'featured': True,
        },
        {
            'client_name': 'Mateo & Clara Fernandez',
            'client_designation': 'Industrial Designers, Buenos Aires',
            'testimonial_text': "From our private viewing of the Sagrada Família to sailing secret Costa Brava coves at sundown, Wanderlust curated an unhurried, soul-stirring journey.",
            'rating': 5,
            'featured': True,
        },
        {
            'client_name': 'Dr. Henrik Lindqvist',
            'client_designation': 'Marine Biologist, Stockholm',
            'testimonial_text': "Wanderlust redefined luxury travel for our family. Slow, thoughtful, and deeply respectful of native communities and ecological boundaries. Truly five stars.",
            'rating': 5,
            'featured': True,
        },
    ]

    Testimonial.objects.all().delete()
    for t in testimonials_data:
        Testimonial.objects.create(**t)
    print(f"-> Added {len(testimonials_data)} featured Guest Testimonials.")

    print("\n------------------------------------------------------------------")
    print("SUCCESS! Wanderlust database is now fully enriched with boutique content!")
    print("------------------------------------------------------------------")

if __name__ == '__main__':
    run()

