

# Get Started with development
### Setup Compiler

Need gcc to be 10 to support coroutines and c++20. Why not clang? because pytorch is compiled using gcc so for now we will use gcc-10
```
sudo apt install gcc-10 g++-10
```
then point c++ to gcc-10

```
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-10 1000 --slave /usr/bin/g++ g++ /usr/bin/g++-10
```

### Install Scheduler

Install boost asio
```
wget https://boostorg.jfrog.io/artifactory/main/release/1.78.0/source/boost_1_78_0.tar.gz
tar -zxvf boost_1_78_0.tar.gz
```


update bashrc
```
export PATH=$PATH:/Users/levongh/Downloads/boost_1_78_0
export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:/Users/levongh/Downloads/boost_1_78_0/stage/lib
```

example https://github.com/jgaa/asio-composed-blog/blob/main/echo-server.cpp

### Install AWS SDK
Follow guidelines here https://docs.aws.amazon.com/sdk-for-cpp/v1/developer-guide/setup-linux.html

```
git clone --recurse-submodules https://github.com/aws/aws-sdk-cpp
cmake ../aws-sdk-cpp/ -DCMAKE_BUILD_TYPE=Release -DBUILD_ONLY="s3" -DCUSTOM_MEMORY_MANAGEMENT=OFF -DENABLE_TESTING=OFF -DENABLE_UNITY_BUILD=ON
make
make install
```

### Package manager
- [] try hunter gate


### Roadmap

TODO list
--- Phase I ---
1. [x] coroutine returns reference to pybytes
2. [x] pybytes returned to iterator
3. [~] coroutines run async while iterator is running  - Davit
4. [ ] AWS requests are sent - Davit
5. [ ] Setup baseline benchmarks - Davit

--- optimization land ---
1. [ ] optimize end-to-end reference passing - Levon 
2. [ ] add multithreading or switching to boost asio - Levon
3. [ ] benchmark if presigned generated URLs are faster - Levon (talk to Sasun)
4. [ ] range requests to AWS - Levon (talk to Sasun)

--- phase II ---
1. [ ] decompression - Levon
2. [ ] cache layer - Abhinav (Sasun has some LRU cache)
3. [ ] parsing into tensor -
4. [ ] custom shuffling order - 

--- phase III ---
1. [ ] add transformations - Abhinav
2. [ ] distributed training - Abhinav

--- phase IV ---
1. build docker for development
2. build 