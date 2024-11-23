# import json
# from django.core.serializers.json import DjangoJSONEncoder
# from thesecretgarden.flowers.models import Plant
#
# # Define the file where the data will be stored
# OUTPUT_FILE = 'plant_data.json'
#
#
# def extract_plant_data():
#     try:
#         # Query all plant objects
#         plants = Plant.objects.all()
#
#         # Serialize data
#         plant_data = []
#         for plant in plants:
#             plant_data.append({
#                 'name': plant.name,
#                 'slug': plant.slug,
#                 'type': plant.type,
#                 'description': plant.description,
#                 'price': float(plant.price),  # Convert Decimal to float for JSON compatibility
#                 'stock': plant.stock,
#                 'photo': plant.photo.name if plant.photo else None,
#                 'created_at': plant.created_at.isoformat(),
#                 'updated_at': plant.updated_at.isoformat(),
#             })
#
#         # Write serialized data to JSON file
#         with open(OUTPUT_FILE, 'w', encoding='utf-8') as file:
#             json.dump(plant_data, file, cls=DjangoJSONEncoder, indent=4)
#
#         print(f"Successfully extracted data for {len(plants)} plants to {OUTPUT_FILE}")
#     except Exception as e:
#         print(f"Error occurred during extraction: {e}")
#
#
# def extract_gift_data():
#     try:
#         # Query all gift objects
#         from thesecretgarden.gifts.models import Gift  # Import Gift model
#         gifts = Gift.objects.all()
#
#         # Serialize data
#         gift_data = []
#         for gift in gifts:
#             gift_data.append({
#                 'brand_name': gift.brand_name,
#                 'short_name': gift.short_name,
#                 'short_description': gift.short_description,
#                 'type': gift.type,
#                 'price': float(gift.price),
#                 'stock': gift.stock,
#                 'photo': gift.photo.name if gift.photo else None,
#                 'created_at': gift.created_at.isoformat(),
#                 'updated_at': gift.updated_at.isoformat(),
#             })
#
#         # Write serialized data to JSON file
#         with open(OUTPUT_GIFT_FILE, 'w', encoding='utf-8') as file:
#             json.dump(gift_data, file, cls=DjangoJSONEncoder, indent=4)
#
#         print(f"Successfully extracted data for {len(gifts)} gifts to {OUTPUT_GIFT_FILE}")
#     except Exception as e:
#         print(f"Error occurred during extraction: {e}")
#
#
# # Run the script
# if __name__ == '__main__':
#     extract_plant_data()
#     extract_gift_data()
