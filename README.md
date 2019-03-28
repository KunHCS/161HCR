[**API Instruction**](#api-instruction)

# Handwritten Character Recognition
This project uses machine learning algorithm to recognize hand written characters


## Git Setup
Clone to local directory

	git clone https://github.com/KunHCS/161HCR.git

## React Setup
**Under /client directory**

Install dependencies

	npm install

Build React for production

	npm run build

For testing only

	npm start

## Flask Setup
**Under project root directory**

Install dependencies

	pip install -r pip_requirements.txt

To start the backend server

	python run.py

## Anaconda Environment Setup
Creating Anaconda environment  for development

	conda create --name <env_name> --file conda_requirements.txt

# API Instruction

## *User Input Image*
#### http://127.0.0.1:5000/image (POST)
**[React image upload example](https://www.academind.com/learn/react/snippets/image-upload/ "React image upload example")**
##### Request body (form-data):
	{
		"image": <image file>,
	}
### Responses:
Status: 200 OK

Status: 400 BAD REQUEST
