call "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvars64.bat"

if not exist .\win64_vs_build (
    mkdir .\win64_vs_build
)

cd .\win64_vs_build

if exist .\CMakeCache.txt ( 
    del CMakeCache.txt
) 

cmake -G "Visual Studio 15 2017 Win64"  -DOPENEXR_BUILD_STATIC=1 -DOPENEXR_BUILD_SHARED=1 -DOPENEXR_NAMESPACE_VERSIONING=0 -DOPENEXR_BUILD_ILMBASE=1 -DOPENEXR_BUILD_OPENEXR=1 -DOPENEXR_BUILD_PYTHON_LIBS=1 -DOPENEXR_BUILD_VIEWERS=0 -DOPENEXR_BUILD_TESTS=1 -DBOOST_ROOT=T:\Development\philip.luk\software\boost\win\1.68.0 -DZLIB_INCLUDE_DIR=T:\Development\philip.luk\repo\dev\internal\blender-git\blender-git-2.8\lib\win64_vc14\zlib\include    -DZLIB_LIBRARY=T:\Development\philip.luk\repo\dev\internal\blender-git\blender-git-2.8\lib\win64_vc14\zlib\lib\libz_st.lib -DPYTHON_EXECUTABLE=C:\pipeline28\python\370_64\python.exe -DPYTHON_INCLUDE_PATH=C:\pipeline28\python\370_64\Lib\site-packages\numpy -DPYTHON_INCLUDE_DIR=C:\pipeline28\python\370_64\include -DPYTHON_LIBRARY=C:\pipeline28\python\370_64\libs\python37.lib -DOPENEXR_PYTHON_MAJOR=3 -DOPENEXR_PYTHON_MINOR=7 -DCMAKE_INSTALL_PREFIX=T:\Development\philip.luk\repo\local\thirdparty\openexr\2.3.0 ..\

REM "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\MSBuild\15.0\Bin\amd64\msbuild.exe" .\INSTALL.vcxproj /p:Configuration=Release /t:Build /m 
