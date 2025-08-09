rmdir dist /s /q
python -m build
pip install dist/algmatch-1.1.2.tar.gz
cls
python -m tests.verification
::python -m tests.SMTests.SM.smSingleVerifier
::python -m tests.SMTests.SMTSuper.smtSuperSingleVerifier
::python -m tests.HRTests.HRTSuper.hrtSuperSingleVerifier