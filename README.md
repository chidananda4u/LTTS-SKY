# LTTS-SKY
BITRIX Assessment

Basics
Fork/Clone
Activate a virtualenv
Install the requirements

Set Environment Variables

export FLASK_APP

Run the Application

flask run

There are two services and oe auth end point

1.) To generate JWT token - http://localhost:5000/api/v1/auth/generate_token
2.) To get market summarries - http://127.0.0.1:5000/api/v1/market/summaries
3.) To get a market symbol - http://localhost:5000/api/v1/markets/summary?market=<market_symbol>

The market summaries and market symbol are authenticated and needs JWT token to be accessed.

first we need to generate JWT token

![image](https://user-images.githubusercontent.com/107303703/233754171-fa3b88ba-e1ad-4cc5-a908-dfb3ef28fe9a.png)

then we need to copy the token and pass in the header of the other services 
1.) To get market summarries
- header name is 'x-access-tokens'
![image](https://user-images.githubusercontent.com/107303703/233754254-9181c69d-3e78-438b-84ed-cfc49999b44c.png)

then we can send request for getting market summarries.
![image](https://user-images.githubusercontent.com/107303703/233754288-cbd9cd4d-3f11-4355-aa16-7c4d5ea08f93.png)

2.)To get a market symbol
- header name is 'x-access-tokens'
![image](https://user-images.githubusercontent.com/107303703/233754358-d2b07132-b4aa-4a3d-8957-caa4e9393057.png)

then we have to come to params and give param symbol for the required market symbol
![image](https://user-images.githubusercontent.com/107303703/233754400-4a735ef9-55f3-4b4c-b926-b2a6a386eaee.png)

we can send request for getting market symbol.
![image](https://user-images.githubusercontent.com/107303703/233754433-8e82c5de-bd8e-477a-bc54-96760bc5610c.png)





