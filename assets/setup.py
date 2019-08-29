try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    "description": "Parking Lot Space Detector",
    "author": "Ujjal Das",
    "url": "https://github.com/ujjaldas132/parking-spot.git",
    "download_url": "https://github.com/ujjaldas132/parking-spot/archive/master.zip",
    "version": "0.1",
    "install_requires": ["cv2", "numpy", "yml"],
    "packages": ["assets"],
    "scripts": [],
    "name": "parking-spot"
}

setup(**config)
