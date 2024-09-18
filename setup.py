from setuptools import setup, find_packages
from setuptools_scm import get_version

# Dynamically write the version to _version.py
def write_version_file():
    version = get_version()
    with open('src/dl_data_pipeline/_version.py', 'w') as f:
        docstring = '""" version of package """'
        f.write(f"{docstring}\nVERSION = '{version}'\n")

# requirements
def load_requirements():
    with open("requirements.txt", "r") as fp:
        required = fp.readlines()
    return required

if __name__ == "__main__":
    write_version_file()
    setup(
        name='dl_data_pipeline',
        use_scm_version=True,
        package_dir={'': 'src'},
        packages=find_packages(where='src'),
        install_requires = load_requirements(),
        author='Sacha Renault',
        author_email='',
        description='Easy pipeline to process datas.',
        long_description=open('readme.md').read(),
        long_description_content_type='text/markdown',
        url='https://sacha-renault.github.io/DataPipeline/',
        # license='MIT',
        # classifiers=[
        #     'Programming Language :: Python :: 3',
        #     'License :: OSI Approved :: MIT License',
        #     'Operating System :: OS Independent',
        # ],
        python_requires='>=3.10',
    )