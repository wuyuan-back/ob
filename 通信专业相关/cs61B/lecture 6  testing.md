## 判断code的正确性
### 1.use unit test
- Writing a test
- use the print code(old and bad)
- use ==truth== library
```java
pubic class somethingtest{
	@Test  //provide a run botton
	pubic void function_1test(){
		double[] input = {10, 20 ,30,40};
		double expected = 125.0;
		double actual = sometiing.som(input);
		assertThat(actual).isEqualTo(expected); 
	}

```
### write the test first
## Rules of test
- special conditions
- 边界条件