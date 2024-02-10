from flask import Flask, render_template, request, redirect, url_for
from Forms import CreateChefForm, CreateCoursesForm, CreateCustomerForm, CreateIngrForm

from Chef import Chef
from Course import Course
from Customer import Customer
from Ingredients import Ingr
import SQLDB
from SQLDB import *
from login import *   
from login import LoginForm  
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


############################## START HOME ############################

@app.route('/')
def Home():
    return render_template('homepage.html')

############################## END HOME ############################



############################## START COURSE FRONT END ############################

@app.route('/course')
def courseFront():
    return render_template('courses.html')

############################## END COURSE FRONT END ############################


############################## START CHEF FRONT END ############################

@app.route('/chef')
def chefs_front():
    chefs = get_chefs_data(limit=3)  # Limit to 3 chefs
    return render_template('chefs.html', chefs=chefs)

############################## END CHEF FRONT END ############################




############################## START LOGIN FRONT END ############################

@app.route('/login')
def loginFront():
    return render_template('login.html')

############################## END LOGIN FRONT END ############################




############################## START CREATE ACCOUNT FRONT END ############################

@app.route('/createAccount')
def createAccFront():
    return render_template('createaccount.html')

############################## END CREATE ACCOUNT FRONT END ############################



############################## START FORGOT PASSWORD FRONT END ############################

@app.route('/forgotPassword')
def forgotPasswordFront():
    return render_template('forgotpassword.html')

############################## END FORGOT PASSWORD FRONT END ############################



############################## START PWRESETEMAILSENT FRONT END ############################

@app.route('/pwresetemailsent', methods=['POST'])
def pwresetemailsent():
    return render_template('pwresetemailsent.html')



############################## END PWRESETEMAILSENT FRONT END ############################




############################## START RESETPASSWORD FRONT END ############################

@app.route('/resetpassword', methods=['POST'])
def resetpassword():
    return render_template('resetpassword.html')



############################## END RESETPASSWORD FRONT END ############################



############################## START RESETSUCCESSFUL FRONT END ############################

@app.route('/resetsuccessful', methods=['POST'])
def resetsuccessful():
    return render_template('resetsuccessful.html')



############################## END RESETSUCCESSFUL FRONT END ############################






############################## START STAFF ############################

@app.route('/staff')
def staffHome():
    if 'username' in session and session['username'] == 'admin':  # Check if 'username' is in session and is 'admin'
        return render_template('staff.html')  # Render the staff home page
    else:
        return redirect(url_for('login'))

############################## END STAFF ############################



@app.route('/createChef', methods=['GET', 'POST'])
def create_chef():
    create_chef_form = CreateChefForm(request.form)
    if request.method == 'POST' and create_chef_form.validate():

        new_chef = Chef(create_chef_form.full_name.data, create_chef_form.gender.data, create_chef_form.contact.data,
                        create_chef_form.email.data, create_chef_form.introduction.data)

        SQLDB.add_chef(new_chef)

        return redirect(url_for('retrieve_chefs'))
    return render_template('createChef.html', form=create_chef_form)


@app.route('/retrieveChefs')
def retrieve_chefs():
    chef_list = SQLDB.get_chef_list()

    return render_template('retrieveChefs.html', count=len(chef_list), chefs_list=chef_list)


@app.route('/updateChef/<int:id>/', methods=['GET', 'POST'])
def update_chef(id):
    update_chef_form = CreateChefForm(request.form)

    if request.method == 'POST' and update_chef_form.validate():
        chef = Chef(update_chef_form.full_name.data, 
                    update_chef_form.gender.data, 
                    update_chef_form.contact.data,
                    update_chef_form.email.data, 
                    update_chef_form.introduction.data)

        chef.set_chef_id(id)
        SQLDB.update_chef(chef)

        return redirect(url_for('retrieve_chefs'))

    else:
        chef = SQLDB.get_chef(id)
        update_chef_form.full_name.data = chef.get_full_name()
        update_chef_form.gender.data = chef.get_gender()
        update_chef_form.contact.data = chef.get_contact()
        update_chef_form.email.data = chef.get_email()
        update_chef_form.introduction.data = chef.get_introduction()

        return render_template('updateChef.html', form=update_chef_form)


