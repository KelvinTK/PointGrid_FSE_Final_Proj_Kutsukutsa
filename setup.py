from setuptools import setup

name = 'pointgrid-contrib'
version = '1.0'

with open("README", 'r') as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read()

if __name__ == "__main__":
    print("Building wheel {}-{}".format(name, version))
    setup(
        name=name,
        version=version,
        description='Skoltech students contributed PointGrid project',
        author='FSE',
        author_email='A.Artemov@skoltech.ru',
        long_description=long_description,
        packages=[name],
        install_requires=requirements, #external packages as dependencies
)
