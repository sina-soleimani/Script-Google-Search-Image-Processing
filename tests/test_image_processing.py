import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import asyncio


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import (
    download_image_from_url,
    download_images,
    resize_image,
    store_images_in_database,
    main
)

class TestImageProcessing(unittest.TestCase):

    @patch('requests.get')
    def test_download_image_from_url(self, mock_get):
        # Setup mock response
        mock_get.return_value.ok = True
        mock_get.return_value.content = b'Test Image Data'

        url = "http://example.com/test_image.png"
        save_path = "/tmp/test_image.png"

        # Call the function
        result = asyncio.run(download_image_from_url(url, save_path))

        self.assertEqual(result, save_path)
        mock_get.assert_called_once_with(url)

        # Check if file was created
        self.assertTrue(os.path.exists(save_path))
        os.remove(save_path)  # Cleanup

    @patch('simple_image_download.simple_image_download')
    @patch('main.download_image_from_url')
    def test_download_images(self, mock_download_image_from_url, mock_simple_image_download):
        mock_instance = mock_simple_image_download.return_value
        mock_instance.urls.return_value = [
            "http://example.com/test_image_1.png",
            "http://example.com/test_image_2.png"
        ]
        mock_download_image_from_url.side_effect = [
            "/tmp/test_image_1.png",
            "/tmp/test_image_2.png"
        ]

        query = "test query"
        max_images = 2

        image_paths = asyncio.run(download_images(query, max_images))

        # Verify the output; expect 2 images
        self.assertEqual(len(image_paths), 2)  # Expecting 2 paths
        mock_download_image_from_url.assert_called()  # Ensure it was called
        print(mock_instance)

    @patch('PIL.Image.open')
    @patch('PIL.Image.Image.save')  # Mock the save method
    def test_resize_image(self, mock_save, mock_open):
        mock_img = MagicMock()
        mock_img.size = (600, 600)
        mock_open.return_value.__enter__.return_value = mock_img  # Simulate opening an image

        image_path = "/tmp/test_image.png"
        target_size = (300, 300)

        # Call the function
        resize_image(image_path, target_size)

        # Verify that the image was resized and saved
        mock_img.resize.assert_called_once_with(target_size)

    @patch('psycopg2.connect')  # Mock the database connection
    def test_store_images_in_database(self, mock_connect):
        mock_conn = mock_connect.return_value.__enter__.return_value
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value

        image_paths = ["/tmp/test_image_1.png", "/tmp/test_image_2.png"]

        for path in image_paths:
            with open(path, 'wb') as f:
                f.write(b'Test Image Data')  # Ensure we have some data

        store_images_in_database(image_paths, {"dbname": "test_db"})

        for path in image_paths:
            os.remove(path)

    @patch('main.download_images')
    @patch('main.resize_images')
    @patch('main.store_images_in_database')
    def test_main_function(self, mock_store_images, mock_resize_images, mock_download_images):
        mock_download_images.return_value = ['/tmp/test_image.png']

        query = "test query"
        max_images = 2
        target_size = (300, 300)
        db_connection_details = {"dbname": "test_db"}

        asyncio.run(main(query, max_images, target_size, db_connection_details))
        mock_download_images.assert_called_once_with(query, max_images)

        mock_resize_images.assert_called_once_with(['/tmp/test_image.png'], target_size)

        mock_store_images.assert_called_once_with(['/tmp/test_image.png'], db_connection_details)

if __name__ == "__main__":
    unittest.main()