@app.route('/deleteChef/<int:id>', methods=['POST'])
def delete_chef(id):
    SQLDB.remove_chef(id)

    return redirect(url_for('retrieve_chefs'))

############################## END CHEF ################################


############################## START COURSE ############################

@app.route('/createCourse', methods=['GET', 'POST'])
def create_course():
    create_course_form = CreateCoursesForm(request.form)

    # Fetch chef names
    chef_names = SQLDB.get_chef_names()

    # Populate choices for the chef_name field
    create_course_form.chef_name.choices = [(name, name) for name in chef_names]

    if request.method == 'POST' and create_course_form.validate():
        # Add course
        new_course = Course(
            cuisine=create_course_form.cuisine.data,
            chef_name=create_course_form.chef_name.data,
            availability=create_course_form.availability.data,
            sessionTime=create_course_form.sessionTime.data,
            description=create_course_form.description.data
        )
        SQLDB.add_course(new_course)

        return redirect(url_for('retrieve_courses'))

    return render_template('createCourse.html', form=create_course_form)


@app.route("/retrieveCourse")
def retrieve_courses():
    course_list = SQLDB.get_course_list()
    #convert dict to list
    return render_template("retrieveCourses.html", count=len(course_list), course_list=course_list)


@app.route('/updateCourse/<int:id>/', methods=['GET', 'POST'])
def update_course(id):
    """update_course_form = CreateCoursesForm(request.form)
    
    if request.method == 'POST' and update_course_form.validate():
        course = Course(update_course_form.cuisine.data, 
                        update_course_form.chef_name.data, 
                        update_course_form.availability.data, 
                        update_course_form.sessionTime.data, 
                        update_course_form.description.data)
        
        course.set_courseID(id)
        SQLDB.update_course(course)
        return redirect(url_for('retrieve_courses'))
    else:
        course = SQLDB.get_course(id)
        update_course_form.cuisine.data = course.get_cuisine()
        update_course_form.chef_name.data = course.get_chef_name()
        update_course_form.availability.data = course.get_availability()
        update_course_form.sessionTime.data = course.get_sessionTime()
        update_course_form.description.data = course.get_description()"""
        
    update_course_form = CreateCoursesForm(request.form)

    # Fetch chef names
    chef_names = SQLDB.get_chef_names()

    # Populate choices for the chef_name field
    update_course_form.chef_name.choices = [(name, name) for name in chef_names]

    if request.method == 'POST' and update_course_form.validate():
        # Update course
        updated_course = Course(
            cuisine=update_course_form.cuisine.data,
            chef_name=update_course_form.chef_name.data,
            availability=update_course_form.availability.data,
            sessionTime=update_course_form.sessionTime.data,
            description=update_course_form.description.data
            )  # Use a function to get chef_id by name
        

        updated_course.set_courseID(id)
        SQLDB.update_course(updated_course)
        return redirect(url_for('retrieve_courses'))

    else:
        course = SQLDB.get_course(id)
        update_course_form.cuisine.data = course.get_cuisine()
        update_course_form.chef_name.data = course.get_chef_name()
        update_course_form.availability.data = course.get_availability()
        update_course_form.sessionTime.data = course.get_sessionTime()
        update_course_form.description.data = course.get_description()
    # Fetch the course details
    
    
    """# Set the choices for the chef_name field
    update_course_form.chef_name.choices = [(name, name) for name in chef_names]

    # Set the form data with the course details
    update_course_form.process(obj=course)"""
    
    return render_template('updateCourse.html', form=update_course_form)


@app.route('/deleteCourse/<int:id>', methods=['POST'])
def delete_course(id):
    SQLDB.remove_course(id)

    return redirect(url_for('retrieve_courses'))


############################## END COURSE ############################



############################## START CUSTOMER ############################
@app.route('/createCustomer', methods=['GET', 'POST'])
def create_customer():
    create_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and create_customer_form.validate():

        new_customer = Customer(
            create_customer_form.cust_first_name.data,
            create_customer_form.cust_last_name.data,
            create_customer_form.cust_gender.data,
            create_customer_form.cust_email.data,
            create_customer_form.cust_birthday.data,
            create_customer_form.cust_address.data,
            create_customer_form.cust_mobile_number.data,
            create_customer_form.cust_username.data,
            create_customer_form.cust_password.data
        )
        # Add the new customer to the database
        SQLDB.add_customer(new_customer)

        return redirect(url_for('retrieve_customers'))
    return render_template('createCustomer.html', form=create_customer_form)

