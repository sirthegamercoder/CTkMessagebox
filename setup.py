from setuptools import setup, find_packages

setup(
    name="CTkMessagebox",
    version="3.5",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "customtkinter",
        "Pillow",
    ],
    package_data={
        "CTkMessagebox": ["icons/*"],
    },
)