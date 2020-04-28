# makefile for building binding deps
    GOCMD=go
    GOBUILD=$(GOCMD) build
    GOCLEAN=$(GOCMD) clean

    GIT_REPO=https://github.com/storj/uplink-c
    UPLINKC_NAME=uplink-c
    LIBRARY_NAME=libuplinkc.so
    
    all: build
    build: 
	    git clone $(GIT_REPO)
	    cd uplink-c; $(GOBUILD) -o $(LIBRARY_NAME) -buildmode=c-shared;mv *.so ../
    clean: 
	    $(GOCLEAN)
	    rm -f $(LIBRARY_NAME)
	    rm -rf $(UPLINKC_NAME)
