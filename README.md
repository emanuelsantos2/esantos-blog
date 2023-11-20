# esantos-blog

### How to run Locally:
Clone repository  
pip install -r requirements.txt  
Populate .ENV file  
python app.py  



### `/posts`:
### `GET` Method:
## Insert a new post.

### Request:
- **Method**: `POST`
- **Accept Header**: `application/json`

- **JSON Request Body**:
  - `title` (str, required): Title of the new post.
  - `html_content` (str): HTML content of the new post.
  - `user_id` (int, required): ID of the user creating the post.
  - `category_id` (int): ID of the category to which the post belongs.

### Response:
- **Status Codes**:
  - `201 Created`: Successful creation of a new post in JSON format.
  - `400 Bad Request`: Invalid request if the required `title` is missing.

- **JSON Response**:
  - Returns a JSON object with the following attributes:
    - `title` (str): Title of the newly created post.
    - `html_content` (str): HTML content of the newly created post.

### Example Usage:
- To create a new post, send a `POST` request with a JSON payload containing the required fields.

### Notes:
- The route expects a JSON payload in the request body with at least the `title` field.
- If successful, the route returns a JSON response with the details of the newly created post.
- Returns a `400 Bad Request` status if the required `title` is missing.


### `/posts/<int:id>`:

### `GET` Method:
## Get a single post.
#### Request:

-   Method: `GET`
-   Accept Header: `application/json` (Optional)

#### Response:

-   Status Codes:

    -   `200 OK`: Successful retrieval of post details in JSON format.
    -   `200 OK`: Successful retrieval of post details in HTML format if 'Accept' header does not specify JSON.
-   JSON Response:

    -   If 'Accept' header includes `application/json`, returns a JSON object with the following attributes:
        -   `id` (int): Unique identifier for the post.
        -   `title` (str): Title of the post.
        -   `html_content` (str): HTML content of the post.
-   HTML Response:

    -   If 'Accept' header does not specify JSON, returns an HTML representation of the post using the `post.html` template.

* * * * *

### `PUT` Method:
## Update a single post.
#### Request:

-   Method: `PUT`

-   Accept Header: `application/json`

-   JSON Request Body:

    -   `title` (str): New title for the post.
    -   `html_content` (str): New HTML content for the post.
    -   `category_id` (int): New category ID for the post.

#### Response:

-   Status Codes:

    -   `202 Accepted`: Successful update of the post.
-   JSON Response:

    -   Returns a JSON object with the message "Updated Successfully."

* * * * *

### `DELETE` Method:
## Delete a single post.
#### Request:

-   Method: `DELETE`
-   Accept Header: `application/json`

#### Response:

-   Status Codes:

    -   `204 No Content`: Successful deletion of the post.
-   JSON Response:

    -   Returns a JSON object with the message "Deleted Successfully."
 
### `/categories`:
### `POST` Method:

#### Request:

-   Method: `POST`

-   Accept Header: `application/json`

-   JSON Request Body:

    -   `name` (str, required): Name of the new category.

#### Response:

-   Status Codes:

    -   `201 Created`: Successful creation of a new category in JSON format.
    -   `400 Bad Request`: Invalid request if the required `name` is missing.
-   JSON Response:

    -   Returns a JSON object with the following attributes:
        -   `id` (int): Unique identifier for the newly created category.
        -   `name` (str): Name of the newly created category.

#### Example Usage:

-   To create a new category, send a `POST` request with a JSON payload containing the required `name` field.

#### Notes:

-   The route expects a JSON payload in the request body with at least the `name` field.
-   If successful, the route returns a JSON response with the details of the newly created category.
-   Returns a `400 Bad Request` status if the required `name` is missing.

* * * * *

### `GET` Method:

#### Request:

-   Method: `GET`
-   Accept Header: `application/json` (Optional)

#### Response:

-   Status Codes:

    -   `200 OK`: Successful retrieval of all categories in JSON format.
    -   `400 Bad Request`: Invalid request if the 'Accept' header does not specify JSON.
-   JSON Response:

    -   If 'Accept' header includes `application/json`, returns a JSON array containing objects with the following attributes:
        -   `id` (int): Unique identifier for the category.
        -   `name` (str): Name of the category.
-   Notes:

    -   If 'Accept' header does not specify JSON, returns a `400 Bad Request` status.
 
### `/categories/<int:id>`:
### `DELETE` Method:

#### Request:

-   Method: `DELETE`
-   Accept Header: `application/json`

#### Response:

-   Status Codes:

    -   `204 No Content`: Successful deletion of the category.
-   JSON Response:

    -   Returns a JSON object with the message "Deleted Successfully."

* * * * *

### `PUT` Method:

#### Request:

-   Method: `PUT`

-   Accept Header: `application/json`

-   JSON Request Body:

    -   `name` (str): New name for the category.

#### Response:

-   Status Codes:

    -   `202 Accepted`: Successful update of the category.
-   JSON Response:

    -   Returns a JSON object with the message "Updated Successfully."

#### Example Usage:

-   To update a category, send a `PUT` request with a JSON payload containing the new `name` field.

#### Notes:

-   The route expects a JSON payload in the request body with at least the `name` field for the `PUT` method.
-   Returns a `400 Bad Request` status if the 'Accept' header does not specify JSON for the `PUT` method.

### `/img_upload`:
### `POST` Method:

#### Request:

-   Method: `POST`
-   Authorization: Requires authentication (User must be logged in).
-   Content-Type: `multipart/form-data`

#### Request Body:

-   The body of the request should contain a file part named `file` with the image to be uploaded.

#### Response:

-   Status Codes:

    -   `201 Created`: Successful upload of the image.
    -   `400 Bad Request`: Invalid request if the file part is missing or empty, or if the file type is not allowed.
-   JSON Response:

    -   Returns a JSON object with the following attribute:
        -   `file_url` (str): URL of the uploaded image.

#### Example Usage:

-   To upload an image, send a `POST` request with the file part named `file` containing the image to be uploaded. The request should include authentication headers.

#### Notes:

-   The route requires the user to be logged in (`login_required` decorator).
-   Expects a `multipart/form-data` request with a file part named `file`.
-   Returns a `400 Bad Request` status if the file part is missing, empty, or if the file type is not allowed.
