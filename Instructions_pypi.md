# <b>uplink-python binding</b>

## <b>Instructions to push package on pypi</b>

Follow these instructions to make changes to the project and push ```uplink-python``` package to pypi, This would make the latest package install using the ```pip install``` command.

Assuming you have git cloned the project to your local directory and have already made the required changes to the project:

* In Command Prompt, navigate to the ```your-local-directory/uplink-python``` folder, here ```uplink-python``` is the root directory of cloned project.

Your directory structure would be something like this:

    uplink-python
    └── CHANGELOG.md
    └── cloudbuild.yaml
    └── Dockerfile
    └── docs
        └── index.html
    └── Instructions_pypi.md
    └── LICENSE
    └── README.assets
    └── README.md
    └── setup.py
    └── test
        └── test_cases.py
    └── uplink_python
        └── __init__.py
        └── uplink.py

* Open ```setup.py``` using any text editor and increment the package ```version```:

        setuptools.setup(
            name="uplink-python",
            version="1.0.4",

> Increment package version is mandatory because pypi does not allow updating a package with same version.

* The next step is to generate distribution packages for the package. These are archives that are uploaded to the Package Index and can be installed by pip.\
Make sure you have the latest versions of setuptools and wheel installed:

        $ python3 -m pip install --user --upgrade setuptools wheel

* Now run this command from the same directory where ```setup.py``` is located:

        $ python3 setup.py sdist

    This command should output a lot of text and once completed should generate two files in the dist directory:

        dist/
            uplink-python-x.x.x.tar.gz

* You will use twine to upload the distribution packages. You’ll need to install Twine if not already installed:

        $ python3 -m pip install --upgrade twine

* Once installed, run Twine to upload all of the archives under dist:
    * On Test PyPI:
        
        Test PyPI is a separate instance of the package index intended for testing and experimentation.

            $ python3 -m twine upload --repository testpypi dist/*
        You will be prompted for a username and password, enter username and password used on ```https://test.pypi.org/```

    * On PyPI:
        
        When you are ready to upload a real package to the Python Package Index, use the following command.

            $ python3 -m twine upload dist/*
        You will be prompted for a username and password, enter username and password used on ```https://pypi.org/```


> For more details and complete tutorial on how to publish a package on pypi, goto [Packaging Python Projects](https://packaging.python.org/tutorials/packaging-projects/)