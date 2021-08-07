
The tests directory basically reflect the source folder.

These tests here have the goal to only check whether the API is working correctly.

Functional testing is already covered by other tests in the geckodriver source code.

To run tests use:
```bash
cd <your-repositories-path>
git clone https://github.com/reapler/geckordp
cd geckordp
python -m pip uninstall geckordp
python -m pip install -e $PWD
pytest tests/
```