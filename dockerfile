# Use the official Python image from the Docker Hub
FROM python:3.10

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy requirements.txt and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application’s code to the container
COPY . .

# Expose the port your bot will run on
EXPOSE 3000

# Define the command to run your bot
CMD ["python3", "remove_bg_bot.py"]
