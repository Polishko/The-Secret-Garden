# The-Secret-Garden
![image](https://github.com/user-attachments/assets/04b5b2e4-6103-4581-b8dc-d73644ec1a38)

## 📚 Table of Contents
1. [About](#about)
2. [Deployed App](#deployed-app)
3. [Setup Instructions](#setup-instructions)
4. [General Requirements](#general-requirements)
5. [Bonuses](#bonuses)
6. [Additional Functionality](#additional-functionality)
7. [Lisence](#lisence)
8. [Credits](#credits)

## <a name="about"></a>📚 About
- A flower shop web app – my final project for the Python Web course at SoftUni. The shop offers houseplants, flowers, and a selection of gifts, including wine, chocolate, and candles. Public users can view the list of products and their details, and they can also send messages to make suggestions, ask questions, or raise any concerns.
- Customers must register in order to purchase products and place orders. An address is required for order placement. Customers can edit their profiles, adding information such as phone number, address, and birthday (for future promotions), and they can also deactivate their profiles.
- Shop staff, as well as superuser admins, can use the app’s front end to add, edit, and remove products, including bulk additions. The superadmin can also delete and edit user profiles, but certain tasks, such as directly removing profiles (without deleting the associated user first), removing users with existing orders, deleting reserved products, and a few other actions, are restricted in order to protect the integrity of the database.   

## <a name="deployed-app"></a>🚀 Deployed App
**[Visit the deployed app here](https://thesecretgarden-bnf4g7hkcrdwajea.italynorth-01.azurewebsites.net/)**


![image](https://github.com/user-attachments/assets/a8162777-7443-4037-afac-4254fea25aa0)

## <a name="setup-instructions"></a>🛠️ Setup Instructions
For detailed setup instructions, please refer to the [Setup Guide](SETUP.md).

## <a name="general-requirements"></a>📋 General Requirements
For the details regarding the general project requirements, please refer to [Project Requirements](REQUIREMENTS.md).

## <a name="bonuses"></a>🌟 Bonuses
- ✅ **Testing**: Comprehensive unit and integration tests are implemented, particularly covering order-related views and functionality.
- ✅ **Asynchronous Views**:
  - **Implements an asynchronous REST API view, `related_products`, that fetches and returns related product data as JSON.
  - Uses Django's async capabilities and integrates with JavaScript for a seamless user experience.
- ✅ **Django REST Capabilities**: Added REST API functionality through the `ContactMessageApiView`, allowing users to submit contact messages with proper validation and response handling.
- ✅ **Extended Django User Model**: The Django user model has been extended to include additional fields (e.g., `role`, `slug`) and linked with a one-to-one Profile model for enhanced customization.
- ✅ **Deployment**: The application is deployed to Azure, with a live link provided in the README for easy access.

## <a name="additional-functionality"></a>🛠️ Additional Functionality
- ✅ **Media Storage**: Integrated Cloudinary for efficient and secure media storage and retrieval.
- ✅ **Signals**:
  - Automatically create a profile when a user is created.
  - Sync `is_active` status on profile deactivation.
  - Assign groups and permissions to users on creation based on roles.
  - Clean up Cloudinary images when products are deleted.
- ✅ **Content Type Framework**: Utilized to manage product relationships dynamically.
- ✅ **Context Processors**: Shared context (e.g., cart item count) across templates to simplify logic and improve usability.
- ✅ **Group Permissions**:
  - **Admin Panel Permissions**: Group permissions for the admin panel are assigned automatically based on roles.
  - **Frontend Permissions**: These are managed separately using custom permission mixins.

## <a name="lisence"></a>📝 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## <a name="credits"></a>🏷️ Credits
Original image names from Unsplash are documented in the file `unsplash_original_image_references.xlsx`.
