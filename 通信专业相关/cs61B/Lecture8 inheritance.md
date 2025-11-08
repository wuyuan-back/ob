## Introduction
- ### overloading(重载):two methods with different signatures.
- ### Don't ==copy== the same code!!!
- List is a hypernym of SLList and ALList
## Simple hyponymic Relations
- two-steps
	- Step1 :Define a reference(引用) type for our hypernym.
	- Step2:Specify that SLLists and ALists are hyponyms of the type
```java
public interface(接口) List61B<Item>{
	public void insert(Item x);//item是个泛型
	
}

public class ALists<Item> implements List61B<Item>{

}
```