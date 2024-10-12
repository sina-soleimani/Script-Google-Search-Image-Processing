<h1 align="center">Description</h1>



Created a versatile script ,capable of downloading images from Google search results based on a specified search query string, such as "cute kittens." Perform resizing tasks on the downloaded images and securely store them in a PostgreSQL database. provided inputs for the search query, the maximum number of images to be fetched, and essential PostgreSQL database connection details. The script's design emphasises asynchronous programming techniques to optimise efficiency, and it comes equipped with a suite of unit tests to ensure reliability and robustness. Additionally, consider Docker containers for convenient project encapsulation and deployment.


<h1 align="center">Installation</h1>

1. We install Docker Desktop software. By installing this software, not only does Docker run on the server, but it also provides a graphical interface for users to easily observe events within Docker.

2. In the PowerShell section with admin access, we run the following command:
```powershell
& 'C:\Program Files\Docker\Docker\DockerCli.exe' -SwitchDaemon
```
At this stage, the Docker daemon is defined.

3. In the next steps, WSL is configured on Windows. The following commands should be run in PowerShell with admin access:
```powershell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

wsl.exe --install
```

4. Download and install WSL from the following link on the system:
[WSL Download Link](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi)

5. After completing the above steps, the Docker Desktop software will be executable. If different sections of Docker Desktop are examined, tables for images, volumes, and containers are visible. Docker is ready for Docker projects to run on it.

6. Then, we build the Docker images that we transferred to the system with the following command:
```bash
docker-compose up --build
```
Using the above command, a container is created from each image file (created in step 6), and Django libraries are imported into the "web" container. In essence, the project is compiled on the server using this command.

7. We run the Docker containers created in the previous step to start the system:
```bash
docker-compose up
```
<h1 align="center">Usage</h1>
<h5>user can change imput values to take suit result. inputs are input-search-query for google search, maximum number of image to processing and target size </h5>


```bash
docker-compose exec app python main.py --query "panda" --max_images 10 --target_size 300 300 
```
<h1 align="center">Contributing</h1>


<h3 align="center">Download images via google search result</h2>




<h3 align="center">reize image </h2>



<h3 align="center">ٍsave images on postgres database </h2>


<h3 align="center">unit test for main module</h2>




