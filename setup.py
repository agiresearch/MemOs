from setuptools import setup, find_packages

setup(
    name="aios-memos",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai",
        "anthropic",
        "requests",
        "qdrant-client",
        "chromadb",
        "numpy",
        "pydantic",
    ],
) 