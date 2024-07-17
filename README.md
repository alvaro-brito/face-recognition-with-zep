# Facial Recognition Service with FastAPI and Zep

## Introduction
This project demonstrates the creation of a facial recognition service using FastAPI and Zep, a robust vector database. The service utilizes a celebrity face image dataset from Kaggle to build a system capable of recognizing and identifying faces in new photos by comparing them to a preloaded database of celebrity faces.

## Dataset
The dataset used for this project can be found [here](https://www.kaggle.com/datasets/vishesh1412/celebrity-face-image-dataset).

## Goal
The goal is to develop a facial recognition service that:
- Loads a database of celebrity faces.
- Generates embeddings for each image.
- Adds these embeddings to a Zep vector database.
- Recognizes and identifies faces in new photos by comparing them to the database.

## Real-World Problem
Facial recognition is essential in domains such as security, user authentication, and personalized user experiences. Traditional databases are inefficient for storing and querying high-dimensional data like image embeddings. Vector databases like Zep provide efficient storage, indexing, and retrieval of vectorized data, making them ideal for this task.

## Solution Approach
We create a FastAPI application that:
- Loads the celebrity face dataset and generates embeddings.
- Stores these embeddings in Zep.
- Provides endpoints to add new images and recognize faces.

## Hands-on Implementation

### Step 1: Download the Example Project
First, ensure you have everything you need. Download the complete example at: [Github Repository](https://github.com/alvaro-brito/face-recognition-with-zep)

### Step 2: Starting Docker Compose
After downloading the project, navigate to the project directory.

The provided `docker-compose.yml` file includes services for PostgreSQL, Zep NLP server, and Zep. Note that you must provide an OpenAI API key by setting the environment variable `ZEP_OPENAI_API_KEY` as Zep is a vector database that automatically executes embeddings with LLMs (OpenAI, Gemini, etc.). However, in this example, we will create our embeddings manually for images and will not use this automatic embedding feature, but if you miss the `ZEP_OPENAI_API_KEY`, `docker-compose` will not work correctly.

```sh
docker-compose up -d
```

The Zep service will be accessible at [http://localhost:8000](http://localhost:8000).

### Step 3: Running the Project
First, install the dependencies:

```sh
pip install -r requirements.txt
```

Run the project:

```sh
uvicorn main:app --reload --port 18000
```

### Step 4: Loading the Image Database
To load our image database, execute the bash script `upload_images.sh`:

```sh
./upload_images.sh
```

This script will take some time to complete as it uploads around 600 photos using our `/add-image` API endpoint.

### Step 5: Testing the Facial Recognition
Once the uploads are finished, we can test the facial recognition by running the `recognize_tests.sh` script:

```sh
./recognize_tests.sh
```

This script will validate 4 photos against our database to ensure that the facial recognition is working correctly.
