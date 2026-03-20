FROM python:3.10-alpine3.22

# Set the working directory inside the container
WORKDIR /app

# Install build dependencies
RUN apk add --no-cache build-base

# Fix for Alpine/musl: Create a symlink for sys/unistd.h
# This is required because pyeda's picosat solver uses legacy glibc paths
RUN mkdir -p /usr/include/sys && ln -s /usr/include/unistd.h /usr/include/sys/unistd.h

# Set Compiler flags for legacy C code (Fixes pyeda build)
ENV CFLAGS="-Wno-error=incompatible-pointer-types"

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
# We copy 'src' and the entry point script
COPY src/ ./src/
COPY fsm_redstone_synthesizer.py .

# Make the script executable
RUN chmod +x fsm_redstone_synthesizer.py

# Set the entrypoint so the container acts like a command-line tool
# This allows you to pass arguments directly to the docker run command
ENTRYPOINT ["python", "fsm_redstone_synthesizer.py"]