@app.route('/retrieveCustomer')
def retrieve_customers():
    customer_list = SQLDB.get_customer_list()

    return render_template('retrieveCustomer.html', count=len(customer_list), customers_list=customer_list)

@app.route('/updateCustomer/<int:id>/', methods=['GET', 'POST'])
def update_customer(id):
    update_customer_form = CreateCustomerForm(request.form)

    if request.method == 'POST' and update_customer_form.validate():
        customer = Customer(
            update_customer_form.cust_first_name.data,
            update_customer_form.cust_last_name.data,
            update_customer_form.cust_gender.data,
            update_customer_form.cust_email.data,
            update_customer_form.cust_birthday.data,
            update_customer_form.cust_address.data,
            update_customer_form.cust_mobile_number.data,
            update_customer_form.cust_username.data,
            update_customer_form.cust_password.data
        )

        customer.set_customer_id(id)
        SQLDB.update_customer(customer)

        return redirect(url_for('retrieve_customers'))
    else:
        customer = get_customer(id)
        update_customer_form.cust_first_name.data = customer.get_cust_first_name()
        update_customer_form.cust_last_name.data = customer.get_cust_last_name()
        update_customer_form.cust_gender.data = customer.get_cust_gender()
        update_customer_form.cust_email.data = customer.get_cust_email()
        update_customer_form.cust_birthday.data = customer.get_cust_birthday()
        update_customer_form.cust_address.data = customer.get_cust_address()
        update_customer_form.cust_mobile_number.data = customer.get_cust_mobile_number()
        update_customer_form.cust_username.data = customer.get_cust_username()
        update_customer_form.cust_password.data = customer.get_cust_password()

        return render_template('updateCustomer.html', form=update_customer_form)

@app.route('/deleteCustomer/<int:id>', methods=['POST'])
def delete_customer(id):
    SQLDB.remove_customer(id)

    return redirect(url_for('retrieve_customers'))

############################## END CUSTOMER ############################

############################## START INGREDIENT ############################


### CREATE INGREDIENT ###

@app.route('/createIngr', methods=['GET', 'POST'])
def create_ingr():
    create_ingr_form = CreateIngrForm(request.form)
    if request.method == 'POST' and create_ingr_form.validate():

        new_ingr = Ingr(create_ingr_form.name.data, create_ingr_form.category.data, create_ingr_form.qty.data, create_ingr_form.cost.data)

        SQLDB.add_ingr(new_ingr)

        return redirect(url_for('retrieve_ingr'))
    return render_template('createIngr.html', form=create_ingr_form)


@app.route('/retrieveIngr')
def retrieve_ingr():
    ingr_list = SQLDB.get_ingr_list()

    return render_template('retrieveIngr.html', count=len(ingr_list), ingr_list=ingr_list)


@app.route('/updateIngr/<int:id>/', methods=['GET', 'POST'])
def update_ingr(id):
    update_ingr_form = CreateIngrForm(request.form)

    if request.method == 'POST' and update_ingr_form.validate():
        ingr = Ingr(update_ingr_form.name.data, update_ingr_form.category.data, update_ingr_form.qty.data,
                    update_ingr_form.cost.data)

        ingr.set_ingr_id(id)
        SQLDB.update_ingr(ingr)

        return redirect(url_for('retrieve_ingr'))

    else:
        ingr = SQLDB.get_ingr(id)
        update_ingr_form.name.data = ingr.get_name()
        update_ingr_form.category.data = ingr.get_category()
        update_ingr_form.qty.data = ingr.get_qty()
        update_ingr_form.cost.data = ingr.get_cost()

        return render_template('updateIngr.html', form=update_ingr_form)


@app.route('/deleteIngr/<int:id>', methods=['POST'])
def delete_ingr(id):
    SQLDB.remove_ingr(id)

    return redirect(url_for('retrieve_ingr'))

############################## END INGREDIENT ################################





############################## START CHATBOT ################################









############################## END CHATBOT ################################




@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        session['username'] = form.login_username.data
        if form.login_username.data == 'admin' and  session['username'] == "admin" :
            return redirect(url_for('staffHome'))
        else:
            return redirect(url_for('Home'))
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)


