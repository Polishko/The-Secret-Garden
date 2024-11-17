from django.utils.html import strip_tags

test_address = ' 123 Amazing <script>console.log("Hi!")</script>  St.  '
cleaned_address = ' '.join(strip_tags(test_address).split())
print(cleaned_address)