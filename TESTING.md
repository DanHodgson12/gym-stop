# Testing

## Testing Paradigms

There are two types of testing a developer can carry out before, during and after writing a web application - Automated and Manual.

### Automated Testing

1. __Quicker__: Automated testing allows for hundreds of tests to be run in a short space of time, making it more resourceful than Manual testing.
2. __Efficient__: Tests written by developers help to detect errors earlier on, and help avoid writing code that likely won't perform as expected.
3. __Specific__: Tests can be written for specific edge cases in which manual testing may not be able to pick up.
4. __Resourceful__: Automated tests can be used for continuous testing of an application, making it easier to find an error if a new piece of content is added to a page, for example.
5. __Data-driven__: Automated testing can be used to check if a piece of code provides the same outcome when using different sources of data.

### Manual Testing

1. __UX(User Experience)__: Manual testing allows for the developer to check if the user experience of the application is as intended.
2. __Layout/Responsiveness__: Manual testing allows for the developer to inspect the application on different browsers and devices, which is something automated testing would not pick up on.
3. __Animation & Interactivity__: Manual testing allows for the developer to check if animations and interactions between elements are performing as expected.
4. __Accessibility__: Manual testing allows the developer to test the application with screen readers and make sure it is accessible.

Although one form of testing may be more appropriate than the other for a specific application, they do both have downsides. The disadvantage of one form of testing is usually something the other form of testing can provide.

Due to this, it is best practice to utilise both forms of testing during the building of an application. However, the choice for which form of testing to use depends on resources available, budget and whether or not you have a team large enough to carry out the tests.

The developer chose to use automated testing as the main form of testing throughout this project. They felt it was an efficient method for this type of application due to its size and the fact that a lot of aspects of the application relied on functions rendering and manipulating data.

## Testing User Stories

### Viewing and Navigation

- **As a** Shopper, **I want** to view a list of products **so that** I can select some to purchase.
  - **Given** I click the "Shop Now" button on the home page, or click the "All Products" link in the navigation menu, **then** I will see a list of products to view.
- **As a** Shopper, **I want** to view individual product details **so that** I can identify the price, description, product rating, product image, and available sizes.
  - **Given** I click on the individual product card, **then** I will see the full product detail page, showing the price, description, product rating, product image, and available sizes.
- **As a** Shopper, **I want** to quickly identify deals, clearance items, and special offers **so that** I can take advantage of special savings on products I'd like to purchase.
  - **Given** I look beneath the main navigation menu, **then** I will see that there is an offer for free delivery on orders over £50.
- **As a** Shopper, **I want** to easily view the total of my purchases at any time **so that** I can avoid spending too much.
  - **Given** I look in the top right corner of the navigation menu, **then** I will see the bag icon showing the total cost of items in my bag.

### Registration and User Accounts

- **As a** Site User, **I want** to easily register for an account **so that** I can have a personal account and be able to view my profile.
  - **Given** I click the 'My Account' icon in the navigation menu, then click the 'Register' link, **then** I will be able to register with an account.
- **As a** Site User, **I want** to easily log in or log out **so that** I can access my personal account information.
  - **Given** I click the 'My Account' icon in the navigation menu, then click the 'Login' or 'Logout' link, **then** I will be able to log in or out of my account.
- **As a** Site User, **I want** to easily recover my password in case I forget it **so that** I can recover access to my account.
  - **Given** I am on the login page and I click the 'Forgot Password?' link, **then** I will be able to reset my password.
- **As a** Site User, **I want** to receive an email confirmation after registering **so that** I can verify that my account registration was successful.
  - **Given** I register with an account with a valid email address, **then** I will receive an email asking me to click a link to verify my account.
- **As a** Site User, **I want** to have a personalized user profile **so that** I can view my personal order history and order confirmations, and save my payment information.
  - **Given** I click the 'My Account' icon in the navigation menu, then click the 'My Profile' link, **then** I will be able to see my saved payment and delivery information and order history.

### Sorting and Searching

- **As a** Shopper, **I want** to sort the list of available products **so that** I can easily identify the best rated, best priced, and categorically sorted products.
  - **Given** I click the 'All Products' dropdown link in the navigation menu and select from one of the dropdown options, **then** I will be able to sort by price, rating or category.
