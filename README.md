"""
VeriSigil AI Python SDK
========================
pip install verisigil
"""

from setuptools import setup, find_packages
import os

# Read long description from README
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="verisigil",
    version="0.1.0",
    author="Raheem Larry Babatunde",
    author_email="info@verisigilai.com",
    description="Trust infrastructure for autonomous AI agents — identity, security, and compliance SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/raheem-verisigil/verisigil-ai",
    project_urls={
        "Documentation": "https://docs.verisigilai.com",
        "Website":        "https://www.verisigilai.com",
        "Bug Reports":    "https://github.com/raheem-verisigil/verisigil-ai/issues",
        "Source":         "https://github.com/raheem-verisigil/verisigil-ai",
    },
    packages=find_packages(exclude=["tests*", "examples*", "docs*"]),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "ruff>=0.1.0",
            "mypy>=1.0",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Security :: Cryptography",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "ai", "security", "identity", "did", "cryptography",
        "ai-agents", "eu-ai-act", "compliance", "trust",
        "llm-security", "zero-trust", "ai-identity", "autonomous-agents"
    ],
)
