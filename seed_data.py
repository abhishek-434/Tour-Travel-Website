import os
import django

# Bootstrap Django settings context
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tour_travel.settings')
django.setup()

import datetime
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from core.models import WebsiteSetting, FAQ, Testimonial, GalleryImage
from tours.models import Category, Destination, TourPackage, TourItinerary, Review
from blog.models import BlogCategory, BlogPost

# 1x1 pixel transparent GIF binary data for mock files
GIF_DATA = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'

def get_mock_image(name):
    return SimpleUploadedFile(name, GIF_DATA, content_type='image/gif')

def seed():
    print("--------------------------------------------------")
    print("Starting Wanderlust Database Seeding Process...")
    print("--------------------------------------------------")

    # 1. Create Users
    print("Creating accounts...")
    admin_user, admin_created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@wanderlust.com',
            'first_name': 'Marcus',
            'last_name': 'Sterling',
            'is_superuser': True,
            'is_staff': True
        }
    )
    if admin_created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("-> Created Admin Account: username='admin', password='admin123'")
    else:
        print("-> Admin account already exists.")

    traveler_user, traveler_created = User.objects.get_or_create(
        username='traveler',
        defaults={
            'email': 'traveler@wanderlust.com',
            'first_name': 'Alex',
            'last_name': 'Wanderer'
        }
    )
    if traveler_created:
        traveler_user.set_password('traveler123')
        traveler_user.save()
        print("-> Created Traveler Account: username='traveler', password='traveler123'")
    else:
        print("-> Traveler account already exists.")

    # 2. Website Settings
    print("\nConfiguring core settings...")
    settings = WebsiteSetting.get_solo()
    settings.site_name = "Wanderlust"
    settings.contact_email = "concierge@wanderlust.com"
    settings.contact_phone = "+1 (800) 555-ROAM"
    settings.address = "742 Evergreen Terrace, Wander City, WC 10001"
    settings.google_maps_embed_url = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3022.428588829598!2d-73.98701042342371!3d40.751680135118774!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c259a9b3117469%3A0xd134e199a405a163!2sEmpire%20State%20Building!5e0!3m2!1sen!2sin!4v1703222384910!5m2!1sen!2sin"
    settings.facebook_url = "https://facebook.com/wanderlust"
    settings.instagram_url = "https://instagram.com/wanderlust"
    settings.twitter_url = "https://twitter.com/wanderlust"
    settings.youtube_url = "https://youtube.com/wanderlust"
    settings.save()
    print("-> Global settings configured.")

    # 3. Testimonials
    print("\nAdding testimonials...")
    Testimonial.objects.all().delete()
    Testimonial.objects.create(
        client_name="Sophia Loren",
        client_designation="Luxury Blogger",
        testimonial_text="The tailored Bora Bora trip was pure perfection. Every transfer was synchronized and the water villa upgrades exceeded our expectations.",
        rating=5,
        featured=True
    )
    Testimonial.objects.create(
        client_name="Dr. Harrison Carter",
        client_designation="Wild Photographer",
        testimonial_text="The private Masai Mara safari guided by local naturalists gave us access to wildlife hotspots away from tourist crowds. Invaluable curation!",
        rating=5,
        featured=True
    )
    Testimonial.objects.create(
        client_name="Liam Mercer",
        client_designation="Backpack Enthusiast",
        testimonial_text="Even with a moderate budget, Wanderlust helped me plan an authentic cultural experience in Kyoto with cozy boutique stays.",
        rating=4,
        featured=True
    )
    print("-> 3 Testimonials seeded.")

    # 4. FAQs
    print("\nAdding FAQs...")
    FAQ.objects.all().delete()
    FAQ.objects.create(
        question="What is included in the base tour package cost?",
        answer="Our base rates cover boutique double lodgings, local private transport transfers, daily breakfasts, national park passes, and the services of local curators. Flights are optional add-ons.",
        category='general',
        order=1
    )
    FAQ.objects.create(
        question="How do I request a date rescheduling?",
        answer="rescheduling requests must be sent to concierge@wanderlust.com at least 15 days before your departure. Rescheduling is free subject to hotel seasonal pricing adjustments.",
        category='booking',
        order=2
    )
    FAQ.objects.create(
        question="What is the mock payment checkout?",
        answer="To secure bookings in our sandbox development environment, you can type any cardholder name and a standard test card number. No charges will be processed.",
        category='payments',
        order=3
    )
    print("-> 3 FAQs seeded.")

    # 5. Tours Categories
    print("\nAdding tour categories...")
    Category.objects.all().delete()
    cat_luxury = Category.objects.create(name="Luxury Escapes", slug="luxury", icon="bi-gem", description="Elite resorts, private island transfers, and bespoke dining.")
    cat_adventure = Category.objects.create(name="Adventure", slug="adventure", icon="bi-activity", description="High altitude trekking, ski slopes, and aquatic rafting.")
    cat_nature = Category.objects.create(name="Nature & Wildlife", slug="nature", icon="bi-tree-fill", description="National parks safaris, marine reef diving, and jungle cabins.")
    cat_cultural = Category.objects.create(name="Cultural", slug="cultural", icon="bi-bank", description="Ancient temples, guided museums tours, and tea ceremonies.")
    print("-> 4 Categories seeded.")

    # 6. Destinations
    Destination.objects.all().delete()
    dest_bali = Destination.objects.create(
        name="Bali, Indonesia",
        slug="bali",
        hero_image="destinations/bali.jpg",
        description="A tropical paradise renowned for its volcanic forested mountains, iconic rice paddies, beaches, and coral reefs.",
        attractions="Ubud Sanctuary, Uluwatu Temple, Nusa Penida Cliffs",
        best_time_to_visit="April to October",
        weather_info="26°C - 31°C average tropical climate",
        featured=True
    )
    dest_swiss = Destination.objects.create(
        name="Swiss Alps, Switzerland",
        slug="swiss-alps",
        hero_image="destinations/swiss.jpg",
        description="A breathtaking landscape of snow-draped alpine summits, glacial lakes, and cozy timber ski lodges.",
        attractions="Zermatt Matterhorn, Interlaken Lakes, Glacier Express",
        best_time_to_visit="December to April",
        weather_info="-5°C - 8°C alpine conditions",
        featured=True
    )
    dest_kenya = Destination.objects.create(
        name="Masai Mara, Kenya",
        slug="masai-mara",
        hero_image="destinations/kenya.jpg",
        description="An expansive savannah wilderness home to spectacular lions, leopards, cheetahs, and the Great Migration.",
        attractions="Mara River Crossing, Wildebeest Trails, Balloon Safari",
        best_time_to_visit="July to October",
        weather_info="15°C - 28°C dry savannah winds",
        featured=True
    )
    
    # Establish symmetrical nearby destinations
    dest_bali.nearby_destinations.add(dest_kenya) # Just a test symmetrical connection
    print("-> 3 Destinations seeded.")

    # 7. Tour Packages
    print("\nAdding packages & itineraries...")
    TourPackage.objects.all().delete()
    
    # Package 1: Bali
    p_bali = TourPackage.objects.create(
        title="Bali Luxury Lagoons & Temple Escape",
        slug="bali-lagoon-escape",
        destination=dest_bali,
        category=cat_luxury,
        cover_image="packages/pkg_bali.jpg",
        price=4500.00,
        discount_price=3990.00,
        duration_days=8,
        duration_nights=7,
        available_seats=6,
        difficulty="easy",
        best_season="May - September",
        included_services="5-star lagoon villa lodging\nDaily private buffet breakfast\nPrivate airport transfers\nLocal temple curator guide passes\nTraditional spa therapy credits",
        excluded_services="International airline tickets\nLunch and dinners (unless scheduled)\nTravel insurance coverage\nVisa entry processing fees",
        featured=True,
        is_active=True
    )
    TourItinerary.objects.create(
        package=p_bali,
        day_number=1,
        title="Arrival & Villa Check-in",
        description="Land in Denpasar Airport. Your private chauffeur guides you past customs to check in at the 5-star Ubud Forest Villa. Welcome tropical drinks served.",
        activities="Airport transfer, Welcome dinner, Spa treatment"
    )
    TourItinerary.objects.create(
        package=p_bali,
        day_number=2,
        title="Ubud Sanctuary & Rice Terraces Walk",
        description="Enjoy a morning hike along Tegallalang rice paddies. Spend your afternoon visiting Ubud Monkey Forest accompanied by our native zoology curator.",
        activities="Rice terrace walk, Monkey sanctuary tour"
    )
    TourItinerary.objects.create(
        package=p_bali,
        day_number=3,
        title="Sunset Uluwatu Temple & Kecak Dance",
        description="Travel south to the cliffs of Uluwatu. Experience the sunset over the Indian Ocean while watching a traditional Kecak fire dance drama.",
        activities="Temple cliff walk, Fire dance performance"
    )

    # Package 2: Swiss Alps
    p_swiss = TourPackage.objects.create(
        title="Matterhorn Ski & Glacier Adventure",
        slug="matterhorn-ski-adventure",
        destination=dest_swiss,
        category=cat_adventure,
        cover_image="packages/pkg_swiss.jpg",
        price=6200.00,
        duration_days=6,
        duration_nights=5,
        available_seats=4,
        difficulty="challenging",
        best_season="January - March",
        included_services="Premium Zermatt ski lodge room\nUnlimited slopes ski lift passes\nExpert ski instructors guidance\nGlacier Express panorama rail tickets\nThermal hot springs access pass",
        excluded_services="Heavy ski gear rentals\nHelicopter ski charters\nOptional private ski instructors",
        featured=True,
        is_active=True
    )
    TourItinerary.objects.create(
        package=p_swiss,
        day_number=1,
        title="Alpine Lodge Check-in & Gear Fitting",
        description="Board the mountain rail to Zermatt. Check in at your luxury chalet with Matterhorn views. Meet instructors and fit ski gear.",
        activities="Rail transfer, Lodge orientation, Ski fitting"
    )
    TourItinerary.objects.create(
        package=p_swiss,
        day_number=2,
        title="Matterhorn Slopes Skiing Session",
        description="First skiing run on the Matterhorn glacier paradise. Full day slopes training under the guidance of our local instructors.",
        activities="Skiing, Glacier hiking, Après-ski dinner"
    )

    # Package 3: Kenya Safari
    p_kenya = TourPackage.objects.create(
        title="Masai Mara Luxury Wildebeest Safari",
        slug="masai-mara-safari",
        destination=dest_kenya,
        category=cat_nature,
        cover_image="packages/pkg_kenya.jpg",
        price=5400.00,
        discount_price=4950.00,
        duration_days=7,
        duration_nights=6,
        available_seats=8,
        difficulty="moderate",
        best_season="July - September",
        included_services="Luxury wilderness tent lodging\nDaily private 4x4 game drives\nFull board dining plans\nNational park curator fees\nGuided evening bonfire stories",
        excluded_services="Hot air balloon charters\nLocal conservation tips\nAlcoholic drinks",
        featured=True,
        is_active=True
    )
    TourItinerary.objects.create(
        package=p_kenya,
        day_number=1,
        title="Charter flight & Tented Camp Check-in",
        description="Fly via light charter from Nairobi to Masai Mara airstrip. Drive to the luxury tented wilderness camp and enjoy sunset appetizers.",
        activities="Charter flight, Safari drive, Sunset appetizers"
    )
    
    # Seed Reviews
    Review.objects.all().delete()
    Review.objects.create(package=p_bali, user=admin_user, rating=5, comment="A flawless execution. The villa is breathtaking and Ubud guides are absolute experts.")
    Review.objects.create(package=p_bali, user=traveler_user, rating=4, comment="Incredible views, but wish we spent more days at the beach than temples. Overall amazing.")
    Review.objects.create(package=p_swiss, user=traveler_user, rating=5, comment="Challenging ski runs but coming back to the thermal baths made it pure heaven. Will book again!")

    print("-> 3 Packages & Itineraries seeded with sample Reviews.")

    # 8. Blog categories & posts
    print("\nAdding blog stories...")
    BlogCategory.objects.all().delete()
    cat_guide = BlogCategory.objects.create(name="Travel Guides", slug="guides")
    cat_tips = BlogCategory.objects.create(name="Tips & Hacks", slug="tips")
    
    BlogPost.objects.all().delete()
    BlogPost.objects.create(
        title="The Ultimate Packing Guide for Luxury Safaris",
        slug="ultimate-safari-packing-guide",
        author=admin_user,
        category=cat_guide,
        cover_image="blog/blog_safari.jpg",
        content="Packing for a luxury safari requires balancing safety, rules, and style. In the savannah, bright colors are avoided to prevent distracting wildlife. We recommend neutral tones (khaki, olive green, sand).\n\nAdditionally, most light bush flights restrict baggage weight to 15kg in soft duffel bags. In this guide, we outline the essential tech gear, footwear, and lenses you need to make the most of your wild expedition.",
        excerpt="What to pack in a soft-sided duffel for luxury bush flight transfers and private safari walks.",
        featured=True,
        views_count=142
    )
    BlogPost.objects.create(
        title="5 Secrets to Booking Luxury Travel on a Budget",
        slug="secrets-booking-luxury-budget",
        author=traveler_user,
        category=cat_tips,
        cover_image="blog/blog_budget.jpg",
        content="Luxury travel does not always require high spending. By utilizing flash sales, shoulder season scheduling, and premium card points multipliers, you can access 5-star properties for a fraction of the cost.\n\nOur travel curators share their insider tips on how to request hotel room upgrades, bypass concierge costs, and check into boutique resorts without breaking your bank accounts.",
        excerpt="Tips from our travel curators on scheduling shoulder seasons, using card perks, and room upgrades.",
        featured=False,
        views_count=89
    )
    print("-> 2 Blog posts seeded.")

    # 9. Gallery Images
    print("\nAdding gallery images...")
    GalleryImage.objects.all().delete()
    GalleryImage.objects.create(image="gallery/g_1.jpg", caption="Snorkeling in Bali's Crystal Bay", tourist_name="Charlotte", location="Nusa Penida, Bali")
    GalleryImage.objects.create(image="gallery/g_2.jpg", caption="Skiing down Zermatt peak", tourist_name="Ethan", location="Zermatt, Switzerland")
    GalleryImage.objects.create(image="gallery/g_3.jpg", caption="Giraffe breakfast encounter", tourist_name="Victoria", location="Nairobi, Kenya")
    print("-> 3 Gallery images seeded.")

    print("\n--------------------------------------------------")
    print("Seeding Complete! Database is fully populated.")
    print("Default Admin: username='admin', password='admin123'")
    print("Default Customer: username='traveler', password='traveler123'")
    print("--------------------------------------------------")

if __name__ == '__main__':
    seed()
