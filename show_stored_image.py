import os
import psycopg2
from PIL import Image
import io
def retrieve_image_from_database(db_connection_details, image_id):

    with psycopg2.connect(**db_connection_details) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT image_data FROM images WHERE id = %s;", (image_id,))
            result = cursor.fetchone()  # Fetch the first result
            if result:
                return result[0]  # Return the binary data of the image
            else:
                print(f"No image found with ID: {image_id}")
                return None

def save_image(image_data, save_path):
    with open(save_path, 'wb') as file:
        file.write(image_data)
        print(f"Image saved to {save_path}")

def display_image(image_data):
    image = Image.open(io.BytesIO(image_data))  # Convert binary data to an image
    image.show()  # Display the image

# Entry point
if __name__ == "__main__":
    db_connection_details = {
        "dbname": os.environ.get('POSTGRES_DB', 'db'),
        "user": os.environ.get('POSTGRES_USER', 'postgres'),
        "password": os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        "host": os.environ.get('POSTGRES_HOST', 'localhost')
    }

    image_id = 1


    image_data = retrieve_image_from_database(db_connection_details, image_id)

    if image_data:

        display_image(image_data)

        save_image(image_data, 'retrieved_image.png')
