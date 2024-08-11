# Use Ubuntu with the specified BuildID
FROM ubuntu@sha256:0702430aef5fa3dda43986563e9ffcc47efbd75e

# Set the working directory in the container
WORKDIR /app

# Update and install Python 3 and pip
RUN apt-get update && apt-get install -y python3 python3-pip curl

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
# (You may need to adjust this if your bot uses a different port)
EXPOSE 80

# Run discord_bot.py when the container launches
CMD ["python3", "src/discord_bot/discord_bot.py"]