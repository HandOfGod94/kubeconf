from setuptools import find_packages, setup

setup(
    name="kubeconf",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "kubeconf = kubeconf.main:main",
        ],
    },
    author="Gahan Rakholia",
    author_email="gahan94rakh@gmail.com",
    description="A small wrapper around fzf and kubectl to view configmap with preview",
    url="https://github.com/handofgod94/kubeconf",
    python_requires=">=3.8",
)
