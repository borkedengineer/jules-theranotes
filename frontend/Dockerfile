# Frontend Dockerfile - Development version
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Expose port
EXPOSE 3000

# Set environment variables
ENV NODE_ENV=development
ENV PORT=3000
ENV HOSTNAME=0.0.0.0

# Start the development server
CMD ["npm", "run", "dev"]