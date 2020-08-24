package test;

import main.FirstSwingExample;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class FirstSwingExampleTest {

    @Test
    void main() {
    }

    @Test
    void foo() {
        FirstSwingExample ex = new FirstSwingExample();
        ex.foo(10);
    }
}