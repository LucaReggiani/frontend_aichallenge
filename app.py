from flask import Flask, render_template, request, session
import requests
from forms.add_book_form import AddBookForm
from forms.edit_book_form import EditBookForm
from forms.filter_book_form import FilterBookForm
from forms.login_form import LoginForm
from forms.signup_form import SignupForm
from forms.review_book_form import ReviewBookForm
import json
from flask import redirect, url_for
from werkzeug.security import generate_password_hash

app = Flask(__name__)

@app.route('/filtering', methods = ['POST'])
def filtering():
    request_form = request.form.to_dict(flat=False)

    # Send the dictionary to the remote API
    response = requests.post("http://127.0.0.1:5000/filter_books", json=request_form)
    
    # Check the response status
    if str(response.status_code)[0] == '2':
        # response payload extraction
        data = response.json()

        form_filtering_book = FilterBookForm()
        form_add_book = AddBookForm()
        return render_template('books_list.html', books_list=data, form_add_book=form_add_book, form_filtering_book=form_filtering_book)
    else:
        return redirect(url_for('books_list'))

@app.route('/', methods = ['POST', 'GET'])
def books_list():    
    if request.method == 'POST':
        
        request_form = request.form.to_dict(flat=False)
    
        # Send the dictionary to the remote API
        requests.post("http://127.0.0.1:5000/book_list", json=request_form)
        
        return redirect(url_for('books_list'))
            
    else:
        is_admin = session.get('is_admin')
        resp = requests.get(
                "http://127.0.0.1:5000/book_list"
        )
        # getting the API status code in orer to get if the request succeded
        status_code = resp.status_code
        # checking the status code
        if str(status_code)[0] != '2':
            print("ERROR")
            return render_template('books_list.html')
        
        # response payload extraction
        data = resp.json()

        form_add_book = AddBookForm()
        form_filtering_book = FilterBookForm()
        return render_template('books_list.html', books_list=data, form_add_book=form_add_book, form_filtering_book=form_filtering_book, is_admin=is_admin)


@app.route('/book_<id_book>', methods = ['POST', 'GET'])
def book_details(id_book):

    is_admin = session.get('is_admin')

    if request.method == 'GET':

        # get book's information
        response_get_book_details = requests.get(f"http://127.0.0.1:5000/book_list/{id_book}")
        # getting the API status code in orer to get if the request succeded
        status_code = response_get_book_details.status_code

        # checking the status code
        if str(status_code)[0] != '2':
            print("ERROR")
            return render_template('books_list.html')
        
        # response payload extraction
        data = response_get_book_details.json()

        # main book extraction
        main_book = data[0]

        # main book removal from the response
        data.pop(0)

        # book's page forms initialization
        form_edit_book = EditBookForm(obj=main_book)
        form_review_book = ReviewBookForm()

        # getting all book's reviews information
        book_reviews = requests.get(f"http://127.0.0.1:5000/reviews/{id_book}")
        book_reviews = book_reviews.json()

        # Checking if the user il logged in
        userId = session.get('userId', None)
        return render_template('book_page.html', 
                               book=main_book,
                               suggested_books=data, 
                               form_edit_book=form_edit_book, 
                               is_admin=is_admin, 
                               form_review_book=form_review_book, 
                               book_reviews=book_reviews, 
                               userId=userId)
    
    else:
        edited_book = request.form.to_dict(flat=False)
        
        edited_book_id = edited_book.get("bookId")[0]
        
        # Send the dictionary to the remote API
        requests.put("http://127.0.0.1:5000/book_list/{edited_book_id}", json=edited_book)

        return redirect(url_for('book_details', id_book=edited_book_id))


@app.route('/delete_<book_id>')
def delete_book(book_id):

    url = f"http://127.0.0.1:5000/book_list/{book_id}"

    try:
        response = requests.delete(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        
        print(response.json())  # Print the JSON response

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    return redirect(url_for('books_list'))

@app.route('/update_order', methods=['POST'])
def update_order():

    data = request.get_json() 

    api_url = 'http://127.0.0.1:5000/book_list/ordering'

    # Make a request to the external API and pass the data variable
    response = requests.post(api_url, json=data)

    # Check the status code of the response
    if response.status_code == 200:
        # Successful response from the external API
        api_response = response.json()

        return api_response
    else:
        # Unsuccessful response from the external API
        return redirect(url_for('books_list'))


@app.route('/user_review/<book_id>', methods=['POST'])
def user_review(book_id):
    request_form = request.form.to_dict(flat=False)
    api_url = f"http://127.0.0.1:5000/reviews/{book_id}"

    # Retrieve values from session
    userId = session.get('userId', None)
    # Include cookies in the JSON payload
    data = {
        "form_data": request_form,
        "userId": userId,
    }

    response = requests.post(api_url, json=data)

    # Check the response status
    if response.status_code != 201:
        pass
        # message = response.content
    return redirect(url_for('books_list'))


@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    email = session.get('email')
    
    if request.method == 'GET':

        if email: # if user is logged
            name = session.get('name')
            return render_template('user_page.html', name=name)
        else:
            form_login = LoginForm()
            return render_template('login.html', form_login=form_login, message="")
        
    else:
        request_form = request.form.to_dict(flat=False)
        api_url = 'http://127.0.0.1:5000/login'

        # Make a request to the external API and pass the data variable
        response = requests.post(api_url, json=request_form)

        # Check the response status
        if response.status_code == 200:
            api_response = response.json()  # Get the response from the API
            user = api_response['user']
            # Store user information in the session
            session['userId'] = user['userId']
            session['name'] = user['name']
            session['lastname'] = user['lastname']
            session['email'] = user['email']
            session['is_admin'] = user['is_admin']
            return redirect(url_for('books_list'))
        else:
            message = "Email or password are incorrect! If you did not register yet, click on the link under the form."
            form_login = LoginForm()
            return render_template('login.html', form_login=form_login, message=message)


@app.route('/signup_user', methods=['GET', 'POST'])
def signup_user():
    if request.method == 'GET':
        form_signup = SignupForm()
        return render_template('signup.html', form_signup=form_signup, message="")
    
    else:
        request_form = request.form.to_dict(flat=False)
        password = request_form['password'][0]
        hashed_password = generate_password_hash(password, method='pbkdf2')
        request_form['password'] = [hashed_password]
        
        api_url = 'http://127.0.0.1:5000/signup'

        # Make a request to the external API and pass the data variable
        response = requests.post(api_url, json=request_form)

        # Check the response status
        if response.status_code == 201:
            # api_response = response.json()  # Get the response from the API
            # res = jsonify(api_response)  # Return the API response as JSON to the frontend
            return redirect(url_for('user_login'))
        else:
            message = "User already registered! Please, log in."
            form_login = LoginForm()
            return render_template('login.html', form_login=form_login, message=message)

@app.route('/logout_user')
def logout_user():
    # Clear user information from the session
    session.pop('userId', None)
    session.pop('name', None)
    session.pop('lastname', None)
    session.pop('email', None)
    session.pop('is_admin', None)
    return redirect(url_for('user_login'))

if __name__ == '__main__':
    # set up the variable regarding the secret key in this app
    app.config['SECRET_KEY'] = "SECRET"
    app.run(debug=True, port=5505)