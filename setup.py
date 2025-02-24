from setuptools import setup, find_packages

setup(
    name="helix-audio",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "speech_recognition",
        "ollama",
        "google-generativeai",
        "sounddevice",
        "numpy",
        "kokoro",
        "webrtcvad",
        "pyaudio",
    ],
)