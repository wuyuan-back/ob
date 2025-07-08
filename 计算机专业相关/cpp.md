<> vs ""
non.h vs .h
## reference
& change the value 
EX:void quadratic(int a,int b,int c,double& root 1,double& root 2)
{

}
## string in cpp
use == != even +
内联函数
s1 ="hello"
s1.append("world");
s1.erase(int start,int end);
str.find()
yes return index;
no return string:: npos;
![[Pasted image 20250707104226.png]]
## c vsC++
C strings char ararys
C++ string string objiects
"  " usually is a string
string s = "hello ";
Can't string s = "hi" +"there";//error

int n = (int)"42";
## error
int n = StringtoInter("42");
yes;

string s ="hi";
s += '?' //"hi?"
s+= 41;// "hi?)" transfer into the ASC||

## string input
cin >> value; only a word a time;

## Grid
->data structure
STL;standard Template Library;
vector Grid stack Queue Set Map
### grid
two dimensional array

```c++
#icnlude “grid.h"
Grid<int> matrix(4,3);
matrix[1][0] = 42;

```


![[Pasted image 20250708144512.png]]![[Pasted image 20250708144649.png]]
iterate over a grid /遍历/
```c++
int computeSUm(Grid<int>& g)//不是复制
```
 
 ## collections
 # vector 
  can resize array
 ```c++
  #include"vector.h"
  vector<string> names;
```
 ![[Pasted image 20250708153337.png]]
  set can replace
  insert just move behind others
  remove move forward ==no gap==
  EX1 of  v.remove
  ![[Pasted image 20250708154739.png]]
  answer:C
 
 use v+= to add elements;
 ```C++
  for(string/*typename*/ s: v){
	  cout<< s << endl;
  }
  for(int i = 0; i< v.size;i++)//"for-each loop
  {
  cout<< s[i] << endl;
  }
```