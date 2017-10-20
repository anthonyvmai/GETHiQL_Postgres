rm LambdaPackage.zip
cd lib/python3.5/site-packages
zip -r9 ../../../LambdaPackage.zip *
cd ../../..
zip -g  ./LambdaPackage.zip *.py
zip -g  ./LambdaPackage.zip ./psycopg2/*
