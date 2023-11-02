# dsp-final-project
(ML Legends) Final Project of Data Science in Production

# Project Title

## Introduction
Welcome to the "Data Science in Production" project by Team “ML Legends”:
- Stephanie Arthaud
- Abubakar Bashir Kankia
- Olanrewaju Adegoke
- Christian Davison Dirisu
- Viet Thai Nguyen

Our project focuses on the Sentiment Analysis of Kindle Book Reviews, aiming to classify them as Positive or Negative. We are utilizing the [Kindle Book Review Dataset], a rich collection of over 2 million reviews and associated metadata for a diverse range of Kindle books.

The dataset, in JSON format, includes attributes such as reviewer ID, product ID, reviewer name, helpful votes of the review, product metadata, review text, product rating, review summary, review time (in both unix and raw formats), and images posted by users after receiving the product.

Our initial step involves creating a Machine Learning model based on the "Kindle Store" reviews. The model's performance and insights will then guide our subsequent steps, including Data Ingestion. The beauty of this approach is that it allows us to extend our model to other datasets with the same schema, providing a robust and scalable solution for sentiment analysis across multiple categories.

## Getting Started
# Getting Started

## Prerequisites

Before you can run the code in this repository, you'll need to have the following software installed on your system:

- Python 3.7 or later
- Git

You'll also need to install several Python libraries. The required libraries are listed in the `requirements.txt` file.

## Installation

1. **Clone the repository**: First, you'll need to clone this repository to your local machine. You can do this by running the following command in your terminal:

```bash
git clone <repository_url>
```
Replace `<repository_url>` with the URL of this repository.

2. **Navigate to the project directory**: Use the following command to navigate to the project directory:

```bash
cd <project_directory>
```
Replace `<project_directory>` with the name of the directory where you cloned the repository.

3. **Install the required Python libraries**: You can install all necessary libraries by running:

```bash
pip install -r requirements.txt
```

Now, you're ready to run the code in this repository!

## Usage

To use this project, you'll need to run specific scripts for data processing, model training, and prediction. Detailed instructions for running these scripts will be provided in subsequent sections of this README.

## File Descriptions
├── api-db
├── app
│   
├── model
project.
├── .gitignore # This is a Git configuration file that specifies which files and directories should be ignored by Git.
├── README.MD # This is a markdown file that typically includes information about our project, such as its purpose, how to install and use it, and how others can contribute.
└── requirements.txt # This file contains a list of all Python libraries that our project depends on. Others can use this file to easily install all necessary libraries using pip.

## Results
Our sentiment analysis model has shown promising results. After training on the "Kindle Store" reviews dataset, the model achieved an accuracy of XX%, a precision of XX%, and a recall of XX%.

Some interesting findings from our analysis include:

1. Finding 1: Briefly describe the finding here.
2. Finding 2: Briefly describe the finding here.
3. Finding 3: Briefly describe the finding here.

These results demonstrate the effectiveness of our approach and provide valuable insights into customer sentiment in Kindle Store reviews.

We plan to extend our model to other datasets with the same schema, which will allow us to perform sentiment analysis across multiple categories.


## Contributing
We welcome contributions to this project! Here's how you can contribute:

1. **Fork the Repository**: Start by forking this repository to your own GitHub account. This allows you to propose changes without access to the main repository.

2. **Clone the Repository**: After forking the repository, clone it to your local machine so you can make changes.

3. **Create a New Branch**: Always create a new branch for each set of changes you want to make. This keeps your changes organized and makes it easier for others to review your contributions.

4. **Make Your Changes**: Make your changes in the new branch. Be sure to follow any coding standards or guidelines provided in the repository.

5. **Commit Your Changes**: Once you've made your changes, commit them with a clear and descriptive commit message.

6. **Push Your Changes**: Push your changes to your forked repository on GitHub.

7. **Submit a Pull Request**: Finally, submit a pull request from your forked repository to the main repository. Include a detailed description of the changes you made and why you made them.

Remember, contributing to open source projects is about more than just code. You can also contribute by reporting bugs, suggesting new features, improving documentation, and more.

Thank you for considering contributing to this project! 😊