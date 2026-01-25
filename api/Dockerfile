# Use a lightweight Node.js version
FROM node:18-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy package files and install dependencies
COPY package.json .
RUN npm install

# Copy the rest of the code
COPY . .

# expose port 3000 to the outside world
EXPOSE 3000

# Command to run the app
CMD ["node", "index.js"]