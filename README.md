# Library Management System using flask

A very basic library management system made using python flask, front-end technologies like HMTL5, CSS, Javascript, Jquery.
For database I have used MongoDB Atlas for ease of use.




## The webapp will offer the following 3 basic pages:


### 1. Books and  Members

- In this page a table will display title, authors, isbn, publisher, pages and stock left of the books in the database and the member details for the member
 table stored in the databse.
- There is an option to import books from the link that was provided in the dev test page.
- We can add new books, delete and edit the book details.
- DataTables has been used for enhancing the functionalities of the table elements, it allows you to search the table for any keyword and will match with content of all 
the columns.

### 3. Transactions
- There is an option to add transacitons which will let you choose between a return and rent option. Renting checks whether the selected use's debt(unpaid rent) is less than or 
equal to 500 or else it will display an error message.
- For dynamic search and selection I have used 'Chosen'. Chosen is a jQuery plugin that makes long, unwieldy select boxes much more user-friendly.


# Screenshots

![image](https://user-images.githubusercontent.com/36098155/111810306-e1b77e80-88fb-11eb-894f-198cabbc9887.png)
![image](https://user-images.githubusercontent.com/36098155/111811098-b6815f00-88fc-11eb-876d-d71eee30c9e8.png)
![image](https://user-images.githubusercontent.com/36098155/111811248-dd3f9580-88fc-11eb-990c-eaec8a91ac4e.png)
![image](https://user-images.githubusercontent.com/36098155/111811292-e9c3ee00-88fc-11eb-9ede-6c46e59b2434.png)


## CRUD Operations
### 1. Adding members and books
<img src= 'https://user-images.githubusercontent.com/36098155/111812123-ca799080-88fd-11eb-8bc9-a43ce4299d74.png' width="50%" height ='50%'>
<img src= 'https://user-images.githubusercontent.com/36098155/111812881-8a66dd80-88fe-11eb-8c25-bf3838d8597a.png' width="60%" height ='70%'> 
<img src= 'https://user-images.githubusercontent.com/36098155/111813855-c2baeb80-88ff-11eb-98ab-1fa7b7facbf7.png' width="60%" height ='70%'> 
<img src= 'https://user-images.githubusercontent.com/36098155/111813956-e54d0480-88ff-11eb-83ef-1263d227c38d.png' width="60%" height ='70%'> 


### 2. Deleting members and books
<img src='https://user-images.githubusercontent.com/36098155/111813649-77a0d880-88ff-11eb-85d6-0b6832c5128c.png' width="60%" height ='70%'>
<img src='https://user-images.githubusercontent.com/36098155/111814767-e03c8500-8900-11eb-9138-bdca3c7a8107.png' width="60%" height ='70%'>
<img src='https://user-images.githubusercontent.com/36098155/111814841-f5191880-8900-11eb-8e6e-9763206a6938.png' width="60%" height ='70%'>
<img src='https://user-images.githubusercontent.com/36098155/111815235-71136080-8901-11eb-9ede-cb71dcdac622.png' width="60%" height ='70%'>

### 3. Updating members and books
<img src='https://user-images.githubusercontent.com/36098155/111817603-3232da00-8904-11eb-87b4-7552b6e80912.png' width="60%" height ='70%'>
<img src='https://user-images.githubusercontent.com/36098155/111827563-09b0dd00-8910-11eb-94dc-d7fa8d5372ac.png' width="60%" height ='70%'>
<img src='https://user-images.githubusercontent.com/36098155/111827801-598fa400-8910-11eb-9bf2-084ca6480c53.png' width="60%" height ='70%'>
<img src='https://user-images.githubusercontent.com/36098155/111827883-72985500-8910-11eb-92ec-4a1794fdee49.png' width="60%" height ='70%'>


### 4. Transaction Rent/Return
<img src='https://user-images.githubusercontent.com/36098155/111828697-afb11700-8911-11eb-910f-980e3d5b69d9.png' width="60%" height ='70%'>
<img src='https://user-images.githubusercontent.com/36098155/111828721-b9d31580-8911-11eb-891c-2e869989718c.png' width="60%" height ='70%'>
**Updation of debt**
<img src='https://user-images.githubusercontent.com/36098155/111828814-db340180-8911-11eb-920b-4b6b3a463583.png' width="60%" height ='70%'>

### 5. Crossing Debt limit of 500
<img src='https://user-images.githubusercontent.com/36098155/111829577-de7bbd00-8912-11eb-88dd-d36f7920aca0.png' width="60%" height ='70%'>

   
