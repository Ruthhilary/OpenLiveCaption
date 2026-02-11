"""Setup configuration for OpenLiveCaption"""

from setuptools import setup, find_packages

with open("README.md.txt", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="openlivecaption",
    version="2.0.0",
    author="OpenLiveCaption Team",
    description="System-wide live captions with real-time transcription",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/openlivecaption",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "opencv-python",
        "sounddevice",
        "numpy",
        "openai-whisper",
        "torch",
        "transformers",
        "soundfile",
        "PyQt6>=6.4.0",
        "pyaudiowpatch>=0.2.12.4; sys_platform == 'win32'",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "hypothesis>=6.82.0",
            "pyinstaller>=5.13.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "openlivecaption=src.main:main",
        ],
    },
)
