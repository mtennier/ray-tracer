#!/bin/bash

printf "cleaning all test cases...\n"

rm *.ppm

printf "running all test cases....\n\n"

printf "\n============\nambient\n"
python3 RayTracer.py ./TestCases/testAmbient.txt
printf "\n============\nbackground\n"
python3 RayTracer.py ./TestCases/testBackground.txt
printf "\n============\nbehind\n"
python3 RayTracer.py ./TestCases/testBehind.txt
printf "\n============\ndiffuse\n"
python3 RayTracer.py ./TestCases/testDiffuse.txt
printf "\n============\nillum\n"
python3 RayTracer.py ./TestCases/testIllum.txt
printf "\n============\nimg plane\n"
python3 RayTracer.py ./TestCases/testImgPlane.txt
printf "\n============\nintersection\n"
python3 RayTracer.py ./TestCases/testIntersection.txt
printf "\n============\nparsing\n"
python3 RayTracer.py ./TestCases/testParsing.txt
printf "\n============\nreflection\n"
python3 RayTracer.py ./TestCases/testReflection.txt
printf "\n============\nsample\n"
python3 RayTracer.py ./TestCases/testSample.txt
printf "\n============\nshadow\n"
python3 RayTracer.py ./TestCases/testShadow.txt
printf "\n============\nspecular\n"
python3 RayTracer.py ./TestCases/testSpecular.txt
printf "done!"