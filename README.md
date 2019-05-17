# Castle Apartments
SC-T-220-VLN2\
Reykjavik University\
17. 5. 2019

## About

Castle Apartments is a real estate website where users can buy and sell properties.\
The website was created by students during a three week course at Reykjavik University.\
The project uses Django, Python and PostgreSQL.

## Requirements

### Featural demands fulfilled
1. Layout Site
   1. The website has a fixed navigation bar on every page
   2. The website has a footer on every page
2. Edit profile
   1. The user can edit his name.
   2. The user can edit his profile image.
3. Apartment catalogue
   1. The user can filter properties by postal code.
   2. The user can search for a property by text.
   3. The user can order properties by price and name.
4. Search history
   1. The user can see which properties he has viewed recently (10 most recent).
5. Apartment details
   1. A property can have a description.
   2. A property can have multiple images.
   3. A property has a seller.
6. Seller profile
   1. A user can view the public profile of a property's seller.
7. Buy an apartment
   1. Contact information
      1. The user can fill in his street name.
      2. The user can fill in his house number.
      3. The user can fill in his city.
      4. The user can select his country from a dropdown list.
      5. The user can fill in his postal code.
      6. The user can fill in his social security number.
   2. Payment step
      1. The user can fill in his credit card information.
   3. Review step
      1. The user can review his payment information before confirming the purchase.
   4. Confirmation step
      1. The user can confirm his purchase and gets a receipt confirmation.
   5. Easy navigation between steps
      1. The user can edit his payment information after writing it in and before finalizing the purchase.


### Structural demands fulfilled

1. The application uses a database to store the data
2. Django Model API is used.
3. The MTV pattern is used.
4. Git was used for version control and GitHub was used for a repository.
5. Exceptions are handled in a proper manner.


### Bonus demands fulfilled

1. Deployment
   1. The application was deployed to Heroku: http://kastalar.herokuapp.com/property/
2. User accounts
   1. The user can create his own account.
   2. The user can log in to his own account.
   3. The user can sign out of his account.
3. User sells a property
   1. The user can put a property up for sale.
   2. The user can edit a property he has put up for sale.
4. User profile pages
   1. The user can both view his own private profile (with more information and editing abilities) and his seller profile (how other users will see him).
   2. The user can view his active listings on his profile page.
   3. The user can view the properties he has sold on his profile page.
   4. The user can view the properties he has purchased on his private profile page.
5. Favourites
   1. The user can add a property to favourites and unfavourite it.
   2. The user can view his favourite properties on his private profile page.
   3. An AJAX request is used to update the favourite status and count when a user favourites/unfavourites a property.
6. Filters
   1. The website has multiple filters: some are a dropdown, some are checkboxes and the user can also search by text.
   2. Searching for properties is done with an AJAX request.
   3. AJAX filter updates for country/municipality/city/postal code are conditional.
7. Accessibility
   1. The website is user friendly.
   2. The website is mobile friendly.
   3. Images on the webpage have alt tags.
8. Navigation
   1. Links in navigation bar are active depending on what page the user is on.
9. Other
   1. The website has an About Us page.
   2. The admin can add attributes, edit, create and delete properties and users through the admin site.

### [Requirements from Design Report](https://github.com/egilltor17/VLN2-Castle-Apartments/wiki/Requirements-from-Design-Report)
