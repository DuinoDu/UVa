USER_DIR = .
CXXFLAG += -g -Wall -Wextra -pthread
EXE = run
FILES = $(foreach d, $(USER_DIR), $(wildcard $(d)/*.cpp))
OBJS = $(patsubst %.cpp, %.o, $(FILES))

all : $(EXE)

clean : 
	rm -f $(EXE) *.o

%.o : %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

$(EXE) : $(OBJS) 
	$(CXX) $(CXXFLAGS) -lpthread $^ -o $@
