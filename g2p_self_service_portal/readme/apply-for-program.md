# Self Service Portal-Apply for program

## Introduction
In this repo the logged in user can apply for the listed programs if they have not applied.

## Steps
When you go to list of all programs and apply for any of the program you will be redirected to the application form of that program and you can fill out the form and can apply for the program or can cancel the application.

**__Note__**: If form is not mapped with the program. Refer this repo [Form mapping with Program]() for mapping form to program.


### When you `submit` the Applicaton ###

If you submit the application it will checking for the required fields. if all required fields are not filled you will get a toast message in the top right side with a error message to fill all the required fields. Along wih the toast message you will also get error message beow the required field and there input box border color will also change.

    List of all the error messages:
       1. If type is checkbox and radio
           eror message: Please select <field_name>
           
           example: let say we have gender field and it is required but not filled then the error message will be- please select gender
       
       2. Remaining data type
           error message: Please enter <field_name>

Along with the required fields it will also check for the valid data type.

    List of all validation messages:
        1. data type is email
            validaton message: Please enter a valid email address
           
        2. data type is url
            validaton message: Please enter a valid url
            
        3. data type is tel
             validaton message: Please enter a valid telephone number

**__Note__**: Both the error message and validation message will not be displayed simultaneously.

When all the required field and valid data type is entered your application will be submitted for that particular program and an application id containing 11 digits will be generated having submission date followed by 5 digit sequence number starting from 00001.

### When you `cancel` the Applicaton ###

If you cancel the application you will get a popup message with __discard__ and __cancel__ buttons. The cancel button will cancel the popup and you can continue with the application form while clicking on the ‘discard’ button will redirect you to the all programs list and your filled data will not be saved.