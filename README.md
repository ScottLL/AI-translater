# AI Translate Summary

result: https://ai-translate-summary.azurewebsites.net/
(get the OpenAI API key from https://openai.com/)

AI-translater is a Python application that leverages machine learning techniques to translate text from one language to another. The application is built using the Google Cloud Translation API and the pre-trained TensorFlow Transformer model. It supports multiple languages and can handle both text and file input.

# Summary
In addition to translation, AI-translater also includes a summary feature that leverages OpenAI's GPT-3 API to generate a summary of the translated text. The summary feature uses natural language processing techniques to identify the most important information in the text and condense it into a shorter, more digestible format.

# Installation
To install AI-translater, you need to have Python 3.x and pip installed on your system. You can install the necessary packages by running the following command in your terminal:

> pip install -r requirements.txt

# Usage
To use AI-translater, simply run the app.py file and follow the instructions on the command line. The application will prompt you to enter the source and target languages, as well as the input text or file. Once you provide the necessary information, the application will translate the text and display the output on the command line.

Here is an example of how to use AI-translater:

> python app.py

# Deployment on Azure
AI-translater can be easily deployed on Microsoft Azure, a cloud computing platform that allows you to build, deploy, and manage applications and services. Deploying AI-translater on Azure provides a scalable, secure, and reliable solution for translating and summarizing text.

To deploy AI-translater on Azure, follow these steps:

1. Create an Azure account if you don't already have one.

2. Create a new web app on Azure. You can do this through the Azure portal, Azure CLI, or Azure PowerShell. Make sure to select the appropriate subscription, resource group, and region.

3. Upload the translator.py file and the requirements.txt file to the web app using FTP or the Azure portal.

4. Install the required packages by running the following command in the Azure CLI:

> pip install -r requirements.txt

5. Configure the web app to use Python 3.7 or later and the translator.py file as the startup command. You can do this through the Azure portal by navigating to the Configuration settings for the web app.

6. Set up the necessary environment variables for AI-translater. You will need to set the following environment variables:

GOOGLE_APPLICATION_CREDENTIALS: Path to the Google Cloud Translation API credentials file.
OPENAI_API_KEY: API key for the OpenAI API.
AZURE_STORAGE_CONNECTION_STRING: Connection string for Azure Blob storage (used for caching translations and summaries).
You can set environment variables through the Azure portal by navigating to the Application settings for the web app.

7. Restart the web app to apply the changes.

8. Test the application by navigating to the URL of the web app in a web browser.

For more detailed instructions on deploying Python applications on Azure, please refer to the Azure documentation.

Please note that deploying AI-translater on Azure may incur additional costs, depending on the size and usage of the web app service. It is important to monitor the usage and scale the application accordingly to avoid unexpected costs.


# Contributing
If you would like to contribute to AI-translater, feel free to submit a pull request or open an issue on the GitHub repository. Any feedback or suggestions are also welcome.