- **As a** Shopper, **I want** to sort a specific category of product **so that** I can find the best-priced or best-rated product in a specific category, or sort the products in that category by name.
  - **Given** I click the 'Sort by...' dropdown in the top right corner of the products page, **then** I will be able to sort by price, rating, name and category of product in ascending or descending order.
- **As a** Shopper, **I want** to search for a product by name or description **so that** I can find a specific product I'd like to purchase.
  - **Given** I type keywords into the search bar in the middle of the navigation menu, **then** I will be able to search for an item containing that keyword in the product name, category or description.
- **As a** Shopper, **I want** to easily see what I've searched for and the number of results **so that** I can quickly decide whether the product I want is available.
  - **Given** I look at the top left of the product page, **then** I will see the number of results returned for the search criteria I have entered.

### Purchasing and Checkout

- **As a** Shopper, **I want** to easily select the size and quantity of a product when purchasing it **so that** I ensure I don't accidentally select the wrong product, quantity, or size.
  - **Given** I navigate to a product detail page and select the size and quantity with the appropriate buttons, **then** I will be able to add the correct size and quantity of product to my bag.
- **As a** Shopper, **I want** to view items in my bag to be purchased **so that** I can identify the total cost of my purchase and all items I will receive.
  - **Given** I look at the success message shortly after adding a product to my bag, or I click on the shopping bag link in the navigation menu, **then** I will be able to see the cost of individual items as well as a subtotal and total of all items.
- **As a** Shopper, **I want** to adjust the quantity of individual items in my bag **so that** I can easily make changes to my purchase before checkout.
  - **Given** I navigate to the shopping bag, **then** I will be able to see different sizes of the same product individually, so I can easily make changes to my order.
- **As a** Shopper, **I want** to easily enter my payment information **so that** I can check out quickly and with no hassles.
  - **Given** I click the 'Secure Checkout' button in my shopping bag, **then** I will be prompted to enter delivery and billing information to finalise my purchase.
- **As a** Shopper, **I want** to view an order confirmation after checkout **so that** I can verify that I haven't made any mistakes.
  - **Given** I finalise my purchase, or I click the link for the order number in my profile's Order History section, **then** I will see an order confirmation page showing the specific details of my order.
- **As a** Shopper, **I want** to receive an email confirmation after checking out **so that** I can keep the confirmation of what I've purchased for my records.
  - **Given** I finalise my purchase, **then** I will be sent a confirmation email showing the details of my order.

### Reviews and Subscriptions

- **As a** Shopper, **I want** to receive marketing emails **so that** I can keep up to date with new deals and offers.
  - **Given** I click the 'Subscribe' button in the page footer, or click the 'Subscribe to marketing emails?' option in my profile's saved information, **then** I will receive marketing emails.
- **As a** Shopper, **I want** to ubsubscribe from marketing emails **so that** I can chose whether I want to see offers and deals.
  - **Given** I click the 'Unsubscribe' link in a marketing email, or uncheck the 'Subscribe to marketing emails?' option in my profile's saved information, **then** I will be unsubscribed from marketing emails.
- **As a** Shopper, **I want** to leave reviews on products I have purchased **so that** I can let other shoppers know what I think of the product.
  - **Given** I am logged in, navigate to the specific product page of a product I have purchased, **then** I can click the 'Add Review' button to leave a review.
- **As a** Shopper, **I want** to be able to edit reviews I have left **so that** I can update my rating, headline or description if I change my mind.
  - **Given** I am logged in, navigate to the specific product page of a product I have purchased, find the review and click the 'Edit' button, **then** I will be able to delete the review.
- **As a** Shopper, **I want** to be able to delete reviews I have left **so that** I can chose whether to leave my review for others to see.
  - **Given** I am logged in, navigate to the specific product page of a product I have purchased, find the review and click the 'Delete' button, **then** I will be able to delete the review.

### Admin and Store Management

- **As a** Store Owner, **I want** to add a product **so that** I can add new items to my store.
  - **Given** I am a superuser and am logged in, **then** I can navigate to the 'Product Management' page via the 'My Account' link in the navigation menu, and add a product.
  - **Given** I am a superuser and am logged in to the admin panel, **then** I can navigate to the 'Products' section and manually add a product
