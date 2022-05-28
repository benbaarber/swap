# Swap: The Day-Trading Game (with fake money)

## Navigation

The website is deployed at [this link](http://swap-bongobooks.herokuapp.com/index.html).

There are two usernames that have roles:
- foobar@bingbong.com (Admin role)
- barfoo@bingbong.com (User role)

The password for both is **Password123**. 

Users have every permission except for `patch:user`. Admins have access to every permission.

### Features

###### Get Data

Clicking this will send a GET request to the */user/username* endpoint. It requires the `read:user` permission. It will return the balance, metadata, and username of a user in JSON format.

###### Buy

Follow the instructions of the button and then click it. This will send a POST request to the */user/username/investments* endpoint. It requires the `create:investments` permission. It will return nothing, subtracting the total value from the user's balance.

###### List Investments

Pressing the **Update** button will send a GET request to the *user/username/investments* endpoint. It requires the `read:investments` permission. It will return a list of active investments for the user, displaying the investment ID, the ticker, the amount, and the date and time of purchase. 

###### Sell

Next to each investment in the list, there is a small unlabeled button. Pressing this button will send a DELETE request to the *user/username/investments/id* endpoint. It requires the `delete:investments` permission. It will return nothing and refresh the list of investments, adding the total value to the user's balance.

###### Give Bonus

Follow the instructions of the button and then click it. This will send a PATCH request to the */user/username* endpoint. It requires the `patch:user` permission. It will return nothing and add the specified amount to the specified user's balance. This method is only allowed if the current user has the **Admin** role.

## Testing

To test the application's endpoints without authorization, it needs to be done locally. Navigate to [this testing script](/test-app.sh) and configure it. Then, run `./test-app.sh` in the main project directory. This will run a copy of the app with no authorization through [this pytest file](/tests/unit/test_app.py). After the local testing is complete, the script will then test RBAC through the actual website using test tokens.