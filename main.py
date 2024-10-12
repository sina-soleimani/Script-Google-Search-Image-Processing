import os
import time
import asyncio
import psycopg2
from simple_image_download import simple_image_download as simp
from PIL import Image, ImageFile
import requests
import io
import argparse
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()


# Function to download an image from URL and save it locally
async def download_image_from_url(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded image from {url}")
        return save_path
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return None


async def download_images(query, max_images):
    print('Downloading images...')
    response = simp.simple_image_download()
    urls = response.urls(query, max_images)

    download_tasks = []
    for url in urls:
        image_name = url.split("/")[-1]
        local_path = os.path.join('/tmp', image_name)
        download_tasks.append(download_image_from_url(url, local_path))

    local_image_paths = await asyncio.gather(*download_tasks)
    return [path for path in local_image_paths if path is not None]



def resize_image(image_path, target_size):
    try:
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        with Image.open(image_path) as img:
            resize_image = img.resize(target_size)
            resize_image.save(image_path)
            print(f"Resized and saved image: {image_path}")
    except Exception as e:
        print(f"Error resizing {image_path}: {e}")


# Resize multiple images
def resize_images(image_paths, target_size):
    print('Resizing images...')
    for image_path in image_paths:
        resize_image(image_path, target_size)


# Function to create the images table if it doesn't exist
def create_images_table(conn):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS images (
        id SERIAL PRIMARY KEY,
        image_data BYTEA NOT NULL
    );
    """
    with conn.cursor() as cursor:
        cursor.execute(create_table_query)
        conn.commit()
        print("Table 'images' ensured in the database.")



def store_images_in_database(image_paths, db_connection_details):
    print('Storing images in database...')

    with psycopg2.connect(**db_connection_details) as conn:
        create_images_table(conn)

        with conn.cursor() as cursor:
            for image_path in image_paths:
                try:
                    with open(image_path, 'rb') as f:
                        image_data = f.read()
                        cursor.execute(
                            "INSERT INTO images (image_data) VALUES (%s)",
                            (psycopg2.Binary(image_data),)
                        )
                        print(f"Inserted image {image_path} into the database.")
                except Exception as e:
                    print(f"Error inserting {image_path} into the database: {e}")

        conn.commit()



async def main(query, max_images, target_size, db_connection_details):
    print(f"Starting image processing for query: '{query}'")

    image_paths = await download_images(query, max_images)

    resize_images(image_paths, target_size)

    store_images_in_database(image_paths, db_connection_details)

    print("Processing complete!")
    time.sleep(6000)


# Entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download and process images from Google search results.')
    parser.add_argument('--query', type=str, default="cute kittens", help='Search query for images')
    parser.add_argument('--max_images', type=int, default=10, help='Maximum number of images to download')
    parser.add_argument('--db_name', type=str, default=os.environ.get('POSTGRES_DB', 'db'),
                        help='PostgreSQL database name')
    parser.add_argument('--db_user', type=str, default=os.environ.get('POSTGRES_USER', 'postgres'),
                        help='PostgreSQL user')
    parser.add_argument('--db_password', type=str, default=os.environ.get('POSTGRES_PASSWORD', 'postgres'),
                        help='PostgreSQL password')
    parser.add_argument('--db_host', type=str, default=os.environ.get('POSTGRES_HOST', 'db'), help='PostgreSQL host')
    parser.add_argument('--target_size', type=int, nargs=2, default=(300, 300),
                        help='Target size for images (width height)')

    args = parser.parse_args()

    db_connection_details = {
        "dbname": args.db_name,
        "user": args.db_user,
        "password": args.db_password,
        "host": args.db_host
    }

    asyncio.run(main(args.query, args.max_images, tuple(args.target_size), db_connection_details))