- **As a** Store Owner, **I want** to edit/update a product **so that** I can change product prices, descriptions, images, and other product criteria.
  - **Given** I am a superuser and am logged in, **then** I can navigate to the specific product detail page, click the 'Edit' button and edit a product.
  - **Given** I am a superuser and am logged in to the admin panel, **then** I can navigate to the 'Products' section and manually edit a product
- **As a** Store Owner, **I want** to delete a product **so that** I can remove items that are no longer for sale.
  - **Given** I am a superuser and am logged in, **then** I can navigate to the specific product detail page, click the 'Delete' button and delete a product.
  - **Given** I am a superuser and am logged in to the admin panel, **then** I can navigate to the 'Products' section and manually delete a product

## Tools Testing

- [Google Chrome DevTools](https://developer.chrome.com/docs/devtools/)
  - Google Chrome DevTools was used throughout the development process to test, explore and make changes to the HTML and CSS of the webpage.
  - Google Chrome DevTools was used throughout the development process to test, explore and debug any issues with the Javascript or Python affecting the functionality of the application.

- Responsiveness
  - [Responsive Design Checker](https://www.responsivedesignchecker.com/) was used to check responsiveness across a variety of devices and screen sizes.
  - [Am I Responsive?](https://ui.dev/amiresponsive) was used to check responsiveness across different screen sizes and generate the mockup final image.
  - [Google Chrome DevTools](https://developer.chrome.com/docs/devtools/) was used to check responsiveness across different screen sizes during the development and testing phases.

## Compatibility Testing

### Browser Compatibility

Browser | Outcome | Pass/Fail
--- | --- | ---
Google Chrome | No appearance, responsiveness or functionality issues | Pass
Safari | No appearance, responsiveness or functionality issues | Pass
Mozilla Firefox | No appearance, responsiveness or functionality issues | Pass
Microsoft Edge | No appearance, responsiveness or functionality issues | Pass
  
### Device Compatibility

The web application was tested across a wide variety of devices using [Google Chrome DevTools](https://developer.chrome.com/docs/devtools/) & [Responsive Design Checker](https://www.responsivedesignchecker.com/).

- No appearance, responsiveness or functionality issues were found.

## Common Elements Testing



### Known Bugs

There are no known bugs with the web application.

---

## Code Validation

The [W3C Markup Validator](https://validator.w3.org/) and [W3C CSS Validator](https://jigsaw.w3.org/css-validator/) services were used to check for any code errors or misuse of syntax/elements in the HTML & CSS.

The [JSHint](https://jshint.com/) service was used to check for any code errors or misuse of syntax in the JavaScript.

The [CI Python Linter](https://pep8ci.herokuapp.com/) and [Flake8](https://flake8.pycqa.org/en/latest/) services were used to check for any linting errors in the Python code.

### HTML

The W3C Markup Validator returned multiple errors and warnings with a lot of the Django templating language used. The developer chose to ignore these specific warnings, as this tool is primarily designed to validate static HTML and doesn't recognize server-side templating languages, including Django.

Other than the above, there were no legitimate errors in the HTML code.

### CSS

The W3C CSS Validator returned no errors in the code.
![CSS Validation](static/images/css-validation.png)

### JavaScript

The JSHint Validation returned a one error in the JS files for undefined variables:

- `$` - This was ignored as it is required for functions using jQuery.

### Python

Flake8 returned 11 errors in the code. However, these errors were mainly for "line too long" in the 'migrations' files. These were left untouched as they were autmoatically generated files.

There were also other files such as env.py, settings.py and apps.py (for each project) that teh developer chose to ignore.

There was also one error type that was chosen to be ignored - *W503 line break before binary operator*. Upon fixing this error, another error occurs - *W504 line break after binary operator*. As these errors conflict with one another, the decision was made to chose to ignore one of the errors - W503.

![Flake8 Validation](assets/flake8-report.png)

![Flake8 Settings](assets/flake8-settings.png)

## Lighthouse Report

Lighthouse in Google Chrome Dev Tools was used to test performance, accessibility, best practices and search engine optimisation of the webpage.